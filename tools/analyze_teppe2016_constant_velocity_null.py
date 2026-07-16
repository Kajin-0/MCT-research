#!/usr/bin/env python3
"""Test the Teppe experimental constant-velocity null."""
from __future__ import annotations
import csv, json
from pathlib import Path

GAPS=Path("data/experimental/teppe2016_figure_annotated_signed_gaps.csv")
VELOCITY=Path("data/experimental/teppe2016_kane_velocity_summary.csv")
KRISH=Path("data/theory/krishnamurthy1995_hg078cd022_kane_closure.csv")

def read(path):
    return list(csv.DictReader(Path(path).read_text().splitlines()))

def analyze(gap_path=GAPS,velocity_path=VELOCITY,krish_path=KRISH):
    gaps=read(gap_path); velocity_rows=read(velocity_path); krish=read(krish_path)
    if len(gaps)!=8 or len(velocity_rows)!=1:
        raise ValueError("unexpected Teppe transcription length")
    by_sample={s:sorted([r for r in gaps if r["sample_id"]==s],key=lambda r:float(r["temperature_k"])) for s in ("A","B")}
    a_gap=[float(r["signed_gap_mev"]) for r in by_sample["A"]]
    b_gap=[float(r["signed_gap_mev"]) for r in by_sample["B"]]
    if not all(v>0 for v in a_gap) or b_gap!=[-24.0,-14.0,0.0,18.0]:
        raise ValueError("signed-gap transcription mismatch")
    vrow=velocity_rows[0]
    velocity=float(vrow["velocity_m_per_s"]); sigma=float(vrow["velocity_sigma_m_per_s"])
    relative_sigma=sigma/velocity
    robust=[r for r in krish if float(r["temperature_k"])<=300]
    drift=max(abs(float(r["hyperbolic_velocity_relative_to_1k"])-1.0) for r in robust)
    summary={
        "sample_a_composition":0.175,"sample_b_composition":0.155,
        "sample_a_gap_annotations_mev":a_gap,"sample_b_gap_annotations_mev":b_gap,
        "sample_b_critical_temperature_k":77.0,
        "velocity_m_per_s":velocity,"velocity_sigma_m_per_s":sigma,
        "velocity_relative_sigma":relative_sigma,
        "krishnamurthy_max_velocity_drift_1_300k":drift,
        "krishnamurthy_drift_to_teppe_sigma_ratio":drift/relative_sigma,
        "constant_velocity_null_supported":drift<relative_sigma,
        "simplified_model_relation":"c_tilde=sqrt(2 P^2/(3 hbar^2))",
        "full_8band_P_identified":False,
        "model_boundary":"Teppe retains Gamma6 and Gamma8 while neglecting Gamma7 and quadratic momentum terms.",
        "decision":"Modern magnetospectroscopy supports a constant reduced Kane velocity through the signed-gap transition at the quoted precision. A large scalar P(T) correction is not the leading null below 120 K.",
        "claim_boundary":"The cross-paper comparison is scale consistency, not direct validation, because composition, temperature range, and reduced Hamiltonian differ."}
    return gaps,summary

if __name__=="__main__":
    rows,summary=analyze(); print(json.dumps({"rows":rows,"summary":summary},indent=2,sort_keys=True))
