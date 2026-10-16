/* GPL-2.0-or-later. No ENV/CLI/boolean can release the material driver. */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
int r07_density_build_gate(void){return EPERM;}
int r07_density_sync(const char *path){
    int fd=open(path,O_RDONLY|O_NOFOLLOW|O_CLOEXEC);if(fd<0)return errno;
    struct stat s;int e=0;
    if(fstat(fd,&s))e=errno;
    else if(!S_ISREG(s.st_mode)||s.st_uid!=getuid()||s.st_size<=0||s.st_size>(1LL<<30))e=EINVAL;
    else if(fsync(fd))e=errno;
    if(close(fd)&&!e)e=errno;
    return e;
}
