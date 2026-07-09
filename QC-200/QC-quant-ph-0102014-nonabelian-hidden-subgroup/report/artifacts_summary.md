# Artifacts Summary

Target directory:
`~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0102014-nonabelian-hidden-subgroup/`

## Required 8 artifacts (per QC wave brief completion bar)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Original paper PDF | `paper.pdf` | ✓ 174 143 B, 12 pages, arXiv:quant-ph/0102014v1 |
| 2 | Marker parse | `extraction/marker.md` | ⚠️ Fallback (Poppler `pdftotext`); Marker install failed on Python 3.14 (numpy metadata error). Explicit header notes fallback. |
| 3 | Nougat parse | `extraction/nougat.mmd` | ⚠️ Fallback (Poppler `pdftotext -layout`); Nougat not installed within wave time budget. Explicit header notes fallback. |
| 4 | Report LaTeX | `report/REPORT.tex` | ✓ Full section-by-section with verdict, claims table, method, results table, discussion, 5 open questions. |
| 5 | Open questions JSON | `report/open_questions.json` | ✓ 5 objects, each `{q, basis, next_steps}`. |
| 6 | Workflow | `report/workflow.md` | ✓ Step-by-step reproduction with commands + tool versions + time estimate. |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✓ This file. |
| 8 | Failure analysis | `report/failure_analysis.md` | ✓ Marker/Nougat absence, negative controls, undone reproductions. |

## Additional evidence (`report/evidence/`)
| File | Bytes | Notes |
|---|---|---|
| `ims_theorem13_results.json` | ~15 KB | Full JSON output of 15-instance Theorem-13 replication. |
| `dihedral_hsp_results.json` | ~2 KB | Negative-control results (plain dihedral, wrong hypothesis). |
| `paper_text.txt` | ~44 KB | `pdftotext -layout` dump of the paper. |

## Code (`code/`)
| File | Bytes | Notes |
|---|---|---|
| `ims_theorem13.py` | ~14 KB | Faithful IMS §6 implementation — MAIN replicator. |
| `dihedral_hsp.py` | ~10 KB | Negative-control implementation for plain D_n. |
| `ims_theorem13_results.json` | ~15 KB | Duplicate of evidence copy (in-place output of the script). |
| `dihedral_hsp_results.json` | ~2 KB | Duplicate of evidence copy. |

## Work / intermediates (`work/`)
| File | Bytes | Notes |
|---|---|---|
| `paper.pdf` | 174 143 | Fetched from `https://arxiv.org/pdf/quant-ph/0102014`. |
| `paper.txt` | ~44 KB | `pdftotext -layout` dump (source for `extraction/nougat.mmd`). |
| `paper_plain.txt` | ~40 KB | `pdftotext` (no `-layout`) dump (source for `extraction/marker.md`). |

## Traces of key decisions
- **Choice of Theorem 13 as target:** §6 has the paper's most-concrete
  reproducible mechanism (an explicit auxiliary function `F` + reduction
  to Abelian HSP). Theorems 8 and 11 are more abstract compositions of
  black-box subroutines that would require re-implementing Beals-Babai
  and would blow past the QC-100 time budget.
- **Choice of N = F_2^k:** direct match to §6's hypothesis ("elementary
  abelian 2-subgroup"); allows exact-arithmetic verification of every
  step over F_2.
- **k ≤ 6:** keeps `2^{k+1} = 128` amplitude vectors and `(k+1)² ≤ 49`
  gate matrices tiny; entire 15-instance sweep runs in 0.05 s wall time,
  making the result trivially re-runnable and easy to extend.
- **σ chosen randomly with 3 seeds per k:** exercises multiple outer
  automorphisms so the correctness result is not artefact of one lucky
  choice.
- **|H| = 2 (single reflection):** paradigmatic non-Abelian HSP case;
  larger |H| left to Open Question Q2.
- **LLM judge = `argo:gpt-5.2`:** free per QC wave rule; `argo:claude-opus-4.8`
  was tried first but returned an upstream schema error (likely a proxy
  bug); GPT-5.2 accepted the prompt and returned the verdict cleanly.

## Reproducibility one-liner
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0102014-nonabelian-hidden-subgroup
python3 -m venv .venv && source .venv/bin/activate && \
    pip install --quiet qiskit qiskit-aer numpy && \
    python3 code/ims_theorem13.py && \
    python3 code/dihedral_hsp.py
```
Expected exit: prints 15 lines `[k=… seed=… …] onPerp=1.00000000 …
match=True`, then writes `code/ims_theorem13_results.json`.
