/* GPL-2.0-or-later. Linux/ext4 project-local storage probe and reservation.
 * No MPI, QE execution, privilege changes or arbitrary-path cleanup.
 */
#define _GNU_SOURCE
#define _FILE_OFFSET_BITS 64
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/quota.h>
#include <sys/stat.h>
#include <sys/statfs.h>
#include <sys/statvfs.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/fs.h>

struct qe_quota {
    int32_t error, active;
    uint64_t used_bytes, hard_blocks_1024, soft_blocks_1024;
    uint32_t valid, padding;
    int32_t limit_error, status_error;
};
struct qe_storage {
    uint64_t fs_type, block_bytes, available_blocks, available_bytes;
    struct qe_quota quotas[3]; /* user, primary group, project */
    int32_t project_error;
    uint32_t project_id;
};

static int checked_multiply(uint64_t a,uint64_t b,uint64_t *out) {
    if (b && a > INT64_MAX/b) return EOVERFLOW;
    *out=a*b; return 0;
}

int qe_storage_probe(int fd,struct qe_storage *out) {
    struct statfs f; struct statvfs v; struct fsxattr attr;
    memset(out,0,sizeof(*out));
    if (sizeof(off_t)!=8) return EOVERFLOW;
    if(fstatfs(fd,&f) || fstatvfs(fd,&v)) return errno;
    out->fs_type=(uint64_t)f.f_type; out->block_bytes=v.f_frsize;
    out->available_blocks=v.f_bavail;
    int e=checked_multiply(v.f_bavail,v.f_frsize,&out->available_bytes);
    if(e) return e;
    /* Local non-CoW ext4 is the only currently qualified backend. */
    if(out->fs_type==0x01021994UL || out->fs_type==0x858458f6UL) return ENODEV;
    if(out->fs_type!=0xef53UL) return ENOTSUP;
    memset(&attr,0,sizeof(attr));
    if(ioctl(fd,FS_IOC_FSGETXATTR,&attr)) out->project_error=errno;
    else out->project_id=attr.fsx_projid;
    struct stat owner;
    if(fstat(fd,&owner)) return errno;
    unsigned int ids[3]={(unsigned int)owner.st_uid,(unsigned int)owner.st_gid,out->project_id};
    for(int type=0;type<3;type++) {
        struct dqblk q; memset(&q,0,sizeof(q));
#ifdef SYS_quotactl_fd
        long r=syscall(SYS_quotactl_fd,fd,QCMD(Q_GETQUOTA,type),ids[type],&q);
        if(r) {
            out->quotas[type].error=errno;
            out->quotas[type].limit_error=errno;
            /* ESRCH means this quota type is not enabled, not unlimited active quota. */
        } else {
            out->quotas[type].active=1;
            out->quotas[type].used_bytes=q.dqb_curspace;
            out->quotas[type].hard_blocks_1024=q.dqb_bhardlimit;
            out->quotas[type].soft_blocks_1024=q.dqb_bsoftlimit;
            out->quotas[type].valid=q.dqb_valid;
        }
        /* Q_GETINFO is read-only and may establish OFF when project-limit
         * retrieval is privileged. Never reinterpret EPERM alone as OFF. */
        struct dqinfo info; memset(&info,0,sizeof(info));
        long status=syscall(SYS_quotactl_fd,fd,QCMD(Q_GETINFO,type),0,&info);
        if(status) {
            out->quotas[type].status_error=errno;
            if(errno==ESRCH && !out->quotas[type].active)
                out->quotas[type].error=ESRCH;
        }
#else
        out->quotas[type].error=ENOSYS;
#endif
    }
    return 0;
}

int qe_reserve_fd(int fd,int64_t bytes,int64_t *allocated_bytes) {
    struct stat s;
    struct statfs fs;
    if(bytes<=0 || sizeof(off_t)!=8) return EINVAL;
    if(fstatfs(fd,&fs)) return errno;
    if((unsigned long)fs.f_type==0x01021994UL || (unsigned long)fs.f_type==0x858458f6UL) return ENODEV;
    if((unsigned long)fs.f_type!=0xef53UL) return ENOTSUP;
    if(fstat(fd,&s)) return errno;
    if(!S_ISREG(s.st_mode) || s.st_nlink!=1 || s.st_uid!=getuid()) return EPERM;
    /* Exclusive new file on ext4; never reserve a shared/reflink/foreign inode. */
    if(s.st_size!=0 || s.st_blocks!=0) return EEXIST;
    if(fallocate(fd,0,0,(off_t)bytes)) return errno;
    if(fdatasync(fd) || fstat(fd,&s)) return errno;
    if(s.st_size!=bytes || s.st_blocks<0 || s.st_blocks>INT64_MAX/512) return EIO;
    *allocated_bytes=(int64_t)s.st_blocks*512;
    if(*allocated_bytes<bytes) return EIO; /* sparse allocation is not a reservation */
    return 0;
}
