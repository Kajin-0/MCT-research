/* GPL-2.0-or-later. Serial wire client test only; never calls MPI. */
#include <stdlib.h>
#include <stdio.h>
int qe75_lease_call(int, int, int, int);
int main(int argc, char **argv) {
    if (argc != 3) return 100;
    int stage = atoi(argv[1]), scope = atoi(argv[2]);
    int rc = qe75_lease_call(0, 2, stage, scope);
    printf("SERIAL_WIRE_NOT_MPI status=%d stage=%d scope=%d\n", rc, stage, scope);
    return rc ? 1 : 0;
}
