/* GPL-2.0-or-later. Exact bounded native lease ABI; no MPI dependency. */
#define _GNU_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/random.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/sysmacros.h>
#include <sys/un.h>
#include <unistd.h>

static int envnum(const char *key,uint64_t *v) {
    const char *s=getenv(key); char *end; unsigned long long n;
    if(!s||!*s||strspn(s,"0123456789")!=strlen(s)) return EINVAL;
    errno=0;n=strtoull(s,&end,10);if(errno||*end) return EINVAL;*v=n;return 0;
}
static int hex64(const char *s) {return s&&strlen(s)==64&&strspn(s,"0123456789abcdef")==64;}
static uint64_t startticks(pid_t pid) {
    char path[64],line[4096],*s,*p,*save;FILE *f;uint64_t ticks=0;int i=0;
    snprintf(path,sizeof path,"/proc/%d/stat",pid);f=fopen(path,"re");if(!f)return 0;
    if(!fgets(line,sizeof line,f)){fclose(f);return 0;}fclose(f);
    s=strrchr(line,')');if(!s)return 0;
    for(p=strtok_r(s+1," ",&save);p;p=strtok_r(NULL," ",&save),i++) if(i==19)ticks=strtoull(p,NULL,10);
    return ticks;
}
static int lease_owned(pid_t pid) {
    const char *path=getenv("QE75_LEASE_LOCK");struct stat st;int fd;FILE *f;char line[512];
    char kind[32],scope[32],access[32];long owner;unsigned ma,mi;unsigned long long inode;
    if(!path)return EINVAL;
    fd=open(path,O_RDONLY|O_NOFOLLOW|O_CLOEXEC);if(fd<0)return errno;
    if(fstat(fd,&st)){int saved=errno;close(fd);return saved;}close(fd);
    f=fopen("/proc/locks","re");if(!f)return errno;
    while(fgets(line,sizeof line,f)) {
        if(sscanf(line,"%*s %31s %31s %31s %ld %x:%x:%llu",kind,scope,access,&owner,&ma,&mi,&inode)==7
           &&!strcmp(kind,"FLOCK")&&!strcmp(access,"WRITE")&&owner==pid
           &&ma==major(st.st_dev)&&mi==minor(st.st_dev)&&inode==st.st_ino) {fclose(f);return 0;}
    }
    fclose(f);return EACCES;
}
static void u32(unsigned char *p,uint32_t x){x=htonl(x);memcpy(p,&x,4);}
static uint32_t get32(const unsigned char *p){uint32_t x;memcpy(&x,p,4);return ntohl(x);}

int qe75_lease_call(int rank,int size,int action,int required_scope) {
    unsigned char request[180]={0},reply[48];struct sockaddr_un sa={0};struct ucred peer;
    socklen_t n=sizeof peer;struct pollfd wait;uint64_t pid,ticks;int sock=-1,pfd=-1,result=EACCES;
    const char *address=getenv("QE75_LEASE_SOCKET"),*jh=getenv("QE75_JOB_SHA256"),*ph=getenv("QE75_PROFILE_SHA256");
    if(rank<0||rank>=2||size!=2||(action!=1&&action!=2)||(required_scope!=1&&required_scope!=2))return EINVAL;
    if(!address||strlen(address)>sizeof(sa.sun_path)-2||!hex64(jh)||!hex64(ph)
       ||envnum("QE75_LEASE_PID",&pid)||envnum("QE75_LEASE_TICKS",&ticks)||!pid||pid>INT32_MAX)return EINVAL;
    memcpy(request,"R07L",4);u32(request+4,1);u32(request+8,action);u32(request+12,rank);u32(request+16,size);
    memcpy(request+20,jh,64);memcpy(request+84,ph,64);
    if(getrandom(request+148,32,0)!=32)return EIO;
    sock=socket(AF_UNIX,SOCK_SEQPACKET|SOCK_CLOEXEC|SOCK_NONBLOCK,0);if(sock<0)return errno;
    sa.sun_family=AF_UNIX;memcpy(sa.sun_path+1,address,strlen(address));
    if(connect(sock,(struct sockaddr*)&sa,sizeof(sa.sun_family)+1+strlen(address))){result=errno;goto done;}
    if(getsockopt(sock,SOL_SOCKET,SO_PEERCRED,&peer,&n)||peer.uid!=getuid()||peer.pid!=(pid_t)pid)goto done;
    pfd=syscall(SYS_pidfd_open,peer.pid,0);if(pfd<0){result=errno;goto done;}
    if(startticks(peer.pid)!=ticks||syscall(SYS_pidfd_send_signal,pfd,0,NULL,0)||lease_owned(peer.pid))goto done;
    if(send(sock,request,sizeof request,MSG_NOSIGNAL)!=(ssize_t)sizeof request){result=EIO;goto done;}
    wait.fd=sock;wait.events=POLLIN;
    if(poll(&wait,1,1000)!=1){result=ETIMEDOUT;goto done;}
    if(recv(sock,reply,sizeof reply,MSG_TRUNC)!=(ssize_t)sizeof reply){result=EPROTO;goto done;}
    if(memcmp(reply,"R07L",4)||get32(reply+4)!=1||memcmp(reply+16,request+148,32)) {result=EPROTO;goto done;}
    if(startticks(peer.pid)!=ticks||syscall(SYS_pidfd_send_signal,pfd,0,NULL,0)||lease_owned(peer.pid))goto done;
    result=(int)get32(reply+8);
    if(!result&&get32(reply+12)!=(uint32_t)required_scope)result=EACCES;
done:
    if(pfd>=0)close(pfd);
    if(sock>=0)close(sock);
    return result;
}
