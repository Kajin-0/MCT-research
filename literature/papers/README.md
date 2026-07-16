# Private primary-paper manifest

The repository owner supplied private research copies of the three papers below on 2026-07-16. This directory records stable citations and SHA-256 hashes of the exact PDFs used for the current primary-source audit.

The publisher PDFs are not included in this commit. Their hashes are retained so that a later manual or Git LFS import can be verified byte-for-byte. Keep any binary copies private unless redistribution rights are independently established.

| Original PDF filename | Citation | DOI | Original PDF SHA-256 | Audit note |
|---|---|---|---|---|
| `hansen1982.pdf` | G. L. Hansen, J. L. Schmit, and T. N. Casselman, *J. Appl. Phys.* **53**, 7099-7101 (1982) | `10.1063/1.330018` | `aa8017a8f3e136a0b893619e836e8808002b9889119c8e809536e94ebd557357` | `data/hansen/acquisition_log.md` |
| `laurenti1990.pdf` | J. P. Laurenti et al., *J. Appl. Phys.* **67**, 6454-6460 (1990) | `10.1063/1.345119` | `1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea` | `literature/laurenti_reconstruction.md` |
| `krishnamurthy1995.pdf` | S. Krishnamurthy, A.-B. Chen, A. Sher, and M. Van Schilfgaarde, *J. Electron. Mater.* **24**, 1121-1125 (1995) | `10.1007/BF02653063` | `790994754e9d0137e48be7f62fb1fe23ff51e203d78059b65120b0f4122c283b` | `literature/notes/krishnamurthy_1995.md` |

## Recommended binary import paths

- `literature/papers/private/hansen_1982_energy_gap.pdf`
- `literature/papers/private/laurenti_1990_absorption_edge.pdf`
- `literature/papers/private/krishnamurthy_1995_temperature_dependence.pdf`

After import, recompute SHA-256 and require exact agreement with the manifest above.

## Evidentiary rule

PDF text extraction is not a typeset authority. Equation layout, superscripts, subscripts, signs, tables, plots, and figure labels must be checked visually before a claim is marked primary-verified.
