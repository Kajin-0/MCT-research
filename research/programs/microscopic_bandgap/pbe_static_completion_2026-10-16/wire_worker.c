/* NON-MPI component fixture. Deliberately not a native H packet or material. */
#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/prctl.h>
#include <unistd.h>
int r07_static_lease(int,int,int,int64_t);
static int command(void){char line[32];return fgets(line,sizeof line,stdin)?line[0]:0;}
int main(int argc,char **argv){
    if(argc!=4)return 2;
    int rank=atoi(argv[1]),e;const char *root=argv[2],*mode=argv[3];
    char path[512];snprintf(path,sizeof path,"%s/pilot/H.rank%d",root,rank);
    if(!strcmp(mode,"premature")||!strcmp(mode,"foreign"))return r07_static_lease(rank,2,10,16)?3:99;
    e=r07_static_lease(rank,2,1,0);if(e)return 4;
    int fd=open(path,O_WRONLY|O_CREAT|O_EXCL,0600);if(fd<0)return 5;
    if(write(fd,"NON_MPI_FIXTURE!",!strcmp(mode,"incomplete")?4:16)<0)return 6;
    if(fsync(fd)||close(fd))return 7;
    puts("READY");fflush(stdout);
    if(command()!='g')return 8;
    if(!strcmp(mode,"lost")){puts("JOB DONE.");return 0;}
    if(!strcmp(mode,"burst")){
        fd=open(path,O_WRONLY|O_APPEND);if(fd<0)return 9;
        char b[4096]={0};for(int i=0;i<512;i++)if(write(fd,b,sizeof b)!=sizeof b)return 10;
        if(close(fd))return 11;
        puts("BURST");fflush(stdout);command();return 0;
    }
    e=r07_static_lease(rank,2,10,16);if(e)return 12;
    puts("FINAL");fflush(stdout);
    int c=command();
    if(c=='d'){
        if(prctl(PR_SET_DUMPABLE,0))return 13;
        puts("DUMPABLE0");fflush(stdout);c=command();
    }
    return c=='x'?0:14;
}
