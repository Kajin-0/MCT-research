/* GPL-2.0-or-later. Gate A NON_SCIENCE; no QE, PP or numerical arrays. */
#define _GNU_SOURCE
#include <mpi.h>
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
extern int r07_static_lease(int,int,int,int64_t);

static unsigned long long ticks(void) {
    char line[4096],*p,*save; FILE *f=fopen("/proc/self/stat","re"); int i=0;
    if(!f)return 0;
    if(!fgets(line,sizeof line,f)){fclose(f);return 0;} fclose(f);
    p=strrchr(line,')'); if(!p)return 0;
    for(p=strtok_r(p+1," ",&save);p;p=strtok_r(NULL," ",&save),i++)
        if(i==19)return strtoull(p,NULL,10);
    return 0;
}
static int normalize(int e) {
    int result=0; if(e<0)e=EIO;
    if(MPI_Allreduce(&e,&result,1,MPI_INT,MPI_MAX,MPI_COMM_WORLD)!=MPI_SUCCESS)
        MPI_Abort(MPI_COMM_WORLD,91);
    return result;
}
int main(int argc,char **argv) {
    int rank=-1,size=0,sum=0,gather[2]={-1,-1},code=0,provided;
    if(MPI_Init_thread(&argc,&argv,MPI_THREAD_SINGLE,&provided)!=MPI_SUCCESS)return 90;
    MPI_Comm_set_errhandler(MPI_COMM_WORLD,MPI_ERRORS_RETURN);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);MPI_Comm_size(MPI_COMM_WORLD,&size);
    if(argc!=3||size!=2||provided!=MPI_THREAD_SINGLE||
       (strcmp(argv[2],"positive")&&strcmp(argv[2],"missing_final"))) MPI_Abort(MPI_COMM_WORLD,92);
    code=normalize(r07_static_lease(rank,size,1,0));
    if(code){MPI_Finalize();return code;}
    /* A bounded live interval lets the real owner sample both rank FD trees. */
    usleep(300000);
    int value=rank+1;
    code=normalize(MPI_Barrier(MPI_COMM_WORLD)!=MPI_SUCCESS);
    if(!code)code=normalize(MPI_Allreduce(&value,&sum,1,MPI_INT,MPI_SUM,MPI_COMM_WORLD)!=MPI_SUCCESS);
    if(!code)code=normalize(MPI_Allgather(&rank,1,MPI_INT,gather,1,MPI_INT,MPI_COMM_WORLD)!=MPI_SUCCESS);
    if(sum!=3||gather[0]!=0||gather[1]!=1)code=93;
    code=normalize(code);
    char cg[1024],packet[3072],path[2048]; int extent=0;
    FILE *f=fopen("/proc/self/cgroup","re");
    if(!f||!fgets(cg,sizeof cg,f))code=94;
    if(f)fclose(f);
    if(!code) {
        cg[strcspn(cg,"\n")]=0;
        if(strncmp(cg,"0::/",4))code=94;
    }
    const char *inv=getenv("INVOCATION_ID"),*job=getenv("R07_LIFECYCLE_JOB"),
        *profile=getenv("R07_LIFECYCLE_PROFILE"),*nonce=getenv("R07_LIFECYCLE_NONCE");
    if(!inv||!job||!profile||!nonce)code=94;
    if(!code) {
        extent=snprintf(packet,sizeof packet,
            "{\"kind\":\"R07_MPI_LIFECYCLE_NON_SCIENCE_V1\",\"scope\":1601,"
            "\"rank\":%d,\"size\":%d,\"pid\":%d,\"uid\":%d,\"start_ticks\":%llu,"
            "\"invocation\":\"%s\",\"job\":\"%s\",\"profile\":\"%s\",\"nonce\":\"%s\","
            "\"cgroup\":\"%s\",\"sum\":%d,\"gather\":[%d,%d],\"collective_error\":%d}\n",
            rank,size,(int)getpid(),(int)getuid(),ticks(),inv,job,profile,nonce,cg+3,sum,gather[0],gather[1],code);
        int n=snprintf(path,sizeof path,"%s/pilot/H.rank%d",argv[1],rank);
        if(extent<=0||extent>=(int)sizeof packet||n<=0||n>=(int)sizeof path)code=95;
        else {
            int fd=open(path,O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC,0600);
            if(fd<0)code=96;
            else {if(write(fd,packet,extent)!=extent||fsync(fd))code=96;if(close(fd))code=96;}
        }
    }
    code=normalize(code);
    if(code){MPI_Finalize();return code;}
    code=normalize(MPI_Barrier(MPI_COMM_WORLD)!=MPI_SUCCESS);
    /* Negative case is separately frozen. Rank1 omits its final, not a retry. */
    if(!code)code=(!strcmp(argv[2],"missing_final")&&rank==1)?88:r07_static_lease(rank,size,10,extent);
    code=normalize(code);
    if(!code) {
        usleep(200000);
        if(rank==0){puts("R07_LIFECYCLE_NON_SCIENCE_COMPLETE");fflush(stdout);}
    }
    int finalcode=normalize(MPI_Barrier(MPI_COMM_WORLD)!=MPI_SUCCESS);
    if(MPI_Finalize()!=MPI_SUCCESS)return 97;
    return code?code:finalcode;
}
