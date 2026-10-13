#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
extern int qe75_lease_call(int,int,int,int);
int main(int argc,char **argv){
    if(argc!=4)return 90;
    int rank=atoi(argv[1]);const char *mode=argv[2],*root=argv[3];
    int scope=!strcmp(mode,"native_scope")?2:1;
    int e=qe75_lease_call(rank,2,1,scope);if(e){fprintf(stderr,"REGISTER_REFUSED %d\n",e);return 91;}
    for(int i=0;i<100;i++){
        e=qe75_lease_call(rank,2,2,scope);if(!e)break;
        if(e!=EAGAIN)return 92;
        usleep(10000);
    }
    if(e)return 93;
    /* Explicit SERIAL fixture release after both live CHECK receipts. This is
       not MPI_Barrier and never grants a native scope. */
    char ready[2048],go[2048],pidtext[32];
    snprintf(ready,sizeof ready,"%s/out/rank%d.ready",root,rank);
    snprintf(go,sizeof go,"%s/out/actors.go",root);
    int readyfd=open(ready,O_CREAT|O_EXCL|O_NOFOLLOW|O_WRONLY,0600);
    if(readyfd<0)return 102;
    int length=snprintf(pidtext,sizeof pidtext,"%d",getpid());
    if(write(readyfd,pidtext,(size_t)length)!=length)return 103;
    close(readyfd);
    int released=0;
    for(int i=0;i<200;i++){
        if(access(go,F_OK)==0){released=1;break;}
        usleep(10000);
    }
    if(!released)return 104;
    fprintf(stdout,"COMPILED_ABI_NO_MPI rank=%d pid=%d\n",rank,getpid());fflush(stdout);
    if(!strcmp(mode,"hold")||!strcmp(mode,"guard_crash")){sleep(20);return 0;}
    if(!strcmp(mode,"orphan")){
        pid_t p=fork();if(p<0)return 94;
        if(!p){setsid();sleep(20);_exit(0);}return 0;
    }
    if(!strcmp(mode,"log_flood")){
        char b[4096];memset(b,'x',sizeof b);
        for(int i=0;i<32;i++)if(write(STDOUT_FILENO,b,sizeof b)<0)return 95;
    }
    if(!strcmp(mode,"file_limit")){
        char path[2048];snprintf(path,sizeof path,"%s/out/rank%d.data",root,rank);
        int fd=open(path,O_CREAT|O_EXCL|O_WRONLY,0600);if(fd<0)return 96;
        char b[4096];memset(b,0,sizeof b);
        for(int i=0;i<64;i++)if(write(fd,b,sizeof b)<0){close(fd);return 97;}
        close(fd);return 98; /* Reaching this is a hard-limit failure. */
    }
    if(!strcmp(mode,"oom")&&rank==0){
        /* One bounded <100-MiB allocation, intentionally above a 64-MiB unit.
           No native QE/MPI and no host-scale exhaustion. */
        size_t n=96u*1024u*1024u;
        volatile unsigned char *p=malloc(n);if(!p)return 99;
        for(size_t i=0;i<n;i+=4096)p[i]=1;
        sleep(1);free((void*)p);return 100;
    }
    if(!strcmp(mode,"task_limit")&&rank==0){
        pid_t children[24];int n=0,limited=0;
        for(int i=0;i<24;i++){
            pid_t p=fork();if(p<0){limited=errno==EAGAIN;break;}
            if(!p){usleep(250000);_exit(0);}children[n++]=p;
        }
        for(int i=0;i<n;i++)waitpid(children[i],NULL,0);
        fprintf(stdout,"TASK_LIMIT_EAGAIN %d created=%d\n",limited,n);fflush(stdout);
        return limited?0:101;
    }
    usleep(50000);return 0;
}
