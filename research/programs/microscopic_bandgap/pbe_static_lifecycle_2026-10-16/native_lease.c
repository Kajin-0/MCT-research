/* GPL-2.0-or-later. NON_SCIENCE lifecycle receipt ABI; NO MPI or command launcher.
 * Derived from R07 native_pair_execution lease_client.c. New magic/scope:
 * cannot accept a previous HSE/48-band or Python-wrapper authorization. */
#define _GNU_SOURCE
#include <arpa/inet.h>
#include <endian.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
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

#ifndef SO_PEERPIDFD
#define SO_PEERPIDFD 77
#endif
static int hex(const char *s,size_t n) {
    return s && strlen(s)==n && strspn(s,"0123456789abcdef")==n;
}
static uint64_t ticks(pid_t pid) {
    char path[64],line[4096],*p,*s,*save; FILE *f; int i=0;
    snprintf(path,sizeof path,"/proc/%d/stat",pid);
    f=fopen(path,"re"); if(!f)return 0;
    if(!fgets(line,sizeof line,f)){fclose(f);return 0;} fclose(f);
    s=strrchr(line,')'); if(!s)return 0;
    for(p=strtok_r(s+1," ",&save);p;p=strtok_r(NULL," ",&save),i++)
        if(i==19)return strtoull(p,NULL,10);
    return 0;
}
static int lock_owned(pid_t pid) {
    const char *path=getenv("R07_LIFECYCLE_LOCK"); struct stat st;
    char line[512],kind[32],scope[32],access[32]; long owner;
    unsigned ma,mi; unsigned long long inode; FILE *f; int fd;
    if(!path)return EINVAL;
    fd=open(path,O_RDONLY|O_NOFOLLOW|O_CLOEXEC); if(fd<0)return errno;
    if(fstat(fd,&st)){int e=errno;close(fd);return e;} close(fd);
    f=fopen("/proc/locks","re"); if(!f)return errno;
    while(fgets(line,sizeof line,f))
        if(sscanf(line,"%*s %31s %31s %31s %ld %x:%x:%llu",kind,scope,access,&owner,&ma,&mi,&inode)==7
           && !strcmp(kind,"FLOCK") && !strcmp(access,"WRITE") && owner==pid
           && ma==major(st.st_dev) && mi==minor(st.st_dev) && inode==st.st_ino) {
            fclose(f);return 0;
        }
    fclose(f);return EACCES;
}
static int alive(int fd) {
    struct pollfd p={.fd=fd,.events=POLLIN};
    int n=poll(&p,1,0); return n==0;
}
static void put32(unsigned char *p,uint32_t v){v=htonl(v);memcpy(p,&v,4);}
static uint32_t get32(const unsigned char *p){uint32_t v;memcpy(&v,p,4);return ntohl(v);}

int r07_static_lease(int rank,int size,int action,int64_t extent) {
    unsigned char request[252]={0},reply[48]; struct sockaddr_un sa={0};
    struct ucred peer; socklen_t n=sizeof peer; struct pollfd wait;
    const char *address=getenv("R07_LIFECYCLE_SOCKET"),*jh=getenv("R07_LIFECYCLE_JOB");
    const char *ph=getenv("R07_LIFECYCLE_PROFILE"),*inv=getenv("R07_LIFECYCLE_INVOCATION");
    const char *nonce=getenv("R07_LIFECYCLE_NONCE"),*ps=getenv("R07_LIFECYCLE_OWNER");
    const char *ts=getenv("R07_LIFECYCLE_OWNER_TICKS"); char *end;
    int sock=-1,pfd=-1,result=EACCES; uint64_t pid,start,bytes;
    if(!inv)inv=getenv("INVOCATION_ID"); /* kernel manager's managed-service environment */
    if(rank<0||rank>1||size!=2||(action!=1&&action!=10)||extent<0||extent>(1LL<<30)
       ||(action==1&&extent)||(action==10&&!extent))return EINVAL;
    if(!address||address[0]!='/'||strlen(address)>107||!hex(jh,64)||!hex(ph,64)
       ||!hex(inv,32)||!hex(nonce,32)||!ps||!ts||!*ps||!*ts
       ||strspn(ps,"0123456789")!=strlen(ps)||strspn(ts,"0123456789")!=strlen(ts))return EINVAL;
    errno=0;pid=strtoull(ps,&end,10);if(errno||*end||!pid||pid>INT_MAX)return EINVAL;
    errno=0;start=strtoull(ts,&end,10);if(errno||*end||!start)return EINVAL;
    memcpy(request,"R07L",4);put32(request+4,1);put32(request+8,action);
    put32(request+12,rank);put32(request+16,size);memcpy(request+20,jh,64);
    memcpy(request+84,ph,64);memcpy(request+148,inv,32);memcpy(request+180,nonce,32);
    if(getrandom(request+212,32,0)!=32)return EIO;
    bytes=htobe64((uint64_t)extent);memcpy(request+244,&bytes,8);
    sock=socket(AF_UNIX,SOCK_SEQPACKET|SOCK_CLOEXEC,0);if(sock<0)return errno;
    struct timeval timeout={.tv_sec=5,.tv_usec=0};
    if(setsockopt(sock,SOL_SOCKET,SO_RCVTIMEO,&timeout,sizeof timeout)
       ||setsockopt(sock,SOL_SOCKET,SO_SNDTIMEO,&timeout,sizeof timeout)){result=errno;goto done;}
    sa.sun_family=AF_UNIX;memcpy(sa.sun_path,address,strlen(address)+1);
    if(connect(sock,(struct sockaddr*)&sa,sizeof sa)){result=errno;goto done;}
    if(getsockopt(sock,SOL_SOCKET,SO_PEERCRED,&peer,&n)||peer.uid!=getuid()||peer.pid!=(pid_t)pid)goto done;
    /* Socket-bound pidfd, not an inherited socket or numeric PID guess. */
    n=sizeof pfd;
    if(getsockopt(sock,SOL_SOCKET,SO_PEERPIDFD,&pfd,&n)||n!=sizeof pfd||!alive(pfd))goto done;
    if(ticks(peer.pid)!=start||lock_owned(peer.pid))goto done;
    if(send(sock,request,sizeof request,MSG_NOSIGNAL)!=(ssize_t)sizeof request){result=EIO;goto done;}
    wait=(struct pollfd){.fd=sock,.events=POLLIN};
    if(poll(&wait,1,5000)!=1){result=ETIMEDOUT;goto done;}
    if(recv(sock,reply,sizeof reply,MSG_TRUNC)!=(ssize_t)sizeof reply){result=EPROTO;goto done;}
    if(memcmp(reply,"R07L",4)||get32(reply+4)!=1||memcmp(reply+16,request+212,32)) {result=EPROTO;goto done;}
    if(!alive(pfd)||ticks(peer.pid)!=start||lock_owned(peer.pid))goto done;
    uint32_t status=get32(reply+8);
    if(status>INT_MAX){result=EPROTO;goto done;}
    result=(int)status;
    if(!result&&get32(reply+12)!=1601)result=EACCES;
done:
    if(pfd>=0)close(pfd);
    if(sock>=0)close(sock);
    return result;
}
