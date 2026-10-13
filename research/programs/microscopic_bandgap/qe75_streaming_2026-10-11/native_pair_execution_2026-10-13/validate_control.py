"""Qualify the completed control from native evidence, never a saved Boolean.

Original RESULT remains failed. Only the witnessed post-completion smaps ESRCH
race is classified as benign; all other monitor failures refuse stream.
Raw control samples were lost to legacy MAX_META: disclose, don't reconstruct.
"""
import hashlib,json,re
from pathlib import Path

def validate(root,owner):
    root=Path(root);r=json.loads((root/'RESULT.json').read_text());job=json.loads((root/'JOB.json').read_text());profile=json.loads((root/'PROFILE.json').read_text())
    reason=r['reason']
    if not re.fullmatch(r"\[Errno 3\] No such process: '/proc/[0-9]+/smaps_rollup'",reason):
        raise owner.Refusal('control failure is not the witnessed post-completion ESRCH')
    terminal=r['manager_terminal'];text=(root/'pw.out').read_text()
    if not (r['owned_cgroup_empty'] and terminal['Result']=='exit-code' and terminal['ExecMainStatus']=='1'
            and 'first ACE captured; intentional fixture stop, not SCF' in text):raise owner.Refusal('control native stop/cleanup unproven')
    if owner.show(r['unit'])['LoadState']!='not-found':raise owner.Refusal('control unit not collected')
    if not (r['elapsed_seconds']<=600 and r['peak_family_RSS_bytes']<=owner.MEMORY
            and r['minimum_MemAvailable_bytes']>=4*owner.GIB and r['minimum_free_disk_bytes']>=10*owner.GIB):
        raise owner.Refusal('control measured resource cap/floors failed')
    for k in ['max','oom','oom_kill']:
        if r['final_kernel']['memory_events'][k]:raise owner.Refusal('control memory event')
    if r['final_kernel']['pids_events'].get('max'):raise owner.Refusal('control task event')
    if owner.sha(job['command'][6])!=profile['binary_sha256'] or owner.sha(root/'pw.in')!=profile['input_sha256']:
        raise owner.Refusal('control ELF/deck changed')
    if owner.digest(profile)!=job['profile_sha256']:raise owner.Refusal('control PROFILE/JOB')
    ranks={h['rank']:h['pid'] for h in r['real_rank_receipts'] if h['action']==1}
    if set(ranks)!={0,1} or len(set(ranks.values()))!=2:raise owner.Refusal('control actual rank registration incomplete')
    for stage in [4,5,6]:
        rows=[h for h in r['real_rank_receipts'] if h['action']==stage]
        if {h['rank'] for h in rows}!={0,1} or len(rows)!=2:raise owner.Refusal('control phase incomplete')
        for h in rows:
            if (h['pid']!=ranks[h['rank']] or h['invocation']!=r['invocation']
                or h['job_sha256']!=owner.digest(job) or h['profile_sha256']!=owner.digest(profile)):
                raise owner.Refusal('control live typed receipt binding')
    retired_pid=int(re.search(r'/proc/([0-9]+)/',reason).group(1))
    if retired_pid not in ranks.values():raise owner.Refusal('ESRCH not a completed native rank')
    initial=owner.all_rank_certificate(owner.initial_paths(root),owner.initial_paths(root),profile['common_input_sha256'],[1,2,3])
    fft=owner.fft_compare([root/'fft'/f'rank{r}.fft' for r in [0,1]], [root/'fft'/f'rank{r}.fft' for r in [0,1]],
        dict(stock=owner.digest(profile),stream=owner.digest(profile)),profile['common_input_sha256'])
    action=owner.action_compare(owner.action_paths(root),owner.action_paths(root),[1,2,3])
    files={str(f.relative_to(root)):owner.sha(f) for sub in ['initial','fft','diag'] for f in (root/sub).iterdir()}
    files.update({n:owner.sha(root/n) for n in ['RESULT.json','JOB.json','PROFILE.json','pw.in','pw.out','KERNEL_ADMISSION.json']})
    return dict(accepted_completed_numerical_control=True,original_guard_result_retained_failed=True,
        reason='two authenticated phase6 completions + exact intentional stop + empty group; post-completion smaps ESRCH',
        control_root=str(root),input_SHA=profile['common_input_sha256'],provenance_files_sha256=files,
        initial=initial,fft=fft,action=action,raw_control_telemetry_unavailable=True,
        original_guarded_resource_summary=r,continuous_resource_guarantee=False,SCF_converged=False)
