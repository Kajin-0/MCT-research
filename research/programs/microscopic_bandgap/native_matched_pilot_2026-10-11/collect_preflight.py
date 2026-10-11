"""Read-only preflight for one user-approved native pair; never launches QE.

Output is confined to this MCT result directory. Prepared DFT decks, native
data, dirty files, pseudopotentials and supervisor states are read-only.
The guard margin is an engineering policy, not an estimated material result.
"""
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
DFT = Path("/home/User/opencode_workspace/DFT")
PAIR = DFT/"calculations/r07/cd_in_hg_pair_n2_k2_q2_e90_f120_prepare"
GIB = 1024**3
POLICY = {"ram_estimate_margin_fraction": "0.20", "system_ram_reserve_GiB": "2",
          "disk_free_floor_GiB": "8", "swap_counted_as_headroom": False,
          "policy_scope": "launch guard only; no measured full-SCF peak or certified upper bound"}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(262144), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*arguments):
    return subprocess.check_output(["git", *arguments], cwd=DFT, text=True).strip()


def parse_memory(text):
    return {key: int(value)*1024 for key, value in
            re.findall(r"^(\w+):\s+(\d+) kB$", text, re.M)}


def cgroup_limits():
    paths = []
    line = next((v for v in Path("/proc/self/cgroup").read_text().splitlines()
                 if v.startswith("0::")), None)
    if line is None:
        return paths
    root = Path("/sys/fs/cgroup")
    current = root/line.split("::", 1)[1].lstrip("/")
    while current.is_relative_to(root):
        fields = {"path": str(current)}
        for name in ("memory.max", "memory.current", "memory.swap.max", "memory.swap.current"):
            path = current/name
            if path.exists():
                value = path.read_text().strip()
                fields[name] = value if value == "max" else int(value)
        if len(fields) > 1:
            paths.append(fields)
        if current == root:
            break
        current = current.parent
    return paths


def process_ownership():
    mpi = []
    queues = []
    names = {"pw.x", "mpirun", "mpiexec", "prterun", "orted", "prted"}
    for path in Path("/proc").iterdir():
        if not path.name.isdigit():
            continue
        try:
            comm = (path/"comm").read_text().strip()
            argv = [v.decode(errors="replace") for v in (path/"cmdline").read_bytes().split(b"\0") if v]
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            continue
        executables = {Path(v).name for v in argv[:2]}
        if comm in names or names.intersection(executables):
            mpi.append({"pid": int(path.name), "comm": comm, "argv": argv})
        # Actual Python/shell driver argument only, never prose in a Codex prompt
        # and never kernel workqueue thread names.
        if argv and Path(argv[0]).name in {"python", "python3", "bash", "sh"}:
            driver = Path(argv[1]).name if len(argv) > 1 else ""
            if driver.startswith("r07_") and any(v in driver for v in ("queue", "followthrough", "supervisor")):
                queues.append({"pid": int(path.name), "comm": comm, "argv": argv})
    return {"MPI_families_or_processes": mpi, "R07_queue_supervisor_processes": queues,
            "exclusive_MPI_snapshot": not mpi and not queues,
            "exclusive_MPI_lock_acquired": False}


def resource_gate(available_bytes, estimated_gib):
    estimate = Decimal(str(estimated_gib))
    required = estimate*(1+Decimal(POLICY["ram_estimate_margin_fraction"]))+Decimal(POLICY["system_ram_reserve_GiB"])
    available = Decimal(available_bytes)/GIB
    return {"available_GiB": str(available), "QE_dry_estimate_GiB": str(estimate),
            "required_available_GiB_under_guard": str(required),
            "shortfall_GiB": str(max(Decimal(0), required-available)),
            "dry_estimate_is_certified_peak": False, "passed": available >= required}


