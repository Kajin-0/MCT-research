"""Regression tests for zero-cost R07/R08 retained-evidence audit."""
from __future__ import annotations

import math
import unittest

from tools.audit_r07_retained_spectral import (
    PAIR,
    R08,
    _json,
    gaussian_centroid,
    gaussian_contrast,
    inverse_contrast,
    load_spectra,
    replay_r07,
    replay_r08,
    run,
)


class TestR07RetainedSpectralGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spectra = load_spectra()
        cls.original = _json(PAIR / "numerical_result.json")

    def test_all_archived_central_values_independently_replay(self):
        result = replay_r07(self.spectra, self.original)
        self.assertEqual(result["gaussian_rows_replayed"], 15)
        self.assertEqual(result["inverse_rows_replayed"], 3)
        self.assertLess(result["max_gaussian_replay_error_eV"], 1e-11)
        self.assertLess(result["max_inverse_replay_error_eV"], 1e-11)

    def test_inverse_eta_robustness_is_probe_specific(self):
        values = [1000 * inverse_contrast(self.spectra, eta)
                  for eta in (0.025, 0.05, 0.1)]
        for value, expected in zip(
            values, (-81.62589860513, -81.47445365236, -80.46361829060)
        ):
            self.assertAlmostEqual(value, expected, places=6)
        self.assertLess(max(values) - min(values), 1.2)

    def test_gaussian_probe_center_reverses_sign(self):
        low = 1000 * gaussian_contrast(self.spectra, 1.0, -0.5)
        high = 1000 * gaussian_contrast(self.spectra, 1.0, 0.5)
        self.assertAlmostEqual(low, -19.32993243938, places=6)
        self.assertAlmostEqual(high, 39.19342188503, places=6)
        r = replay_r07(self.spectra, self.original)
        self.assertLess(r["W1_shift_minus0p5_archived_interval_meV"][1], 0)
        self.assertGreater(r["W1_shift_plus0p5_archived_interval_meV"][0], 0)

    def test_probe_center_crossings_are_not_composition_crossings(self):
        roots = replay_r07(self.spectra, self.original)[
            "gaussian_central_probe_shift_zero_eV"
        ]
        expected = {"1.0": 0.0266033623,
                    "1.5": 0.0303476380,
                    "2.0": 0.2471945593}
        for key, value in expected.items():
            self.assertAlmostEqual(roots[key], value, places=7)
            self.assertLess(abs(gaussian_contrast(
                self.spectra, float(key), roots[key])), 1e-11)

    def test_spectral_centroid_is_origin_covariant(self):
        spectrum = self.spectra["shared"]["Gamma6"]
        original = gaussian_centroid(spectrum, 1.0, 0.27)
        # Energy origin and reference shift together: no change.
        moved = tuple((e + 3.14, w) for e, w in spectrum)
        translated = gaussian_centroid(moved, 1.0, 3.41)
        self.assertTrue(math.isclose(original, translated,
                                     rel_tol=0, abs_tol=1e-12))

    def test_read_only_r08_identity_and_phase_space_limitation(self):
        r = replay_r08(_json(R08 / "finite_k_interference_summary.json"))
        self.assertEqual(r["n_k_sector_records"], 16)
        self.assertGreater(
            r["remote_gt5eV_fraction_at_k8"]["Gamma6_like"], 0.95)
        self.assertGreater(
            r["remote_gt5eV_fraction_at_k8"]["Gamma8_like"], 0.97)
        self.assertEqual(
            r["non_gamma_saved_k_with_near_0p5eV_final_bands"]["Gamma6_like"],
            [(2, 2)]
        )
        self.assertEqual(
            r["non_gamma_saved_k_with_near_0p5eV_final_bands"]["Gamma8_like"],
            []
        )
        self.assertFalse(r["raw_packet_independently_replayed"])

    def test_publication_gate_remains_no_go(self):
        self.assertEqual(run()["publication_gate"],
                         "NO_GO_PHYSICAL_DISORDER_CORRECTION")


if __name__ == "__main__":
    unittest.main()
