#!/usr/bin/env python3
"""Read-only EXX 7.5 buffer arithmetic and committed telemetry checks. No QE."""
from pathlib import Path
import json
GIB=1024**3
GRID=(64,64,64)
BANDS=352
SPINOR=2
QPOINTS=8
C128_BYTES=16
HERE=Path(__file__).resolve().parent
def nominal_exxbuff_bytes(nx=64,ny=64,nz=64,npol=2,nbands=352,nq=8):
    return nx*ny*nz*npol*nbands*nq*C128_BYTES
def nominal_decomposition(ranks,groups):
    """Idealized count; NOT a prediction of QE physical/private memory."""
    assert ranks%groups==0 and groups>=1
    per_group=ranks//groups
    bands=(BANDS+groups-1)//groups
    total=ranks*((64**3/per_group)*SPINOR*bands*QPOINTS*C128_BYTES)
    return {"ranks":ranks,"groups":groups,"bands_ceiling_per_group":bands,
            "nominal_aggregate_GiB":round(total/GIB,6),
            "nominal_per_rank_GiB":round(total/ranks/GIB,6)}
def check_saved_data():
    rows=[json.loads(x) for x in (HERE/"host_telemetry.jsonl").read_text().splitlines()]
    result=json.loads((HERE/"host_result.json").read_text())
    assert len(rows)==354
    assert result["mpi_ranks"]==6 and result["accepted_scf"] is False
    assert result["exx_converged"] is False and result["job_done"] is False
    assert result["measured_peak_process_family_RSS_bytes"]>=max(r["RSS_bytes"] for r in rows)
    assert min(r["available_RAM_bytes"] for r in rows)==result["minimum_sampled_available_RAM_bytes"]
    assert max(r["RSS_bytes"] for r in rows)>result["process_family_RSS_limit_bytes"]
    return rows,result
if __name__=="__main__":
    rows,result=check_saved_data()
    print(json.dumps({"nominal_buffer_GiB":nominal_exxbuff_bytes()/GIB,
       "decomposition_models":[nominal_decomposition(6,i) for i in (1,2,3,6)],
       "samples":len(rows), "observed_RSS_peak_GiB":result["measured_peak_process_family_RSS_bytes"]/GIB,
       "observed_min_available_GiB":result["minimum_sampled_available_RAM_bytes"]/GIB},
       indent=2))
