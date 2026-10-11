"""Saved intake provenance and independent guard arithmetic; never launches QE."""
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r07_native_preflight", HERE/"collect_preflight.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def saved():
    return json.loads((HERE/"preflight.json").read_text())


def test_independent_resource_policy_arithmetic_and_real_shortfall():
    record = saved()
    available = Decimal(record["effective_available_memory_bytes"])/Decimal(2)**30
    for name, estimate in (("host", Decimal("21.27")), ("impurity", Decimal("21.32"))):
        expected = Decimal("1.20")*estimate+Decimal(2)
        result = record["ram_gates"][name]
        assert Decimal(result["required_available_GiB_under_guard"]) == expected
        assert available < expected and not result["passed"]
        assert Decimal(result["shortfall_GiB"]) == expected-available
        assert not result["dry_estimate_is_certified_peak"]
        assert module.resource_gate(record["effective_available_memory_bytes"], estimate) == result


def test_byte_boundary_units_and_no_swap_credit():
    threshold = Decimal("27.5240")*Decimal(2)**30
    floor = int(threshold.to_integral_value(rounding=ROUND_FLOOR))
    ceil = int(threshold.to_integral_value(rounding=ROUND_CEILING))
    assert not module.resource_gate(floor, "21.27")["passed"]
    assert module.resource_gate(ceil, "21.27")["passed"]
    # Decimal GB mistaken for GiB would incorrectly relax this guard.
    assert not module.resource_gate(27524000000, "21.27")["passed"]
    assert saved()["policy"]["swap_counted_as_headroom"] is False


def test_recorded_memory_disk_and_cgroup_constraints():
    record = saved()
    memory = record["memory_bytes"]
    assert module.parse_memory("MemTotal: 8 kB\nMemAvailable: 3 kB\nHugePages_Total: 0\n") == {
        "MemTotal": 8192, "MemAvailable": 3072}
    assert record["effective_available_memory_bytes"] <= memory["MemAvailable"] < memory["MemTotal"]
    assert record["swap_used_bytes"] == memory["SwapTotal"]-memory["SwapFree"] > 0
    assert record["disk_bytes"]["free"] > 8*2**30 and record["disk_floor_met"]
    assert not record["full_SCF_disk_demand_certified"]
    for group in record["cgroup_intake"]:
        if isinstance(group.get("memory.max"), int):
            assert record["effective_available_memory_bytes"] <= max(0, group["memory.max"]-group["memory.current"])


def test_approved_stage_gate_does_not_claim_an_execution_or_host_pass():
    record = saved()
    assert record["decision"] == "PREFLIGHT_RESOURCE_NO_GO"
    assert record["host_preflight_passed"] is False
    assert record["QE_invocations"] == [] and record["created_native_output_directories"] == []
    assert record["host_SCF_gate"] == "NOT_RUN"
    assert record["host_projector_irrep_gate"] == "NOT_EVALUABLE_WITHOUT_SCF"
    assert record["impurity_stage"] == "NOT_ADMITTED"
    assert record["physical_xc"] is None and record["full_SCF_peak_RAM_bytes"] is None
    assert record["allowed_cap"]["MPI_ranks"] == 6
    assert record["allowed_cap"]["native_seconds"]+record["allowed_cap"]["grace_seconds"] == 5400
    assert record["allowed_cap"]["substitution_requires_accepted_host_SCF_projector_irrep_exchange"]
    assert record["process_ownership"]["exclusive_MPI_snapshot"]
    assert not record["process_ownership"]["exclusive_MPI_lock_acquired"]


def test_prepared_native_inputs_and_source_provenance_unchanged():
    record = saved()
    assert len(record["source_sha256"]) == 15
    for path, expected in record["source_sha256"].items():
        assert module.digest(path) == expected
    assert module.digest(HERE/"collect_preflight.py") == record["collector_sha256"]
    host, impurity = record["prepared_cases"]["host"], record["prepared_cases"]["impurity"]
    assert host["physics"] == impurity["physics"]
    assert host["physics"]["ecutfock"] == "120.0"
    assert host["physics"]["conv_thr"] == "1e-10"
    assert host["physics"]["nbnd"] == "352" and host["physics"]["nat"] == "16"
    assert all(not case["full_SCF_launched"] and not case["dry_RSS_is_full_SCF_peak"]
               for case in (host, impurity))


def test_existing_dirty_files_and_supervisor_records_not_modified():
    record = saved()
    assert record["DFT_dirty_status_unchanged"] and record["DFT_dirty_status_before"]
    assert record["DFT_dirty_status_before"] == record["DFT_dirty_status_after"]
    assert record["DFT_files_written_by_this_collector"] == []
    assert record["supervisor_states_unchanged"]
    for item in record["supervisor_intake"]:
        assert item["stage"].startswith("FINISHED")
        assert module.digest(item["path"]) == item["sha256"]
    assert not record["process_ownership"]["MPI_families_or_processes"]
    assert not record["process_ownership"]["R07_queue_supervisor_processes"]
