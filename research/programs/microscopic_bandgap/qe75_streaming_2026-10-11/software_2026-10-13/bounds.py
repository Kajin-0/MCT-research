"""Source-conditioned finite bounds. Unknown whole-native budget stays refused."""
from decimal import Decimal,localcontext
from fractions import Fraction
import itertools
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'m5_readiness'))
from layout_budget import components
from family_runtime import integer,multiply
from resource_guard import add,round_blocks
from binding import Refusal


def good_order(n,factor=1):
    integer(n);integer(factor)
    if n<1 or factor<1 or factor>n:raise Refusal('FFT order/factor domain')
    for m in range(n,16386):
        p=m
        for prime in [2,3,5]:
            while p%prime==0:p//=prime
        if p==1 and m%factor==0:return m
    raise Refusal('QE FFT maximum exceeded')


def conservative():
    # The pinned primitive cell is half the 6.46-Angstrom cubic cell. Outward
    # decimal intervals contain QE's CODATA constant and native roundoff with
    # ample margin; no near-boundary index is rounded down on a float guess.
    with localcontext() as ctx:
        ctx.prec=50
        a_hi=Decimal('6.460000000001')/Decimal('0.5291772108')
        a_lo=Decimal('6.459999999999')/Decimal('0.5291772110')
        pi_lo=Decimal('3.14159265358');pi_hi=Decimal('3.14159265360')
        primitive_norm_hi=a_hi/Decimal(2).sqrt()
        k_hi=2*pi_hi/a_lo
        wave_radius=(Decimal(90).sqrt()+k_hi)
        if wave_radius**2>=120:raise Refusal('Fock cutoff no longer dominates enlarged wave radius')
        n_wave=int(wave_radius*primitive_norm_hi/(2*pi_lo))
        n_fock=int(Decimal(120).sqrt()*primitive_norm_hi/(2*pi_lo))
        n_dense=int(Decimal(360).sqrt()*primitive_norm_hi/(2*pi_lo))
    # grid_set returns 2*max_Miller+1; good order cannot exceed this 2/3/5
    # padding result under the CPU symmorphic fixture's fft_fact=1 (or 2).
    fock_order=good_order(2*n_fock+1);dense_order=good_order(2*n_dense+1)
    G=(2*n_wave+1)**3;GF=(2*n_fock+1)**3;GD=(2*n_dense+1)**3
    VF=fock_order**3;VD=dense_order**3;P=2;B=48;K=8;Q=8
    # fft_type_set has four maxima; each is <=P*V even without assuming
    # equal sticks/slabs or silently substituting V/P for the local workspace.
    fft_rows=P*VF*2;density_rows=P*VD
    L=256+K*G+5*GF+K*Q+5*Q+4*K
    c=components(G,G,2,B,K,K,L,fft_rows,Q)
    LI=19+5*GD
    initial=208+8*LI+24*G+16*G*2*B+16*B*K+16*density_rows*4+16*GD*4
    return {'kind':'CONSERVATIVE_COMPONENT_BOUND_NOT_NATIVE_ADMISSION',
            'Miller_bounds':{'wave':n_wave,'fock':n_fock,'density':n_dense},
            'global_FFT_order_upper':{'fock':fock_order,'density':dense_order},
            'global_G_box_upper':{'wave':G,'fock':GF,'density':GD},
            'per_rank_fft_rows_including_spin_upper':fft_rows,'per_rank_density_rows_upper':density_rows,
            'per_rank_npwx_upper':G,'world_ranks':P,'bands':B,'k_upper':K,'stored_q_upper':Q,
            'diagnostic_layout_ints_upper':L,'initial_layout_ints_upper':LI,
            'per_rank_initial_packet_upper_bytes':initial,'initial_packet_guard_bytes':128*(1<<20),
            'per_rank_components_upper_bytes':c,
            'two_rank_full_q_store_upper_bytes':2*c['rank_stream_bytes'],
            'two_rank_one_q_plane_resident_upper_bytes':2*c['rank_stream_bytes']//Q,
            'two_rank_initial_all_k_upper_bytes':2*K*initial,
            'collected_wave_and_ACE_payload_upper_bytes':2*16*2*G*B*K,
            'collected_density_payload_upper_bytes':16*GD*4,
            'whole_native_output_envelope_certified':False,'whole_family_RSS_certified':False,
            'actual_native_MPI_descriptor':'UNKNOWN',
            'unbounded_or_unqualified':['HDF5 metadata/allocation and temporary replacement lifetime',
                'all XML/log/mix/native files and maximum live generations',
                'allocator/FFT/MPI/backend workspaces and page cache',
                'actual FFT factors, ownership/G maps and native q selection'],
            'scope':'exact pinned 2-atom CPU NC SOC geometry/cutoffs, one pool/group, symmorphic fft_fact<=2; source conditions must be checked'}


def exact_initial_extent(h):
    if len(h)!=13:raise Refusal('initial header length')
    _,_,_,r,n,p,b,k,nr,ns,ng,L,_=h
    value=208
    for term in [multiply(8,L),multiply(24,n),multiply(multiply(multiply(16,r),p),b),
                 multiply(multiply(16,b),k),multiply(multiply(16,nr),ns),multiply(multiply(16,ng),ns)]:
        value=add(value,term)
    return value


def live_inode_budget(objects,phases,block=4096):
    """Count one physical allocation for every live owned inode class.

    File aliases never create extra data copies; different generation/inode
    classes do. Actual metadata/quota/backend blocks remain separate inputs.
    """
    allocated={name:round_blocks(integer(size),block) for name,size in objects.items()}
    totals=[]
    for phase in phases:
        if not set(phase)<=set(objects):raise Refusal('unregistered live inode')
        value=0
        for name in set(phase):value=add(value,allocated[name])
        totals.append(value)
    return {'per_phase_allocated_payload_blocks':totals,'peak_payload_blocks':max(totals,default=0),
            'metadata_and_unknown_files_included':False}


def admit_native_envelope(descriptor,extras):
    if descriptor.get('actual_native_MPI_descriptor')=='UNKNOWN':raise Refusal('native descriptor UNKNOWN')
    if any(extras.get(key) is None for key in ['HDF5_blocks','XML_logs_mix_blocks','live_generations','RAM_backend_peak']):
        raise Refusal('complete native envelope missing independent bounds')
    raise Refusal('no issued native admission path in component bounds')
