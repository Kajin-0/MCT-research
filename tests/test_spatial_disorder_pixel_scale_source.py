from __future__ import annotations

from mct_research.spatial_disorder_validation_path import (
    EvidenceState,
    QualificationClass,
    qualify_validation_candidate,
)
from tools.build_spatial_disorder_pixel_scale_source_reference import (
    build_reference,
    candidate_records,
)


def _records_by_id():
    return {item.source_id: item for item in candidate_records()}


def test_phillips_2003_is_one_scale_figure_benchmark() -> None:
    phillips = _records_by_id()[
        "phillips_2003_pixel_scale_absorption_mapping"
    ]
    result = qualify_validation_candidate(phillips)

    assert phillips.doi == "10.1063/1.1625776"
    assert phillips.independent_effective_scale_count == 1
    assert phillips.numerical_data_available is EvidenceState.ABSENT
    assert phillips.spatial_map_reported is EvidenceState.CONFIRMED
    assert result.qualification is (
        QualificationClass.SOURCE_BOUNDED_FIGURE_BENCHMARK
    )
    assert result.direct_validation_ready is False
    assert "three_effective_scales_or_reusable_map" in (
        result.missing_direct_requirements
    )


def test_dense_raster_does_not_increase_effective_scale_count() -> None:
    phillips = _records_by_id()[
        "phillips_2003_pixel_scale_absorption_mapping"
    ]
    notes = " ".join(phillips.notes)

    assert "400 measured spectra" in notes
    assert "9 micrometres" in notes
    assert "10-micrometre spacing" in notes
    assert "200 by 200 micrometre" in notes
    assert phillips.independent_effective_scale_count == 1


def test_phillips_source_statistics_are_source_bounded() -> None:
    phillips = _records_by_id()[
        "phillips_2003_pixel_scale_absorption_mapping"
    ]
    notes = " ".join(phillips.notes)

    assert "887 cm^-1" in notes
    assert "24.6 cm^-1" in notes
    assert "2.8 percent" in notes
    assert "x = 0.2256" in notes
    assert "3.0e-4" in notes
    assert "measurement drift" in notes


def test_reference_separates_partial_and_pixel_scale_benchmarks() -> None:
    reference = build_reference()
    by_source = {
        item["source_id"]: item["qualification"]
        for item in reference["qualifications"]
    }

    assert reference["schema_version"] == "1.2"
    assert len(by_source) == 11
    assert by_source["gopal_1992_two_beam_transmission"] == (
        "partial_multiresolution_benchmark"
    )
    assert by_source[
        "phillips_2003_pixel_scale_absorption_mapping"
    ] == "source_bounded_figure_benchmark"

    headline = reference["headline"]
    assert headline["nearest_partial_multiresolution_benchmark"] == (
        "gopal_1992_two_beam_transmission"
    )
    assert headline["nearest_detector_pixel_scale_benchmark"] == (
        "phillips_2003_pixel_scale_absorption_mapping"
    )
    assert headline["pixel_scale_reported_spectrum_count"] == 400
    assert headline["pixel_scale_beam_diameter_micrometre"] == 9.0
    assert headline["pixel_scale_scan_spacing_micrometre"] == 10.0


def test_reference_preserves_dense_raster_claim_boundaries() -> None:
    boundaries = " ".join(build_reference()["claim_boundaries"])
    assert "dense raster" in boundaries
    assert "Four hundred spectra" in boundaries
    assert "one effective probe scale" in boundaries
    assert "manuscript" in boundaries
