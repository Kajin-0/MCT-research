#ifndef R07_LOCAL_STATUS_H
#define R07_LOCAL_STATUS_H
/* Normalize BEFORE MPI_MAX; INT_MIN is failure, never take abs(status). */
static inline int r07_failed(int status) { return status != 0; }
#endif
