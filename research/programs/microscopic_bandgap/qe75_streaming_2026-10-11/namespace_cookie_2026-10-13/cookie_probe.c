/* Fixed non-MPI service. No fork, exec, MPI or IP connect/send operation. */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <ifaddrs.h>
#include <inttypes.h>
#include <limits.h>
#include <net/if.h>
#include <netinet/in.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/random.h>
#include <sys/resource.h>
#include <sys/file.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/un.h>
#include <time.h>
#include <unistd.h>

static int fail(const char *step,int code) {
    fprintf(stdout,"{\"event\":\"REFUSAL\",\"step\":\"%s\",\"errno\":%d,\"pid\":%ld}\n",step,code,(long)getpid());
    fflush(stdout);return 94;
}
static int hex64(const char *s) {return s&&strlen(s)==64&&strspn(s,"0123456789abcdef")==64;}
static uint64_t number(const char *s) {
    char *end=NULL;if(!s||!*s||strspn(s,"0123456789")!=strlen(s))return 0;
    errno=0;unsigned long long n=strtoull(s,&end,10);return errno||*end?0:(uint64_t)n;
}
static uint64_t ticks(pid_t pid) {
    char path[64],line[4096],*p,*save=NULL;uint64_t result=0;
    snprintf(path,sizeof path,"/proc/%ld/stat",(long)pid);FILE *f=fopen(path,"re");if(!f)return 0;
    if(!fgets(line,sizeof line,f)){fclose(f);return 0;}fclose(f);p=strrchr(line,')');if(!p)return 0;
    int i=0;for(p=strtok_r(p+1," ",&save);p;p=strtok_r(NULL," ",&save),i++)if(i==19)result=number(p);
    return result;
}
static int fresh_cookie(uint64_t *value) {
    int fd=socket(AF_INET,SOCK_DGRAM|SOCK_CLOEXEC,0);if(fd<0)return errno;
    socklen_t n=sizeof(*value);int e=getsockopt(fd,SOL_SOCKET,SO_NETNS_COOKIE,value,&n)?errno:0;
    close(fd);return e?e:(n==sizeof(*value)&&*value?0:EPROTO);
}
static int read_cgroup(char *out,size_t n) {
    FILE *f=fopen("/proc/self/cgroup","re");if(!f)return errno;
    if(!fgets(out,(int)n,f)){fclose(f);return EIO;}fclose(f);
    out[strcspn(out,"\n")]=0;
    if(strncmp(out,"0::/",4)||strspn(out,"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/._:-@\\")!=strlen(out))return EPROTO;
    return 0;
}

