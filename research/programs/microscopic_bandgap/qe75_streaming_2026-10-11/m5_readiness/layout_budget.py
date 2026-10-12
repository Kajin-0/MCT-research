"""Exact checked component extents; deliberately no whole-output admission guess."""
from pathlib import Path
import os
from binding import Refusal
from family_runtime import multiply,integer
from resource_guard import add
from process_identity import table


def components(npwx,npw,npol,bands,nkstot,nks,layout_ints,fft_rows,nq):
    values=[npwx,npw,npol,bands,nkstot,nks,layout_ints,fft_rows,nq]
    for value in values:
        if integer(value)<1: raise Refusal('positive actual descriptor required')
    if npw>npwx: raise Refusal('active rows exceed padded basis')
    R=multiply(npwx,npol);B=bands;L=layout_ints
    def total(*terms):
        result=0
        for term in terms: result=add(result,term)
        return result
    packet=total(240,multiply(8,L),multiply(multiply(8,B),nkstot),multiply(multiply(16,B),nks),
                 multiply(multiply(multiply(16,R),B),nks))
    header=total(96,multiply(8,L),multiply(8,npw))
    before=total(header,16,multiply(multiply(8,B),nkstot),multiply(multiply(32,R),B),
                 multiply(multiply(16,B),B),multiply(32,R))
    after=total(header,multiply(multiply(16,R),B),multiply(multiply(16,B),B),multiply(16,R))
    return {'rank_stream_bytes':multiply(multiply(multiply(16,fft_rows),B),nq),
            'rank_state_packet_bytes':packet,'first_ACE_before_per_k_bytes':before,
            'first_ACE_after_per_k_bytes':after,'first_ACE_diagnostics_all_k_bytes':multiply(total(before,after),nks),
            'probe_scratch_bytes':total(multiply(multiply(32,R),B),multiply(16,R)),
            'whole_native_output_envelope_certified':False}


def inventory():
    unknown=[]
    for pid,row in table().items():
        if row['state']=='Z': continue
        try: Path(f'/proc/{pid}/maps').read_text()
        except (FileNotFoundError,ProcessLookupError): continue
        except PermissionError:
            unknown.append({'pid':pid,'start_ticks':row['start_ticks'],
                            'UID':Path(f'/proc/{pid}').stat().st_uid,'reason':'mapping permission denied'})
    return {'complete_global_inventory':not unknown,'unreadable':unknown,
            'native_inventory_gate':'UNKNOWN_REFUSE' if unknown else 'REQUIRES_MPI_CLASSIFICATION',
            'permissions_modified':False}
