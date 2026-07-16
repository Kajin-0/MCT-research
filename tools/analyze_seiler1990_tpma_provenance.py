#!/usr/bin/env python3
"""Audit Seiler 1990 TPMA provenance."""
from __future__ import annotations
import csv, json
from collections import Counter
from pathlib import Path

SAMPLES=Path("data/experimental/seiler1990_table1_samples.csv")
GAPS=Path("data/experimental/seiler1990_table2_low_temperature_magneto_optical.csv")

def read(path):
    return list(csv.DictReader(Path(path).read_text().splitlines()))

def dedx(x,t):
    return 1.93-1.62*x+2.496*x*x-2*5.35e-4*t

def analyze(sample_path=SAMPLES,gap_path=GAPS):
    samples=read(sample_path); gaps=read(gap_path)
    if len(samples)!=5 or len(gaps)!=18:
        raise ValueError("unexpected table length")
    by_id={int(r["sample_number"]):r for r in samples}
    expected={1:(.239,False),2:(.253,False),3:(.259,True),4:(.277,True),5:(.300,True)}
    for n,(x,independent) in expected.items():
        r=by_id[n]
        if float(r["composition_x"])!=x:
            raise ValueError("sample composition mismatch")
        if (r["independent_for_composition_law"]=="true")!=independent:
            raise ValueError("sample provenance mismatch")
    present=[r for r in gaps if r["present_work"]=="true"]
    if {int(r["sample_number"]) for r in present}!={1,3,4,5}:
        raise ValueError("present-work sample mismatch")
    rows=[]
    for g in present:
        n=int(g["sample_number"]); s=by_id[n]
        x=float(g["composition_x"])
        if x!=float(s["composition_x"]):
            raise ValueError("table join mismatch")
        sx=float(g["composition_sigma_x"]) if g["composition_sigma_x"] else None
        sg=float(g["gap_sigma_mev"]) if g["gap_sigma_mev"] else None
        er=None; rr=None
        if sx is not None:
            er=sorted(abs(dedx(x,t))*sx*1000 for t in (2,10))
            rr=[v/sg for v in er]
        rows.append({
            "sample_number":n,"composition_x":x,"gap_mev":float(g["gap_mev"]),
            "gap_sigma_mev":sg,"composition_provenance":s["composition_provenance"],
            "independent_for_composition_law":s["independent_for_composition_law"]=="true",
            "composition_energy_sigma_range_2_10k_mev":er,
            "composition_to_gap_sigma_ratio_range":rr})
    independent=[r for r in rows if r["independent_for_composition_law"]]
    summary={
        "table1_sample_count":len(samples),"table2_gap_row_count":len(gaps),
        "measurement_class_counts":dict(sorted(Counter(r["measurement_class"] for r in gaps).items())),
        "provenance_status_counts":dict(sorted(Counter(r["composition_provenance_status"] for r in gaps).items())),
        "present_work_tpma_count":len(present),
        "independent_present_work_tpma_count":len(independent),
        "independent_sample_numbers":[r["sample_number"] for r in independent],
        "independent_compositions":[r["composition_x"] for r in independent],
        "composition_uncertainty_exceeds_gap_sigma":all(min(r["composition_to_gap_sigma_ratio_range"])>1 for r in independent),
        "hansen_derivative_used_only_as_sensitivity":True,
        "decision":"Only samples 3, 4, and 5 are present-work TPMA anchors with independently calibrated composition. Samples 1 and 2 cannot validate a composition law.",
        "observable_boundary":"The reported TPMA gap is inferred from a modified Pidgeon-Brown fit to resonant Landau-level transitions.",
        "next_task":"Digitize Figure 7 by specimen while preserving one shared composition per specimen."}
    return rows,summary

if __name__=="__main__":
    rows,summary=analyze(); print(json.dumps({"rows":rows,"summary":summary},indent=2,sort_keys=True))
