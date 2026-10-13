/* Serial kernel-lease ABI observation worker, never MPI/PW. */
#include <stdio.h>
#include <stdlib.h>
int qe75_lease_call(int,int,int,int);
int main(int argc,char **argv) {
    int scope=argc==2?atoi(argv[1]):1;
    int code=qe75_lease_call(0,2,1,scope);
    printf("WIRE_RETURN %d\n",code);
    return code==0?0:1;
}
