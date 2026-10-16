/* GPL-2.0-or-later. NON_SCIENCE. No QE linkage/material paths/launcher. */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/landlock.h>
#include <linux/seccomp.h>
#include <sched.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <unistd.h>
#ifdef R07_MPI
#include <mpi.h>
#endif
#ifndef LANDLOCK_ACCESS_FS_REFER
#define LANDLOCK_ACCESS_FS_REFER (1ULL<<13)
#endif
#ifndef LANDLOCK_ACCESS_FS_TRUNCATE
#define LANDLOCK_ACCESS_FS_TRUNCATE (1ULL<<14)
#endif
#ifndef LANDLOCK_ACCESS_FS_IOCTL_DEV
#define LANDLOCK_ACCESS_FS_IOCTL_DEV (1ULL<<15)
#endif
#define REQUIRE(x) do{if(!(x)){fprintf(stderr,"REFUSED line=%d errno=%d %s\n",__LINE__,errno,#x);return 70;}}while(0)
static int rules(const char *path){
 int abi=syscall(SYS_landlock_create_ruleset,NULL,0,LANDLOCK_CREATE_RULESET_VERSION);
 if(abi<5)return -1;
 uint64_t rights=LANDLOCK_ACCESS_FS_WRITE_FILE|LANDLOCK_ACCESS_FS_REMOVE_DIR|LANDLOCK_ACCESS_FS_REMOVE_FILE|LANDLOCK_ACCESS_FS_MAKE_CHAR|LANDLOCK_ACCESS_FS_MAKE_DIR|LANDLOCK_ACCESS_FS_MAKE_REG|LANDLOCK_ACCESS_FS_MAKE_SOCK|LANDLOCK_ACCESS_FS_MAKE_FIFO|LANDLOCK_ACCESS_FS_MAKE_BLOCK|LANDLOCK_ACCESS_FS_MAKE_SYM|LANDLOCK_ACCESS_FS_REFER|LANDLOCK_ACCESS_FS_TRUNCATE|LANDLOCK_ACCESS_FS_IOCTL_DEV;
 struct landlock_ruleset_attr rs={.handled_access_fs=rights};
 int r=syscall(SYS_landlock_create_ruleset,&rs,sizeof(rs),0);if(r<0)return -1;
 int fd=open(path,O_PATH|O_CLOEXEC);if(fd<0)return -1;
 struct landlock_path_beneath_attr rule={.allowed_access=LANDLOCK_ACCESS_FS_WRITE_FILE|LANDLOCK_ACCESS_FS_TRUNCATE,.parent_fd=fd};
 if(syscall(SYS_landlock_add_rule,r,LANDLOCK_RULE_PATH_BENEATH,&rule,0))return -1;
 if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0))return -1;
 if(syscall(SYS_landlock_restrict_self,r,0))return -1;
 close(r);close(fd);return abi;
}
#define DENY(n) BPF_JUMP(BPF_JMP|BPF_JEQ|BPF_K,(n),0,1),BPF_STMT(BPF_RET|BPF_K,SECCOMP_RET_ERRNO|EPERM)
static int filter(void){
 struct sock_filter b[]={
 BPF_STMT(BPF_LD|BPF_W|BPF_ABS,offsetof(struct seccomp_data,arch)),
 BPF_JUMP(BPF_JMP|BPF_JEQ|BPF_K,AUDIT_ARCH_X86_64,1,0),BPF_STMT(BPF_RET|BPF_K,SECCOMP_RET_KILL_PROCESS),
 BPF_STMT(BPF_LD|BPF_W|BPF_ABS,offsetof(struct seccomp_data,nr)),
 /* x32 syscall encodings are outside this ABI. */
 BPF_JUMP(BPF_JMP|BPF_JSET|BPF_K,0x40000000,0,1),BPF_STMT(BPF_RET|BPF_K,SECCOMP_RET_KILL_PROCESS),
 DENY(SYS_socket),DENY(SYS_socketpair),DENY(SYS_connect),DENY(SYS_bind),DENY(SYS_listen),DENY(SYS_accept),DENY(SYS_accept4),DENY(SYS_fork),DENY(SYS_vfork),DENY(SYS_execve),DENY(SYS_execveat),DENY(SYS_ptrace),DENY(SYS_pidfd_getfd),
 /* clone3 ENOSYS permits libc to fall back to inspectable clone for threads. */
 BPF_JUMP(BPF_JMP|BPF_JEQ|BPF_K,SYS_clone3,0,1),BPF_STMT(BPF_RET|BPF_K,SECCOMP_RET_ERRNO|ENOSYS),
 BPF_JUMP(BPF_JMP|BPF_JEQ|BPF_K,SYS_clone,0,4),
 BPF_STMT(BPF_LD|BPF_W|BPF_ABS,offsetof(struct seccomp_data,args[0])),
 BPF_JUMP(BPF_JMP|BPF_JSET|BPF_K,CLONE_THREAD,1,0),BPF_STMT(BPF_RET|BPF_K,SECCOMP_RET_ERRNO|EPERM),
 BPF_STMT(BPF_RET|BPF_K,SECCOMP_RET_ALLOW),
 BPF_STMT(BPF_RET|BPF_K,SECCOMP_RET_ALLOW)};
 struct sock_fprog p={.len=sizeof(b)/sizeof(b[0]),.filter=b};
 return prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&p);
}
static int denied_open(const char *p){
 errno=0;int fd=open(p,O_WRONLY|O_TRUNC|O_CLOEXEC);int e=errno;if(fd>=0)close(fd);return fd<0&&e==EACCES;
}
int main(int argc,char **argv){
 REQUIRE(argc==3);REQUIRE(strlen(argv[1])<400&&strlen(argv[2])==32);alarm(15);
 /* Every inherited descriptor beyond bounded regular stdio is closed BEFORE confinement. */
 for(int i=0;i<3;i++){struct stat s;REQUIRE(fstat(i,&s)==0&&S_ISREG(s.st_mode));}
 REQUIRE(syscall(SYS_close_range,3U,~0U,0)==0);
 REQUIRE(chdir(argv[1])==0);
 printf("NON_SCIENCE READY pid=%ld\n",(long)getpid());fflush(stdout);
 char token[64]={0};int ready=0;
 for(int i=0;i<500;i++){int f=open("go",O_RDONLY|O_NOFOLLOW|O_CLOEXEC);if(f>=0){ssize_t n=read(f,token,63);close(f);if(n==32&&!memcmp(token,argv[2],32)){ready=1;break;}}usleep(10000);}
 REQUIRE(ready);
#ifndef R07_MPI
 /* Demonstrate Landlock's inherited-FD exemption ONLY on a disposable canary. */
 int inherited=open("foreign/inherited",O_WRONLY|O_CLOEXEC);REQUIRE(inherited>=3);
#endif
 int abi=rules("output/allowed");REQUIRE(abi>=5);REQUIRE(filter()==0);
 REQUIRE(prctl(PR_GET_NO_NEW_PRIVS,0,0,0,0)==1);
 REQUIRE(denied_open("input/ro"));REQUIRE(denied_open("foreign/canary"));REQUIRE(denied_open("temp/ro"));
 REQUIRE(denied_open("foreign/new_missing"));
 int f=open("output/allowed",O_WRONLY|O_TRUNC|O_NOFOLLOW|O_CLOEXEC);REQUIRE(f>=0);REQUIRE(write(f,"allowed\n",8)==8);REQUIRE(fsync(f)==0);REQUIRE(close(f)==0);
 /* O_TMPFILE creates no pathname; an unexpected allowed call still closes an empty inode. */
 errno=0;f=open("/tmp",O_TMPFILE|O_RDWR|O_CLOEXEC,0600);int et=errno;if(f>=0)close(f);REQUIRE(f<0&&et==EACCES);
 errno=0;f=open("/dev/shm",O_TMPFILE|O_RDWR|O_CLOEXEC,0600);int es=errno;if(f>=0)close(f);REQUIRE(f<0&&es==EACCES);
 errno=0;f=socket(AF_INET,SOCK_STREAM,0);REQUIRE(f<0&&errno==EPERM);
 errno=0;f=socket(AF_UNIX,SOCK_STREAM,0);REQUIRE(f<0&&errno==EPERM);
 errno=0;long child=syscall(SYS_fork);REQUIRE(child<0&&errno==EPERM);
#ifndef R07_MPI
 REQUIRE(write(inherited,"X",1)==1);REQUIRE(close(inherited)==0);
 errno=0;REQUIRE(fcntl(inherited,F_GETFD)<0&&errno==EBADF);
 printf("LANDLOCK abi=%d allowed=1 RO_foreign_TMPDIR_devshm_denied=1 socket_spawn_denied=1 inherited_exemption_demonstrated_then_closed=1\n",abi);
#else
 printf("LANDLOCK abi=%d enforced; entering singleton MPI_Init_thread (no launcher/helper/network allowed)\n",abi);fflush(stdout);
 int provided=-1,size=-1,rank=-1;int rc=MPI_Init_thread(NULL,NULL,MPI_THREAD_SINGLE,&provided);
 REQUIRE(rc==MPI_SUCCESS);REQUIRE(MPI_Comm_size(MPI_COMM_WORLD,&size)==MPI_SUCCESS);REQUIRE(MPI_Comm_rank(MPI_COMM_WORLD,&rank)==MPI_SUCCESS);
 REQUIRE(size==1&&rank==0&&provided>=MPI_THREAD_SINGLE);
 REQUIRE(MPI_Finalize()==MPI_SUCCESS);
 printf("SINGLETON world_size=%d rank=%d finalized=1\n",size,rank);
#endif
 fflush(stdout);return 0;
}