int main(int argc,char **argv) {
    if(argc!=10)return fail("fixed_argv",EINVAL);
    const char *path=argv[1],*job=argv[4],*profile=argv[5],*case_name=argv[9];
    uint64_t owner=number(argv[2]),owner_ticks=number(argv[3]),host_cookie=number(argv[6]);
    uint64_t lock_dev=number(argv[7]),lock_ino=number(argv[8]);
    if(!hex64(job)||!hex64(profile)||!owner||owner>INT_MAX||!owner_ticks||!host_cookie||!lock_dev||!lock_ino||
       (strcmp(case_name,"normal")&&strcmp(case_name,"bad_nonce")&&strcmp(case_name,"owner_disconnect")))return fail("fixed_arguments",EINVAL);
    struct rlimit nf,fs,co;
    if(getrlimit(RLIMIT_NOFILE,&nf)||getrlimit(RLIMIT_FSIZE,&fs)||getrlimit(RLIMIT_CORE,&co))return fail("rlimits",errno);
    if(nf.rlim_cur!=64||nf.rlim_max!=64||fs.rlim_cur!=16384||co.rlim_cur!=0)return fail("rlimit_values",EPROTO);
    int inherited_sockets=0;
    for(int fd=0;fd<64;fd++){struct stat s;if(!fstat(fd,&s)&&S_ISSOCK(s.st_mode))inherited_sockets++;}
    if(inherited_sockets)return fail("inherited_socket",EPROTO);
    uint64_t cookies[3]={0};
    for(int i=0;i<3;i++){int e=fresh_cookie(&cookies[i]);if(e)return fail("fresh_cookie",e);}
    if(cookies[0]!=cookies[1]||cookies[1]!=cookies[2])return fail("cookie_changed",EPROTO);
    struct ifaddrs *ifs=NULL;if(getifaddrs(&ifs))return fail("getifaddrs",errno);
    unsigned nonlo=0,lo=0,up=0,bad_address=0;
    for(struct ifaddrs *p=ifs;p;p=p->ifa_next){
        if(strcmp(p->ifa_name,"lo")||!(p->ifa_flags&IFF_LOOPBACK))nonlo++;
        else{lo++;if(p->ifa_flags&IFF_UP)up++;}
        if(!p->ifa_addr)continue;
        if(p->ifa_addr->sa_family==AF_INET){
            uint32_t a=ntohl(((struct sockaddr_in*)p->ifa_addr)->sin_addr.s_addr);if((a>>24)!=127)bad_address++;
        } else if(p->ifa_addr->sa_family==AF_INET6){
            if(!IN6_IS_ADDR_LOOPBACK(&((struct sockaddr_in6*)p->ifa_addr)->sin6_addr))bad_address++;
        }
    }
    freeifaddrs(ifs);
    struct if_nameindex *names=if_nameindex();if(!names)return fail("if_nameindex",errno);
    unsigned interfaces=0;for(struct if_nameindex *p=names;p->if_index;p++){interfaces++;if(strcmp(p->if_name,"lo"))nonlo++;}
    if_freenameindex(names);
    char cg[1024];int cg_errno=read_cgroup(cg,sizeof cg);if(cg_errno)return fail("self_cgroup",cg_errno);
    const char *inv=getenv("INVOCATION_ID");
    if(!inv||strlen(inv)!=32||strspn(inv,"0123456789abcdef")!=32)return fail("invocation",EPROTO);
    struct stat ns,exe;int ns_errno=stat("/proc/self/ns/net",&ns)?errno:0;
    int exe_errno=stat("/proc/self/exe",&exe)?errno:0;
    unsigned char random[32];if(getrandom(random,sizeof random,0)!=(ssize_t)sizeof random)return fail("nonce",errno);
    char nonce[65];for(int i=0;i<32;i++)snprintf(nonce+2*i,3,"%02x",random[i]);
    char hello[4096];
    int bytes=snprintf(hello,sizeof hello,
        "{\"event\":\"HELLO\",\"scope\":\"NON_MPI_NAMESPACE_COMPONENT\",\"job\":\"%s\",\"profile\":\"%s\","
        "\"nonce\":\"%s\",\"pid\":%ld,\"uid\":%ld,\"start_ticks\":%"PRIu64",\"invocation\":\"%s\","
        "\"cgroup\":\"%s\",\"cookies\":[%"PRIu64",%"PRIu64",%"PRIu64"],\"inherited_sockets\":%d,"
        "\"interfaces\":%u,\"lo_entries\":%u,\"up_entries\":%u,\"nonlo_entries\":%u,\"bad_addresses\":%u,"
        "\"ns_stat_errno\":%d,\"exe_stat_errno\":%d,\"exe_dev\":%"PRIu64",\"exe_ino\":%"PRIu64"}",
        job,profile,nonce,(long)getpid(),(long)getuid(),ticks(getpid()),inv,cg+3,
        cookies[0],cookies[1],cookies[2],inherited_sockets,interfaces,lo,up,nonlo,bad_address,ns_errno,exe_errno,
        exe_errno?0:(uint64_t)exe.st_dev,exe_errno?0:(uint64_t)exe.st_ino);
    if(bytes<0||bytes>=(int)sizeof hello)return fail("hello_extent",EOVERFLOW);
    puts(hello);fflush(stdout);
    struct sockaddr_un sa={.sun_family=AF_UNIX};
    if(strlen(path)>=sizeof sa.sun_path)return fail("path_extent",ENAMETOOLONG);
    strcpy(sa.sun_path,path);
    int sock=socket(AF_UNIX,SOCK_SEQPACKET|SOCK_CLOEXEC,0);if(sock<0)return fail("owner_socket",errno);
    if(connect(sock,(struct sockaddr*)&sa,sizeof sa))return fail("owner_connect",errno);
    struct ucred peer;socklen_t pn=sizeof peer;
    if(getsockopt(sock,SOL_SOCKET,SO_PEERCRED,&peer,&pn)||peer.pid!=(pid_t)owner||peer.uid!=getuid())return fail("owner_peer",EACCES);
    int pidfd=(int)syscall(SYS_pidfd_open,peer.pid,0);
    if(pidfd<0||ticks(peer.pid)!=owner_ticks||syscall(SYS_pidfd_send_signal,pidfd,0,NULL,0))return fail("live_owner",EACCES);
    if(send(sock,hello,(size_t)bytes,MSG_NOSIGNAL)!=bytes)return fail("hello_send",EIO);
    struct pollfd wait={.fd=sock,.events=POLLIN};if(poll(&wait,1,3000)!=1)return fail("grant_wait",ETIMEDOUT);
    char response[4096]={0};_Alignas(struct cmsghdr) char control[CMSG_SPACE(sizeof(int))];
    struct iovec io={.iov_base=response,.iov_len=sizeof response-1};
    struct msghdr msg={.msg_iov=&io,.msg_iovlen=1,.msg_control=control,.msg_controllen=sizeof control};
    ssize_t received=recvmsg(sock,&msg,MSG_CMSG_CLOEXEC);if(received<=0)return fail("owner_eof",EPIPE);
    int lease=-1,count=0;
    for(struct cmsghdr *c=CMSG_FIRSTHDR(&msg);c;c=CMSG_NXTHDR(&msg,c)){
        if(c->cmsg_level==SOL_SOCKET&&c->cmsg_type==SCM_RIGHTS){
            if(c->cmsg_len!=CMSG_LEN(sizeof(int)))return fail("fd_extent",EPROTO);
            memcpy(&lease,CMSG_DATA(c),sizeof lease);count++;
        }
    }
    if(count!=1||(msg.msg_flags&(MSG_TRUNC|MSG_CTRUNC)))return fail("grant_rights",EPROTO);
    char expected[512];
    snprintf(expected,sizeof expected,"GRANT|1|%s|%s|%s|%"PRIu64"|%"PRIu64"|NON_MPI_NAMESPACE_COMPONENT",job,profile,nonce,cookies[0],host_cookie);
    struct stat ls;
    if(received!=(ssize_t)strlen(expected)||memcmp(response,expected,(size_t)received)||fstat(lease,&ls)||
       !S_ISREG(ls.st_mode)||(uint64_t)ls.st_dev!=lock_dev||(uint64_t)ls.st_ino!=lock_ino||flock(lease,LOCK_EX|LOCK_NB))
        return fail("grant_binding",EACCES);
    if(cookies[0]==host_cookie||interfaces!=1||!lo||up!=lo||nonlo||bad_address)return fail("isolation_conditions",EPROTO);
    if(ticks(peer.pid)!=owner_ticks||syscall(SYS_pidfd_send_signal,pidfd,0,NULL,0))return fail("owner_retired",EACCES);
    printf("{\"event\":\"DONE\",\"pid\":%ld,\"cookie\":%"PRIu64",\"scope\":\"NON_MPI_NAMESPACE_COMPONENT\"}\n",(long)getpid(),cookies[0]);fflush(stdout);
    struct timespec pause={1,0};nanosleep(&pause,NULL);
    close(lease);close(pidfd);close(sock);return 0;
}
