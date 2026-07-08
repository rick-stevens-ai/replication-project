# Artifacts summary — QC-1904.02260 (contextuality test for VQE)

Independent replication of Kirby & Love, PRL 123, 200501 (2019).
QC-100 wave, verdict **REPLICATED** (6/6 Table I contextuality verdicts).

## Artifact index (8 standard + supporting)

| # | Path (relative to dir root) | Purpose | Backfilled? |
|---|---|---|---|
| 1 | `report/REPORT.md` | Human-readable replication report (source of truth) | No — original 2026-07-03 |
| 2 | `report/REPORT.tex` | LaTeX version with honest Critique section + open-questions input | **Yes — 2026-07-06** |
| 3 | `report/open_questions.json` | 5 truly-open questions (bare JSON list) with basis + next steps | **Yes — 2026-07-06** |
| 4 | `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions | **Yes — 2026-07-06** |
| 5 | `report/workflow.md` | Procedural log of the replication | **Yes — 2026-07-06** |
| 6 | `report/artifacts_summary.md` | This file — artifact index | **Yes — 2026-07-06** |
| 7 | `report/failure_analysis.md` | Expanded honest critique | **Yes — 2026-07-06** |
| 8 | `extraction/nougat.mmd` | Extraction stub (paper is text-mineable directly; see work/paper.txt) | **Yes — 2026-07-06** |

## Supporting artifacts (pre-existing)

| Path | Purpose |
|---|---|
| `code/contextuality_test.py` | Self-contained implementation of Theorem 3 classifier + molecular Hamiltonian builder + VQE sanity |
| `report/evidence/contextuality_results.json` | Machine-readable results: |S|, |T|, witness triples, HF/FCI/VQE energies |
| `work/paper.pdf` | The paper itself |
| `work/paper.txt` | Plain-text extraction of the paper |

## Scientific bottom line

- **Verdict:** REPLICATED
- **Headline claim exercised?** YES — the paper's Theorem 3 classifier was re-implemented from scratch and applied to real molecular Hamiltonians built from PySCF integrals via OpenFermion JW/BK transforms. All 6 tested Table I verdicts (H2 x3 non-contextual; HeH+, LiH, H2O contextual) reproduce.
- **Not tested:** the CD_0 quantitative heuristic (out of scope), BeH / Schwinger / deuteron rows of Table I, the classical-simulability construction (Kirby-Love 2020, separate paper), comparison against alternative advantage witnesses (magic, entanglement, negativity), noise robustness on NISQ hardware.
- **Compute:** ~90 s CPU on CherryRd. No paid API, no GPU, no HPC.

## Reproduction

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1904.02260-contextuality-test-vqe
python3 -m venv venv && source venv/bin/activate
pip install --quiet qiskit qiskit-nature qiskit-algorithms pyscf openfermion openfermionpyscf
python3 code/contextuality_test.py
```

Expected output: `report/evidence/contextuality_results.json` matches the pre-existing file bit-for-bit modulo VQE seed noise (which converges to FCI to 1e-9 Ha regardless).
