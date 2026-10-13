/* Compile-only candidate. No runtime authority is supplied by this source. */
#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <mpi.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include "status.h"
extern int r07_collective_lease_call(int,int,int);

static int mpi_checked(int code,const char *phase,int rank) {
    if (code == MPI_SUCCESS) return 0;
    fprintf(stderr,"MPI_ERROR phase=%s rank=%d code=%d\n",phase,rank,code);
    fflush(stderr);
    /* MPI_ERRORS_RETURN does not guarantee a usable communicator on failure.
       Do NOT attempt another collective to normalize a transport failure. */
    MPI_Abort(MPI_COMM_WORLD,71);
    return 1;
}

int main(int argc,char **argv) {
    if (argc!=2 || strcmp(argv[1],"--registered-local-collective")) return 90;
    if (!getenv("QE75_JOB_SHA256") || !getenv("QE75_PROFILE_SHA256")) return 91;
    /* A live family-only receipt precedes Init. (-1,0) is an explicit
       non-world-rank sentinel, never evidence of actual rank registration. */
    int preinit=r07_collective_lease_call(-1,0,3);
    if (preinit) {fprintf(stderr,"PREINIT_FAMILY_REFUSAL status=%d\n",preinit);return 92;}
    int provided=0,rank=-1,size=0;
    int code=MPI_Init_thread(&argc,&argv,MPI_THREAD_SINGLE,&provided);
    if (code!=MPI_SUCCESS) {
        /* No world-wide normalization is claimed before MPI_Init succeeds. */
        fprintf(stderr,"MPI_INIT_FAILED code=%d\n",code);return 72;
    }
    if (mpi_checked(MPI_Comm_set_errhandler(MPI_COMM_WORLD,MPI_ERRORS_RETURN),"errors_return",rank)) return 71;
    if (mpi_checked(MPI_Comm_rank(MPI_COMM_WORLD,&rank),"rank",rank) ||
        mpi_checked(MPI_Comm_size(MPI_COMM_WORLD,&size),"size",rank)) return 71;
    if (size!=2 || rank<0 || rank>1 || provided!=MPI_THREAD_SINGLE) {MPI_Abort(MPI_COMM_WORLD,73);return 73;}
    int error=r07_collective_lease_call(rank,size,1);
    for (int i=0;!error && i<100;i++) {
        int check=r07_collective_lease_call(rank,size,2);
        if (!check) break;
        if (check!=EAGAIN || i==99) {error=check;break;}
        struct timespec pause={0,10000000};nanosleep(&pause,NULL);
    }
    if (error) {fprintf(stderr,"LIVE_SCOPE3_REFUSAL rank=%d status=%d\n",rank,error);MPI_Abort(MPI_COMM_WORLD,74);return 74;}
    char name[MPI_MAX_PROCESSOR_NAME]={0};int name_size=0;
    if (mpi_checked(MPI_Get_processor_name(name,&name_size),"node",rank)) return 71;
    struct stat ns;
    if (stat("/proc/self/ns/net",&ns)) {MPI_Abort(MPI_COMM_WORLD,75);return 75;}
    fprintf(stdout,"REGISTERED rank=%d size=%d pid=%ld netns=%llu node=%.*s\n",
            rank,size,(long)getpid(),(unsigned long long)ns.st_ino,name_size,name);fflush(stdout);
    if (mpi_checked(MPI_Barrier(MPI_COMM_WORLD),"barrier",rank)) return 71;
    int local=rank+1,sum=0;
    if (mpi_checked(MPI_Allreduce(&local,&sum,1,MPI_INT,MPI_SUM,MPI_COMM_WORLD),"integer_sum",rank)) return 71;
    int gathered[2]={-1,-1};
    if (mpi_checked(MPI_Allgather(&rank,1,MPI_INT,gathered,1,MPI_INT,MPI_COMM_WORLD),"rank_allgather",rank)) return 71;
    int invalid=(sum!=3 || gathered[0]!=0 || gathered[1]!=1);
    const int statuses[4][2]={{0,0},{INT_MIN,0},{0,-13},{7,0}};
    const int expected[4]={0,1,1,1};
    for (int phase=0;phase<4;phase++) {
        int flag=r07_failed(statuses[phase][rank]),any=-1;
        if (mpi_checked(MPI_Allreduce(&flag,&any,1,MPI_INT,MPI_MAX,MPI_COMM_WORLD),"application_status",rank)) return 71;
        invalid |= any!=expected[phase];
        fprintf(stdout,"STATUS rank=%d phase=%d raw=%d normalized=%d any=%d\n",
                rank,phase,statuses[phase][rank],flag,any);fflush(stdout);
    }
    int flag=r07_failed(invalid),any=0;
    if (mpi_checked(MPI_Allreduce(&flag,&any,1,MPI_INT,MPI_MAX,MPI_COMM_WORLD),"final_status",rank)) return 71;
    fprintf(stdout,"RESULT rank=%d sum=%d ranks=%d,%d invalid=%d\n",rank,sum,gathered[0],gathered[1],any);
    fflush(stdout);
    code=MPI_Finalize();
    if (code!=MPI_SUCCESS) {fprintf(stderr,"MPI_FINALIZE_FAILED code=%d\n",code);return 76;}
    return any ? 77 : 0;
}
