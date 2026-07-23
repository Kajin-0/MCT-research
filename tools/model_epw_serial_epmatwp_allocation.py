"""Static model for the QE 7.6 EPW ``epmatwp`` restart allocation.

This module models array ownership and index bounds only. It never compiles,
patches, imports, or executes Quantum ESPRESSO.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class AllocationModelError(ValueError):
    """Raised when a modeled allocation cannot satisfy the source bounds."""


@dataclass(frozen=True)
class Distribution:
    nrr_g: int
    nmodes: int
    irn_start: int
    irn_stop: int
    irg_start: int
    irg_stop: int
    nirg_loc: int
    nirn_loc: int


@dataclass(frozen=True)
class AllocationShape:
    nbndsub: int
    nrr_k: int
    nmodes: int
    fifth_extent: int

    @property
    def dimensions(self) -> tuple[int, int, int, int, int]:
        return (
            self.nbndsub,
            self.nbndsub,
            self.nrr_k,
            self.nmodes,
            self.fifth_extent,
        )

    @property
    def element_count(self) -> int:
        total = 1
        for extent in self.dimensions:
            total *= extent
        return total


def _positive(name: str, value: int) -> int:
    integer = int(value)
    if integer <= 0:
        raise AllocationModelError(f"{name} must be positive")
    return integer


def derive_distribution(
    *, nrr_g: int, nmodes: int, irn_start: int, irn_stop: int
) -> Distribution:
    """Apply the pinned ``ws_indexes_distribution`` formulas."""

    nrr_g = _positive("nrr_g", nrr_g)
    nmodes = _positive("nmodes", nmodes)
    total = nrr_g * nmodes
    irn_start = int(irn_start)
    irn_stop = int(irn_stop)
    if not (1 <= irn_start <= irn_stop <= total):
        raise AllocationModelError(
            f"invalid combined mode/WS bounds: {irn_start}:{irn_stop} of {total}"
        )
    irg_start = (irn_start - 1) // nmodes + 1
    irg_stop = (irn_stop - 1) // nmodes + 1
    return Distribution(
        nrr_g=nrr_g,
        nmodes=nmodes,
        irn_start=irn_start,
        irn_stop=irn_stop,
        irg_start=irg_start,
        irg_stop=irg_stop,
        nirg_loc=irg_stop - irg_start + 1,
        nirn_loc=irn_stop - irn_start + 1,
    )


def serial_distribution(*, nrr_g: int, nmodes: int) -> Distribution:
    """Return the one-process distribution used by the observed serial run."""

    nrr_g = _positive("nrr_g", nrr_g)
    nmodes = _positive("nmodes", nmodes)
    return derive_distribution(
        nrr_g=nrr_g,
        nmodes=nmodes,
        irn_start=1,
        irn_stop=nrr_g * nmodes,
    )


def allocation_shape(
    *, nbndsub: int, nrr_k: int, distribution: Distribution
) -> AllocationShape:
    return AllocationShape(
        nbndsub=_positive("nbndsub", nbndsub),
        nrr_k=_positive("nrr_k", nrr_k),
        nmodes=distribution.nmodes,
        fifth_extent=distribution.nirg_loc,
    )


def local_index_pairs(distribution: Distribution) -> list[tuple[int, int, int]]:
    """Return ``(global_ir_g, imode, local_ir_g)`` used by the Wigner loop."""

    values: list[tuple[int, int, int]] = []
    for irn in range(distribution.irn_start, distribution.irn_stop + 1):
        global_ir_g = (irn - 1) // distribution.nmodes + 1
        imode = (irn - 1) % distribution.nmodes + 1
        local_ir_g = global_ir_g - distribution.irg_start + 1
        values.append((global_ir_g, imode, local_ir_g))
    return values


def assert_all_local_indices_fit(
    distribution: Distribution, shape: AllocationShape
) -> None:
    if shape.nmodes != distribution.nmodes:
        raise AllocationModelError("mode extent differs from the distribution")
    for global_ir_g, imode, local_ir_g in local_index_pairs(distribution):
        if not (1 <= global_ir_g <= distribution.nrr_g):
            raise AllocationModelError("global WS index exceeds nrr_g")
        if not (1 <= imode <= shape.nmodes):
            raise AllocationModelError("mode index exceeds the fourth extent")
        if not (1 <= local_ir_g <= shape.fifth_extent):
            raise AllocationModelError(
                f"local WS index {local_ir_g} exceeds fifth extent {shape.fifth_extent}"
            )


def assert_serial_direct_read_fits(
    distribution: Distribution, shape: AllocationShape
) -> None:
    """Check the serial ``irg=1..nrr_g`` direct-read loop."""

    if distribution.irn_start != 1:
        raise AllocationModelError("serial distribution must start at one")
    if distribution.irn_stop != distribution.nrr_g * distribution.nmodes:
        raise AllocationModelError("serial distribution must cover the full combined range")
    if distribution.nirg_loc != distribution.nrr_g:
        raise AllocationModelError("serial nirg_loc must equal nrr_g")
    if shape.fifth_extent < distribution.nrr_g:
        raise AllocationModelError(
            "serial direct-read loop exceeds the allocated fifth dimension"
        )
    assert_all_local_indices_fit(distribution, shape)


def count_allocations(events: Iterable[str]) -> int:
    return sum(event == "allocate_epmatwp" for event in events)


def assert_exactly_one_allocation(events: Iterable[str]) -> None:
    count = count_allocations(events)
    if count != 1:
        raise AllocationModelError(f"expected one epmatwp allocation, observed {count}")


def modeled_paths() -> dict[str, list[str]]:
    """Represent allocation events in the pinned and proposed control flows."""

    return {
        "normal_preparation": ["allocate_epmatwp", "fill_epmatwp", "write_epmatwp"],
        "restart_mpi_pinned": ["allocate_epmatwp", "read_epmatwp", "divide_ndegen"],
        "restart_serial_pinned": ["read_epmatwp", "divide_ndegen"],
        "restart_mpi_proposed": ["allocate_epmatwp", "read_epmatwp", "divide_ndegen"],
        "restart_serial_proposed": ["allocate_epmatwp", "read_epmatwp", "divide_ndegen"],
    }


def diagnose_path(events: Iterable[str]) -> str:
    events = list(events)
    allocation_count = count_allocations(events)
    if allocation_count == 0 and any(
        event in {"read_epmatwp", "divide_ndegen"} for event in events
    ):
        return "MISSING_ALLOCATION"
    if allocation_count > 1:
        return "DOUBLE_ALLOCATION"
    return "ALLOCATION_LIFETIME_VALID"


def explicit_dummy_extent_risk(
    *, global_nrr_g: int, actual_fifth_extent: int
) -> bool:
    """Flag the separate MPI explicit-dummy extent mismatch risk."""

    return int(actual_fifth_extent) < int(global_nrr_g)
