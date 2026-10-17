"""Decision-only R07 exact-xCd=1/8 atomistic configurational-capacity audit.
No SCF, DFT, approximation to disorder mass, or new source-model assumption.
"""
import json,math,itertools,hashlib
from pathlib import Path
a=6.46
basis=((0,a/2,a/2),(a/2,0,a/2),(a/2,a/2,0))
def cart(v):
    return [sum(v[i]*basis[i][j] for i in range(3)) for j in range(3)]
def closest_pair(cells,u,v):
    dv=tuple(v[i]-u[i] for i in range(3))
    return min(math.dist((0.,0.,0.),cart(tuple(dv[i]+n[i]*cells[i] for i in range(3))))
            for n in itertools.product((-1,0,1), repeat=3))
def audit(cells):
    sites=list(itertools.product(*(range(n) for n in cells)))
    n=len(sites)
    assert n%8==0
    cd=n//8
    result={"primitive_repetitions":list(cells),"atoms":2*n,"cation_sites":n,
            "cadmium_sites_for_x0125":cd,"number_of_raw_Cd_occupancy_sets":math.comb(n,cd),
            "number_of_single_Cd_orbits_under_lattice_translations":1}
    if cd==1:
        result["Cd_Cd_pair_distances_A"]=[]
        result["Cd_pair_correlations_identifiable"]=False
    elif cd==2:
        distances=sorted({round(closest_pair(cells,u,v),9) for u,v in itertools.combinations(sites,2)})
        result["Cd_Cd_pair_distances_A"]=distances
        result["Cd_pair_correlations_identifiable"]="different pair distances allow inequivalent environments, but 1-2 configurations do not establish ensemble convergence"
    return result
r16=audit((2,2,2));r32=audit((2,2,4))
assert r16["atoms"]==16 and r16["cadmium_sites_for_x0125"]==1
assert r32["atoms"]==32 and r32["cadmium_sites_for_x0125"]==2
assert len(r32["Cd_Cd_pair_distances_A"])>=2
pbe=Path("/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/physical_pbe_soc_16atom_20261013/impurity/pw.in")
raw=pbe.read_text()
atoms=raw.split("ATOMIC_POSITIONS crystal\n")[1].split("\n\nK_POINTS")[0].splitlines()
assert len(atoms)==16
assert sum(x.lstrip().startswith("Cd ") for x in atoms)==1
conditional_m=-0.04939398435995024
out={"purpose":"disorder benchmark capacity and coherent sign-switch decision threshold; not a disorder calculation",
 "lattice_constant_A":a,"supercells":[r16,r32],
 "archived_x0125_PBE16_input":{"exists":True,"Cd_atoms":1,"atoms":16,"source_path":str(pbe),"sha256":hashlib.sha256(pbe.read_bytes()).hexdigest(),
    "scientific_status":"input and interrupted older PBE archive; not accepted self-consistent HSE alloy evidence"},
 "historical_HSE16_resource":{"source":"research/programs/microscopic_bandgap/native_matched_pilot_2026-10-11/decision.md",
    "interrupted_family_RSS_GiB":26.72213,"authorized_family_cap_GiB":26.63966,
    "SCF_completed":False,"Cd_substitution_started":False},
 "conditional_VCA_x0125_half_ordering_eV":conditional_m,
 "conditional_positive_disorder_shift_needed_for_sign_reversal_eV":-conditional_m,
 "important_limits":["conditional x=.125 VCA sign NOT certified under prospective 1e-8 full-density symmetry gate",
     "two Cd sites and multiple pair distances are necessary not sufficient for ensemble uncertainty",
     "x=.125 PBE 16-atom model is different from HSE",
     "same-H screened spectral correction and configurational uncertainty remain unknown",
     "no native run or spending authorized by this capacity test"]}
path=Path(__file__).with_name("structural_gate.json")
path.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"16atom":r16,"32atom":r32,"conditional_sign_reversal_meV":-conditional_m*1000},indent=2))
