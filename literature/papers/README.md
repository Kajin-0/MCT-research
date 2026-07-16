# Private primary-paper manifest

The repository owner supplied private research copies of the papers below. This directory records stable citations and SHA-256 hashes of the exact PDFs used for primary-source and prior-art audits.

The publisher PDFs are not included in this commit. Their hashes are retained so that a later manual or Git LFS import can be verified byte-for-byte. Keep any binary copies private unless redistribution rights are independently established.

| Original PDF filename | Citation | DOI | Original PDF SHA-256 | Audit note |
|---|---|---|---|---|
| `hansen1982.pdf` | G. L. Hansen, J. L. Schmit, and T. N. Casselman, *J. Appl. Phys.* **53**, 7099-7101 (1982) | `10.1063/1.330018` | `aa8017a8f3e136a0b893619e836e8808002b9889119c8e809536e94ebd557357` | `data/hansen/acquisition_log.md` |
| `laurenti1990.pdf` | J. P. Laurenti et al., *J. Appl. Phys.* **67**, 6454-6460 (1990) | `10.1063/1.345119` | `1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea` | `literature/laurenti_reconstruction.md` |
| `krishnamurthy1995.pdf` | S. Krishnamurthy, A.-B. Chen, A. Sher, and M. Van Schilfgaarde, *J. Electron. Mater.* **24**, 1121-1125 (1995) | `10.1007/BF02653063` | `790994754e9d0137e48be7f62fb1fe23ff51e203d78059b65120b0f4122c283b` | `literature/notes/krishnamurthy_1995.md` |
| `allen1976.pdf` | P. B. Allen and V. Heine, *J. Phys. C: Solid State Phys.* **9**, 2305 (1976) | `10.1088/0022-3719/9/12/013` | `fdf15ed1d2c073d8dfdfba81c062c9517be8c19e35ddd5d5e402cec272364246` | `literature/notes/modern_ahc_matrix_and_polar_prior_art.md` |
| `Ponce2015.pdf` | S. Poncé et al., *J. Chem. Phys.* **143**, 102813 (2015) | `10.1063/1.4927081` | `de88f63d4a125fbfb09fb55e202129cd1ad73720f1670e420b394e90b04e3d3a` | `literature/notes/modern_ahc_matrix_and_polar_prior_art.md` |
| `Ponce2015_errata.pdf` | S. Poncé et al., *J. Chem. Phys.* **146**, 099901 (2017) | `10.1063/1.4977571` | `b996e3ebed585291a4d93cd050c8fad79e6a1dd99e66eaa5fd51221486b2ae16` | must accompany the 2015 paper |
| `verdi2015.pdf` | C. Verdi and F. Giustino, *Phys. Rev. Lett.* **115**, 176401 (2015) | `10.1103/PhysRevLett.115.176401` | `d2c7cd52ba074892be25d8e2a0e42cff825502ccc93e777140192b9c5c410e21` | `literature/notes/modern_ahc_matrix_and_polar_prior_art.md` |
| `nery2016.pdf` | J. P. Nery and P. B. Allen, *Phys. Rev. B* **94**, 115135 (2016) | `10.1103/PhysRevB.94.115135` | `9502bbd8b610020e8a74c3b9d79d17574020fa18552a802f42d746fe1154e5e0` | `literature/notes/modern_ahc_matrix_and_polar_prior_art.md` |
| `giustino2017.pdf` | F. Giustino, *Rev. Mod. Phys.* **89**, 015003 (2017) | `10.1103/RevModPhys.89.015003` | `ebc8ad4c23a0f004926585f8c0b8125fe5cf7f207de069194021ec2fc2585746` | review and terminology map, not primary material evidence |
| `lihm2020.pdf` | J.-M. Lihm and C.-H. Park, *Phys. Rev. B* **101**, 121102(R) (2020) | `10.1103/PhysRevB.101.121102` | `fe0fbcd12f3896c2c036302ee268fbedce14e17f0a90fc1c63c44fcb80faa3b6` | highest-priority matrix-AHC prior art |
| `brunin2020.pdf` | G. Brunin et al., *Phys. Rev. Lett.* **125**, 136601 (2020) | `10.1103/PhysRevLett.125.136601` | `8e2ebdb446804aa28b93d3084638b0567d03010c0f4d4b72d28f8d9350bd55ec` | long-range quadrupole prior art |

## Recommended binary import paths

- `literature/papers/private/hansen_1982_energy_gap.pdf`
- `literature/papers/private/laurenti_1990_absorption_edge.pdf`
- `literature/papers/private/krishnamurthy_1995_temperature_dependence.pdf`
- `literature/papers/private/allen_heine_1976_temperature_band_structures.pdf`
- `literature/papers/private/ponce_2015_temperature_electronic_structure.pdf`
- `literature/papers/private/ponce_2017_erratum.pdf`
- `literature/papers/private/verdi_giustino_2015_frohlich_vertex.pdf`
- `literature/papers/private/nery_allen_2016_polar_band_renormalization.pdf`
- `literature/papers/private/giustino_2017_electron_phonon_review.pdf`
- `literature/papers/private/lihm_park_2020_wavefunction_renormalization.pdf`
- `literature/papers/private/brunin_2020_dynamical_quadrupoles.pdf`

After import, recompute SHA-256 and require exact agreement with the manifest above.

## Evidentiary rule

PDF text extraction is not a typeset authority. Equation layout, superscripts, subscripts, signs, tables, plots, and figure labels must be checked visually before a claim is marked primary-verified.

The Poncé 2015 paper must always be interpreted together with its 2017 erratum. The erratum changes the printed forms of Eqs. 4, 5, 7, 15, 16, 18, and 19, while stating that the numerical results, ABINIT implementation, and conclusions are unaffected.