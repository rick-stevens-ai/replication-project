# Workflow — Poremba 2022 replication (arXiv:2203.01610)

**Date:** 2026-07-05
**Host:** CherryRd (m1 Mac Studio, Darwin 25.3.0)
**Wave:** QC-200
**Executor:** subagent under `agent:main:telegram:direct:8542341053`
**Wall clock:** ~50 min end-to-end (paper fetch → all 8 artifacts)

## Steps executed

| # | Step | Tool / command | Time |
|---|------|---|---|
| 1 | Read wave brief | `read ~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md` | <1s |
| 2 | Create target dir + subdirs | `mkdir -p work extraction report/evidence` | <1s |
| 3 | Fetch paper PDF | `curl -sL -o work/paper.pdf https://arxiv.org/pdf/2203.01610`  |  <5s |
| 4 | Verify author/title from PDF | `pdftotext -layout work/paper.pdf work/paper.txt; head -50` | <2s |
| 5 | Skim §7.1 Construction 1 | `awk '/^7.1 Construction/,/^7.2/' work/paper.txt` | <5s |
| 6 | Create venv + install deps | `python3 -m venv venv && pip install numpy scipy qiskit qiskit-aer` | ~120s |
| 7 | Implement + test (a) LWE base | `report/evidence/lwe_base.py`; smoke = 400/400 ok | ~3s |
| 8 | Implement + test (b),(c),(d),(e) BB84 layer | `report/evidence/bb84_deletion.py`; 200-trial run | ~30s |
| 9 | Implement + test combined LWE+BB84 pipeline | `report/evidence/lwe_bb84_full.py`; 200-trial run | ~34s |
| 10 | Save results | `report/evidence/results.json` | <1s |
| 11 | Marker/Nougat extraction (fallback) | `pdftotext -layout` + headers → `extraction/marker.md`, `extraction/nougat.mmd` | <5s |
| 12 | Write REPORT.tex + open_questions | edit | <1s |
| 13 | Compile REPORT.pdf | `pdflatex REPORT.tex` | ~10s |
| 14 | Write workflow.md / artifacts_summary.md / failure_analysis.md | edit | <1s |

## Tools + versions

| Tool | Version |
|---|---|
| macOS | Darwin 25.3.0 (Tahoe) |
| Python | 3.14 (system) → venv |
| numpy | 2.5.1 |
| scipy | 1.18.0 |
| qiskit | 2.5.0 |
| qiskit-aer | 0.17.2 |
| pdftotext | poppler 25.03.0 (Homebrew) |
| pdflatex | TeX Live 20260301 |
| curl | Apple curl 8.15.0 |

## Missing tools (falling back to surrogate)

| Tool | Attempted | Failure mode | Fallback |
|---|---|---|---|
| `marker-pdf` (VikParuchuri) | ~/.openclaw hosts | `TypeError: Invalid input type 'PdfDocument'` at `pdftext.extraction._load_pdf` on Darwin 25 + `pypdfium2 4.30.0`; not installable in reasonable time | `pdftotext -layout` reflowed as GFM with an honest surrogate note in the top-of-file header + a `extraction/README.md` explanation |
| `nougat` (Meta) | ~/.openclaw hosts | pins `transformers==4.28.1` + `torch<2.1`; requires building `torchvision` from source, blocked by MacOSX 26 SDK | `pdftotext -layout` reflowed with a Nougat-style YAML `---` header |

Both fallbacks are prominently labeled as surrogates and mirror the sibling
QC-200 replication `QC-quant-ph-9709029-entanglement-formation-two-qubits-wootters/`
under the same Darwin 25 + m1 constraints.

## Effort estimate

- Total automated work: ~50 min wall-clock
- Human effort equivalent: ~4 hours (paper skim + choose which claims are
  reproducible on a laptop + design the qubit-scale demo of a
  qudit-scale construction + implement + validate + write up)

## What is genuinely reproduced vs. surrogated

| Component | Reproduction |
|---|---|
| Dual-Regev LWE ciphertext distribution (Lemma 17 target) | GENUINE — computational-basis distribution of the primal Gaussian state matches the classical Dual-Regev ciphertext distribution exactly (this is a theorem) |
| Correctness of Dec (Lemma 17) | GENUINE at $n{=}8, q{=}257, m{=}128, \sigma{=}3.2$; 400/400 |
| Quantum encoding — primal Gaussian state on $\mathbb{Z}_q^{m+1}$ | SURROGATE — full state has $\approx 10^{310}$ amplitudes, unsimulable. We use the BB84 precursor (BI20, cited by Poremba §1) on 17 qubits, sharing the same certified-deletion structure |
| Correctness of Vrfy (Lemma 18) on honest Del | GENUINE for the BB84 primitive; 200/200. The paper's Fourier-basis Vrfy on the full primal state cannot be simulated at qudit resolution |
| Cheater accept-prob tradeoff | GENUINE for the BB84 primitive; exponentially decreasing in cheated qubits, matches theory |
| IND-CPA security under LWE | ASSUMED — asymptotic, non-empirical |
| Certified-deletion security under strong Gaussian-collapsing | ASSUMED — asymptotic, non-empirical |
| FHE extension (§9) | NOT ATTEMPTED — out of scope |
