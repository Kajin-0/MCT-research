/* Explicit serial component fixture: never initializes/links MPI or PW. */
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
int qe75_lease_call(int,int,int,int);
int main(int argc,char **argv) {
    int rank,scope,code;
    if(argc!=3)return 99;
    rank=atoi(argv[1]);scope=atoi(argv[2]);
    code=qe75_lease_call(rank,2,1,scope);if(code)return code;
    for(int i=0;i<40;i++) {
        code=qe75_lease_call(rank,2,2,scope);
        if(!code){usleep(150000);return 0;}
        if(code!=EAGAIN)return code;
        usleep(10000);
    }
    return 98;
}
