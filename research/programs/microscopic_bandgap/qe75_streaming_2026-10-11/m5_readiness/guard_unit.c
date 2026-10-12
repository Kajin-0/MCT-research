/* Calls only this project's refusal stubs, linked WITHOUT any MPI library. */
#include <stdlib.h>
int MPI_Init(int*,char***);
int PMPI_Init(int*,char***);
int MPI_Init_thread(int*,char***,int,int*);
int PMPI_Init_thread(int*,char***,int,int*);
int main(int argc,char **argv) {
    int which,provided=0;
    if(argc!=2)return 98;
    which=atoi(argv[1]);
    if(which==0)return MPI_Init(&argc,&argv);
    if(which==1)return PMPI_Init(&argc,&argv);
    if(which==2)return MPI_Init_thread(&argc,&argv,0,&provided);
    if(which==3)return PMPI_Init_thread(&argc,&argv,0,&provided);
    return 98;
}
