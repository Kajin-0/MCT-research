"""Auditable payload/lifetime expressions. UNKNOWN terms are never zero."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'software_2026-10-13'))
from bounds import conservative
from family_runtime import integer,multiply
from resource_guard import add
from binding import Refusal


def total(*values):
    result=0
    for value in values:result=add(result,integer(value))
    return result


def wave_file_payload(global_active,npol,bands):
    # pw_restart_new.gk_l2gmap_kdip compacts to ngk_g; write_wfc receives THAT
    # compact map. igwx is NOT assumed equal to max original density-G label.
    for n in [global_active,npol,bands]:
        if integer(n)<1:raise Refusal('wave payload positive scope')
    return total(multiply(multiply(multiply(16,global_active),npol),bands),multiply(12,global_active))


def density_file_payload(global_G,nspin):
    if integer(global_G)<1 or integer(nspin)<1:raise Refusal('density payload positive scope')
    return total(multiply(multiply(16,global_G),nspin),multiply(12,global_G))


def collected_writer_scratch(global_active,local_npwx,max_density_label,npol,local_G,global_G,kcount):
    for n in [global_active,local_npwx,max_density_label,npol,local_G,global_G,kcount]:
        if integer(n)<1:raise Refusal('writer positive extent')
    # Parent local index arrays + mill_k persist. Mapping helper is a separate
    # phase; two label-sized arrays overlap there; HDF5 gather occurs after it.
    parent=total(multiply(20,local_npwx),multiply(4,kcount))
    mapping=total(multiply(8,max_density_label),multiply(4,global_active))
    wave_gather=max(multiply(12,global_active),multiply(multiply(16,npol),global_active))
    # mill_g is freed BEFORE rho_g/rhoaux. These formulae exclude mergekg/
    # mergewf, MPI and HDF5 internals, all separately UNKNOWN in the ledger.
    return {'wave_parent_array_bytes':parent,'wave_map_phase_bytes':total(parent,mapping),
            'wave_root_gather_phase_bytes':total(parent,wave_gather),
            'wave_selected_peak_bytes':total(parent,max(mapping,wave_gather)),
            'density_selected_root_peak_bytes':max(multiply(12,global_G),total(multiply(16,global_G),multiply(16,local_G))),
            'native_merge_MPI_HDF5_included':False}


def mixing_history(local_smooth_G,nspin,nmix,io_level):
    for n in [local_smooth_G,nspin,nmix,io_level]:integer(n)
    if local_smooth_G<1 or nspin!=4 or not 1<=nmix<=25 or io_level<0:raise Refusal('NC HSE spinor mixing scope')
    record=multiply(multiply(16,local_smooth_G),nspin)
    count=total(2,multiply(2,nmix));store=multiply(record,count)
    # df,dv + rhout_m,rhoin_m + io_buffer. Normal plain mixing; optional
    # local-TF auxiliary arrays need their own ledger entry.
    live=total(multiply(record,total(multiply(2,nmix),3)),multiply(multiply(8,nmix),nmix),multiply(12,nmix))
    return {'record_bytes':record,'max_record_index':count,'history_store_payload_bytes':store,
            'history_RAM_payload_bytes':store if io_level==0 else 0,
            'active_history_disk_logical_bytes':store if io_level>0 else 0,
            # Native close_buffer(keep) dumps RAM records BEFORE freeing them.
            # Both SCF stop paths can keep history. RAM mode is NOT no-output.
            'kept_history_disk_logical_upper_bytes':store,
            'RAM_close_keep_extra_vector_bytes':record if io_level==0 else 0,
            'selected_mix_live_array_bytes':live,'buffer_pointer_metadata_included':False,
            'scope':'plain mixing, NC, nspin4; no meta/XDM/U/PAW/dipole/SIC/RISM/GC-SCF/plugin chunks'}


REQUIRED_DISK=['HDF5_file_format_and_allocation','native_XML_restart_and_PPs','logs_and_errors',
               'all_live_generations_and_aliases','misc_native_scratch','filesystem_metadata_and_quota',
               'new_FFT_packets_and_manifests']
REQUIRED_RSS=['all_PW_live_allocation_phases','solver_ELPA_BLAS_workspace','FFT_plan_and_copy_workspace',
              'MPI_transport_collective_and_plugin_buffers','HDF5_caches_and_conversion_workspace',
              'allocator_fragmentation_thread_stacks_shared_libraries','diagnostic_and_capture_temporaries',
              'guardian_launcher_and_all_descendants']


def require_complete(certificate):
    missing=[k for k in REQUIRED_DISK+REQUIRED_RSS if certificate.get(k) is None]
    if missing:raise Refusal('UNKNOWN envelope terms: '+','.join(missing))
    # A bag of numeric allowances without provenance/phase coverage is not a
    # certificate. No new native authority is implemented by this audit.
    raise Refusal('native completeness/provenance and admission remain unissued')


def report():
    b=conservative();G=b['global_G_box_upper']['wave'];GD=b['global_G_box_upper']['density'];K=8;P=2
    wave=wave_file_payload(G,2,48);density=density_file_payload(GD,4)
    return {'kind':'SOURCE_CONDITIONED_SELECTED_ENVELOPE_NOT_ADMISSION',
            'source_scope':b['scope'],'per_wave_or_ACE_dataset_payload_upper_bytes':wave,
            'one_collected_wave_plus_ACE_generation_dataset_payload_upper_bytes':multiply(2*K,wave),
            'per_density_dataset_payload_upper_bytes':density,
            'added_Miller_dataset_bytes_one_collected_wave_ACE_and_density_generation':total(multiply(2*K*12,G),multiply(12,GD)),
            'collected_writer':collected_writer_scratch(G,G,GD,2,GD,GD,K),
            'fixture_default_io_level_source_derived':0,
            'per_rank_plain_mix_ndim8':mixing_history(GD,4,8,0),
            'two_rank_plain_mix_kept_history_logical_upper_bytes':multiply(P,mixing_history(GD,4,8,0)['kept_history_disk_logical_upper_bytes']),
            'two_rank_default_wave_RAM_record_payload_upper_bytes':multiply(P,multiply(16*2*48*K,G)),
            'known_EXX_and_initial':b,
            'disk_terms_UNKNOWN':REQUIRED_DISK,'RSS_terms_UNKNOWN':REQUIRED_RSS,
            'whole_disk_envelope_certified':False,'whole_RSS_envelope_certified':False,
            'native_MPI_PW_run':False,'native_admission_issued':False}
