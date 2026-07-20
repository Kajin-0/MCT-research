"""Source-bound Yue et al. 2006 absorption-edge helper.

The paper uses this critical absorption coefficient for thick bulk specimens.
It is an observation operator inside the source domain, not a band-gap or
composition law and not the operator used for the thin MBE specimens.
"""
from __future__ import annotations

import math

SOURCE_DOI = "10.1063/1.2221411"
SOURCE_RECORD_FINGERPRINT_SHA256 = (
    "65c2fa758df7ca6881e44ef3263b603511d84adee06ca0f5c7b0ae4861f23a34"
)
COMPOSITION_RANGE = (0.232, 0.337)
TEMPERATURE_RANGE_K = (11.0, 300.0)


def _finite(value: float, *, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def bulk_critical_absorption_cm1(composition_x: float, temperature_k: float) -> float:
    """Return source Eq. (1), the bulk critical absorption coefficient.

    ``alpha_Eg = -65 + 1.88*T + (8694 - 10.31*T)*x``

    The source uses the resulting coefficient as an extrapolation target for
    thick bulk spectra. The reported composition was itself absorption-derived,
    so this function cannot provide independent material-law validation.
    """

    x = _finite(composition_x, name="composition_x")
    temperature = _finite(temperature_k, name="temperature_k")
    if not COMPOSITION_RANGE[0] <= x <= COMPOSITION_RANGE[1]:
        raise ValueError(
            "Yue 2006 bulk operator requires composition_x in "
            f"[{COMPOSITION_RANGE[0]}, {COMPOSITION_RANGE[1]}]"
        )
    if not TEMPERATURE_RANGE_K[0] <= temperature <= TEMPERATURE_RANGE_K[1]:
        raise ValueError(
            "Yue 2006 bulk operator requires temperature_k in "
            f"[{TEMPERATURE_RANGE_K[0]}, {TEMPERATURE_RANGE_K[1]}]"
        )
    absorption = -65.0 + 1.88 * temperature + (8694.0 - 10.31 * temperature) * x
    if absorption <= 0.0:
        raise ValueError("Yue 2006 critical absorption is nonpositive")
    return float(absorption)
