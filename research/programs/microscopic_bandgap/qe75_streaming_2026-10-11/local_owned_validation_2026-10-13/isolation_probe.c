/* Non-MPI, one-process prerequisite probe. Never execs another program. */
#define _GNU_SOURCE
#include <errno.h>
#include <ifaddrs.h>
#include <net/if.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

int main(void) {
    struct stat ns; struct ifaddrs *ifs = NULL;
    struct rlimit fsize, core;
    const char *failed=NULL;
    if (stat("/proc/self/ns/net", &ns)) failed="self_netns_stat";
    else if (getifaddrs(&ifs)) failed="getifaddrs";
    else if (getrlimit(RLIMIT_FSIZE, &fsize)) failed="fsize_getrlimit";
    else if (getrlimit(RLIMIT_CORE, &core)) failed="core_getrlimit";
    if (failed) {
        printf("{\"failed_step\":\"%s\",\"errno\":%d,\"pid\":%ld,\"uid\":%ld}\n",
               failed,errno,(long)getpid(),(long)getuid());fflush(stdout);
        return 91;
    }
    unsigned nonloop = 0, loop = 0;
    for (struct ifaddrs *p=ifs; p; p=p->ifa_next) {
        if (!p->ifa_addr) continue;
        if (p->ifa_flags & IFF_LOOPBACK) ++loop; else ++nonloop;
    }
    freeifaddrs(ifs);
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    int inet_errno = fd < 0 ? errno : 0;
    if (fd >= 0) close(fd); /* Does not bind/connect/send any network data. */
    printf("{\"pid\":%ld,\"uid\":%ld,\"netns_inode\":%llu,"
           "\"nonloop_addresses\":%u,\"loop_addresses\":%u,"
           "\"inet_socket_errno\":%d,\"fsize\":%llu,\"core\":%llu}\n",
           (long)getpid(), (long)getuid(), (unsigned long long)ns.st_ino,
           nonloop, loop, inet_errno, (unsigned long long)fsize.rlim_cur,
           (unsigned long long)core.rlim_cur);
    fflush(stdout);
    struct timespec pause={2,0}; nanosleep(&pause,NULL);
    return nonloop ? 92 : 0;
}
