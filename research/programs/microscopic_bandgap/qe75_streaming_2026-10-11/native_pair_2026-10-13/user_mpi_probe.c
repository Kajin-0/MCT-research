#include <mpi.h>
#include <stdio.h>
#include <unistd.h>
int main(int argc, char **argv) {
    int provided=0,rank=-1,n=0;
    if (MPI_Init_thread(&argc,&argv,MPI_THREAD_SINGLE,&provided)!=MPI_SUCCESS) return 11;
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&n);
    int mine=rank+1,sum=-1,gather[2]={-1,-1},err=0;
    if (n!=2 || provided!=MPI_THREAD_SINGLE) err=1;
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Allreduce(&mine,&sum,1,MPI_INT,MPI_SUM,MPI_COMM_WORLD);
    MPI_Allgather(&rank,1,MPI_INT,gather,1,MPI_INT,MPI_COMM_WORLD);
    if(sum!=3||gather[0]!=0||gather[1]!=1)err=1;
    int total=0;MPI_Allreduce(&err,&total,1,MPI_INT,MPI_MAX,MPI_COMM_WORLD);
    char proc[MPI_MAX_PROCESSOR_NAME]={0};int len=0;MPI_Get_processor_name(proc,&len);
    printf("NATIVE_MPI rank=%d/%d pid=%ld node=%s sum=%d gathered=%d,%d invalid=%d\\n",rank,n,(long)getpid(),proc,sum,gather[0],gather[1],total);
    fflush(stdout);MPI_Finalize();return total?12:0;
}
