/* Serial HDF5 component may load the installed parallel-HDF5 MPI dependency.
   Any attempt to initialize MPI is a hard test failure, never permission. */
#include <unistd.h>
static int refuse(void) {
    static const char text[]="SERIAL_COMPONENT_REFUSED_MPI_INITIALIZATION\n";
    ssize_t written=write(2,text,sizeof(text)-1);
    if(written<0) _exit(97);
    _exit(97);
}
int MPI_Init(int *argc,char ***argv) {(void)argc;(void)argv;return refuse();}
int PMPI_Init(int *argc,char ***argv) {(void)argc;(void)argv;return refuse();}
int MPI_Init_thread(int *argc,char ***argv,int requested,int *provided) {
    (void)argc;(void)argv;(void)requested;(void)provided;return refuse();
}
int PMPI_Init_thread(int *argc,char ***argv,int requested,int *provided) {
    (void)argc;(void)argv;(void)requested;(void)provided;return refuse();
}