def collect():
    status_before = git("status", "--porcelain=v1", "--untracked-files=normal")
    preparation = json.loads((PAIR/"preparation.json").read_text())
    supervisor_paths = [DFT/"calculations/r07/fock_followthrough_5eed5ea4/state.json",
                        DFT/"calculations/r07/reference_queue_5eed5ea4_recovered/state.json"]
    supervisor_hashes = {str(p): digest(p) for p in supervisor_paths}
    supervisors = []
    for path in supervisor_paths:
        data = json.loads(path.read_text())
        owner = data.get("owner_pid")
        supervisors.append({"path": str(path), "sha256": supervisor_hashes[str(path)],
                            "stage": data.get("stage"), "owner_pid": owner,
                            "owner_pid_present": Path(f"/proc/{owner}").exists() if owner else None})
    source_hashes = {str(DFT/"AGENTS.md"): digest(DFT/"AGENTS.md"),
                     str(PAIR/"preparation.json"): digest(PAIR/"preparation.json")}
    cases = {}
    for member in ("host", "impurity"):
        folder = PAIR/member
        for filename in ("pw.in", "pw_dry.in", "pw_dry.out", "pw_dry_result.json", "pw_dry_provenance.json"):
            source_hashes[str(folder/filename)] = digest(folder/filename)
        dry = json.loads((folder/"pw_dry_result.json").read_text())
        text = (folder/"pw.in").read_text()
        expected = preparation["inputs_sha256"][member]
        assert digest(folder/"pw.in") == expected["pw.in"]
        assert digest(folder/"pw_dry.in") == expected["pw_dry.in"]
        assert dry["input_sha256"] == expected["pw_dry.in"]
        assert dry["pp_sha256"] == preparation["pp_sha256"]
        assert dry["accepted_native_dry_run"] and not dry["accepted_scf"]
        assert dry["mpi_ranks"] == 6 and not dry["full_SCF_peak_memory_measured"]
        assert re.search(r"input_dft\s*=\s*'HSE'", text)
        physical = {}
        for name in ("nat", "nbnd", "ecutwfc", "ecutrho", "ecutfock", "nqx1", "nqx2", "nqx3", "conv_thr", "degauss", "exx_fraction", "screening_parameter"):
            physical[name] = re.search(rf"\b{name}\s*=\s*([^\n,]+)", text).group(1).strip()
        for name in ("noncolin", "lspinorb", "diago_full_acc"):
            assert re.search(rf"\b{name}\s*=\s*\.true\.", text)
        assert "2 2 2  0 0 0" in text
        cases[member] = {"input_sha256": expected["pw.in"], "physics": physical,
                         "previous_QE_version_line": dry["actual_QE_version_line"],
                         "dry_estimate_GiB": dry["estimated_total_dynamical_RAM_QE_GB"],
                         "dry_peak_RSS_bytes": dry["measured_peak_process_family_RSS_bytes"],
                         "dry_RSS_is_full_SCF_peak": False, "full_SCF_launched": False}
    assert cases["host"]["physics"] == cases["impurity"]["physics"]
    for element, expected in preparation["pp_sha256"].items():
        path = DFT/f"pseudopotentials/{element}_sg15_pbe_fr_v12.UPF"
        assert digest(path) == expected
        source_hashes[str(path)] = expected
    memory = parse_memory(Path("/proc/meminfo").read_text())
    groups = cgroup_limits()
    available = memory["MemAvailable"]
    for g in groups:
        if isinstance(g.get("memory.max"), int) and isinstance(g.get("memory.current"), int):
            available = min(available, max(0, g["memory.max"]-g["memory.current"]))
    disk = shutil.disk_usage(DFT)
    ownership = process_ownership()
    ram = {name: resource_gate(available, case["dry_estimate_GiB"]) for name, case in cases.items()}
    host_passes = ram["host"]["passed"] and ownership["exclusive_MPI_snapshot"] and disk.free >= int(POLICY["disk_free_floor_GiB"])*GIB
    status_after = git("status", "--porcelain=v1", "--untracked-files=normal")
    states_unchanged = all(digest(p) == supervisor_hashes[str(p)] for p in supervisor_paths)
    assert status_before == status_after and states_unchanged
    for path, expected in source_hashes.items():
        assert digest(path) == expected
    return {"written_utc": datetime.now(timezone.utc).isoformat(),
            "claim_status": "CALCULATED measured intake; engineering launch guard, no native SCF result",
            "authorization": "one staged host then conditional Cd pilot; user explicit approval; old goal unchanged",
            "DFT_git_commit": git("rev-parse", "HEAD"),
            "DFT_branch": git("branch", "--show-current"), "DFT_dirty_status_before": status_before,
            "DFT_dirty_status_after": status_after, "DFT_dirty_status_unchanged": status_before == status_after,
            "DFT_files_written_by_this_collector": [], "source_sha256": source_hashes,
            "supervisor_intake": supervisors, "supervisor_states_unchanged": states_unchanged,
            "process_ownership": ownership, "memory_bytes": memory, "cgroup_intake": groups,
            "effective_available_memory_bytes": available,
            "swap_used_bytes": memory["SwapTotal"]-memory["SwapFree"],
            "disk_bytes": {"total": disk.total, "used": disk.used, "free": disk.free},
            "disk_floor_met": disk.free >= int(POLICY["disk_free_floor_GiB"])*GIB,
            "full_SCF_disk_demand_certified": False, "policy": POLICY,
            "ram_gates": ram, "prepared_cases": cases,
            "allowed_cap": {"MPI_ranks": 6, "sequential_families": 1, "native_seconds": 3600, "grace_seconds": 1800,
                            "substitution_requires_accepted_host_SCF_projector_irrep_exchange": True},
            "host_preflight_passed": host_passes,
            "decision": "PREFLIGHT_RESOURCE_NO_GO" if not host_passes else "PREFLIGHT_GUARD_PASSED_NOT_A_RUN_AUTHORIZER",
            "QE_invocations": [], "created_native_output_directories": [],
            "host_SCF_gate": "NOT_RUN", "host_projector_irrep_gate": "NOT_EVALUABLE_WITHOUT_SCF",
            "impurity_stage": "NOT_ADMITTED", "full_SCF_peak_RAM_bytes": None, "physical_xc": None,
            "collector_sha256": digest(Path(__file__))}


if __name__ == "__main__":
    output = HERE/"preflight.json"
    if output.exists():
        raise FileExistsError("never overwrite a pilot intake result")
    record = collect()
    output.write_text(json.dumps(record, indent=2, sort_keys=True)+"\n")
    print(json.dumps({name: record[name] for name in ("written_utc", "decision", "ram_gates", "disk_bytes", "process_ownership", "supervisor_states_unchanged")}, indent=2))
