/* Tiny serial integration worker. No MPI/PW/FFT library or initialization. */
#define _GNU_SOURCE
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
int qe75_lease_call(int,int,int,int);
int main(int argc,char **argv) {
    if(argc!=4) return 99;
    int rank=atoi(argv[1]),code,scope=1;char *mode=argv[3];
    if(!strcmp(mode,"native_scope"))scope=2;
    if(!strcmp(mode,"bad_job"))setenv("QE75_JOB_SHA256","ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",1);
    if(!strcmp(mode,"bad_profile"))setenv("QE75_PROFILE_SHA256","ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",1);
    if(!strcmp(mode,"bad_ticks"))setenv("QE75_LEASE_TICKS","1",1);
    if(!strcmp(mode,"duplicate"))rank=0;
    code=qe75_lease_call(rank,2,1,scope);if(code)return code;
    if(!strcmp(mode,"dead_rank")&&rank==0)return 0;
    for(int i=0;i<100;i++) {
        code=qe75_lease_call(rank,2,2,scope);
        if(!code)break;
        if(code!=EAGAIN)return code;
        usleep(10000);
    }
    if(code)return 98;
    pid_t child=fork();if(child<0)return 96;
    if(child==0){
        execl(getenv("QE75_TEST_PYTHON"),getenv("QE75_TEST_PYTHON"),getenv("QE75_TEST_HOOK"),argv[2],"normal",NULL);
        _exit(95);
    }
    int status;if(waitpid(child,&status,0)!=child||!WIFEXITED(status)||WEXITSTATUS(status))return 94;
    if(!strcmp(mode,"hold"))sleep(8);
    else if(!strcmp(mode,"forged_hook"))usleep(500000);
    else usleep(150000);
    return 0;
}
