# Artifact Harvest — QC-1708.09213

## Primary source
| Artifact | URL | Local path | Size | Notes |
|---|---|---|---|---|
| arXiv preprint PDF v4 | https://arxiv.org/pdf/1708.09213 | `work/1708.09213.pdf` | 6.45 MB | 27 Jul 2019 version; published as Springer LNP vol. 964 (2020) |
| pdftotext extract | (derived) | `work/paper_full.txt` | 260 KB (6659 lines) | `pdftotext -layout` |

## Software
| Tool | Version | Source |
|---|---|---|
| Python | 3.11.15 | Homebrew python@3.11 |
| numpy | (auto) | pip |
| scipy | (auto) | pip |
| numba | 0.62.1 | pip binary wheel (macOS) |
| llvmlite | (auto) | pip binary wheel (macOS) |
| cytoolz | (auto) | pip binary wheel |
| quimb | 1.14.0 | pip |
| autoray, cotengra, opt_einsum, networkx, tqdm, psutil, requests | (auto) | pip |

## LLM endpoint (judge)
| Provider | Model | Endpoint |
|---|---|---|
| Argo (Argonne) via local proxy | `argo:gpt-5` | `http://127.0.0.1:44497/v1/chat/completions` (bearer: `stevens`, `user: stevens`) — FREE |

## No external data downloads beyond the paper
No genomes, no benchmarks-from-a-repo, no third-party numerical tables — all reference values (exact free-fermion TFIM ground-state energy, CFT central charge c=1/2, chord-distance Calabrese–Cardy formula) are analytical / textbook, re-derived from primary Pauli-convention Hamiltonians in this replication.

## Evidence produced (report/evidence/)
| File | Bytes | Meaning |
|---|---|---|
| `exp1_dmrg_tfim.json` | ~1 KB | DMRG-vs-FF ground energies for N=20,40,60,80 (rel err ≤1e-11) + 1/N extrapolation to −1.2731 (vs −4/π=−1.2732) |
| `exp1b_ed_ff_check.json` | ~1 KB | ED-vs-FF-vs-DMRG cross-check for N=6..12 (agreement to 1e-14) |
| `exp2_entanglement_scaling.json` | ~2 KB | Fit of c from S(l) chord scaling: 0.533 (N=32), 0.517 (N=64), 0.505 (N=128) |
| `exp2b_ent_diag.json` | ~2 KB | Diagnostic: DMRG entropy vs (buggy) Peschel-formula attempt for N=64 |
| `exp2c_ed_entropy.json` | ~1 KB | ED entropy for N=10,12,14,16, fit gives c=0.544 |
| `exp3_canonical_form.json` | ~1 KB | Left-orth error ≤1e-15 per site; single-bond truncation error matches theory to ratio 1.000 |
| `exp4_itebd_tfim.json` | ~1 KB | iTEBD (N=64, chi=32, dtau=0.05, T=8) → E/N=−1.267543 vs FF−1.267593 |
| `llm_judge_verdict.json` | ~4 KB | Argo gpt-5 judge JSON output |

## Code files (work/)
- `exp1_dmrg_tfim_energy.py` – DMRG + Pfeuty FF
- `exp1b_check_ed_small.py` – small-N ED cross-check
- `exp2_entanglement_scaling.py` – critical-CFT entropy scaling
- `exp2b_diag_entropy.py` – diagnostic (Peschel attempt, kept for provenance)
- `exp2c_ed_entropy.py` – ED entropy for small N
- `exp3_canonical_form.py` – MPS canonicalization + optimal truncation
- `exp4_itebd_tfim.py` – imaginary-time TEBD
- `llm_judge.py` – verdict via Argo gpt-5

All logs (`.log`) live alongside their scripts in `work/`.
