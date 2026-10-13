"""Small integer budget auditor, not a native execution/admission API."""
from dataclasses import dataclass

I64=(1<<63)-1


class MissingBound(ValueError):pass


def checked(value):
    if type(value) is not int or value<0 or value>I64:raise ValueError('nonnegative signed-64 quantity required')
    return value


def product(a,b):return checked(checked(a)*checked(b))


def resident_mapping_upper_bound(max_tasks,per_process_as,outside_resident):
    """Conditional on hard per-process AS and startup/raise restrictions.

    Every process leader consumes >=1 task; its exact resident mappings
    occupy its virtual address space. Thread accounting is conservatively
    bounded by treating every task as a separate leader. Shared-RSS overcount
    is already included. Kernel/shared-manager costs are separate.
    """
    if max_tasks<=0 or per_process_as<=0:raise ValueError('positive task/AS limits required')
    return checked(product(max_tasks,per_process_as)+checked(outside_resident))


def monitored_rss_upper_bound(max_tasks,per_process_as,outside_resident,accounting_error_bound=None):
    if accounting_error_bound is None:raise MissingBound('reported RSS needs independently bounded accounting/snapshot error')
    return checked(resident_mapping_upper_bound(max_tasks,per_process_as,outside_resident)+checked(accounting_error_bound))


def aggregate_file_upper_bound(per_file_bytes,max_retained_generations,metadata_bytes):
    if max_retained_generations is None:raise MissingBound('closed-file/generation count is indispensable; NOFILE is not that count')
    return checked(product(per_file_bytes,max_retained_generations)+checked(metadata_bytes))


@dataclass(frozen=True)
class Term:
    name:str
    bytes_bound:int|None
    evidence:str


def complete_budget(terms):
    names=[t.name for t in terms]
    if len(set(names))!=len(names):raise ValueError('duplicate budget term')
    missing=[t.name for t in terms if t.bytes_bound is None]
    if missing:raise MissingBound('not a complete producer envelope: '+', '.join(missing))
    total=0
    for t in terms:
        if not t.evidence:raise MissingBound('bound without independent evidence: '+t.name)
        total=checked(total+checked(t.bytes_bound))
    return total


def current_local_mpi_terms():
    # Even the count two is a scoped same-node model, not native observation.
    return [Term('two_default_sm_segments',2*16777216,'installed ompi_info selected default; conditional count2'),
            Term('PRRTE_PMIX_retained_generations',None,'no complete pinned producer/state bound'),
            Term('private_temp_and_shm_path_enforcement',None,'no production local issuer/path certificate'),
            Term('metadata_and_filesystem_overhead',None,'no full producer/inode bound'),
            Term('bounded_capture_and_outside_control',None,'existing tiny owner is not full local MPI owner')]
