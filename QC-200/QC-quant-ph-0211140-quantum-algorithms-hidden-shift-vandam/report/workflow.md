# Workflow: QC-200 replication of quant-ph/0211140

## 1. Narrative

1. **Paper retrieval** — Fetched `https://arxiv.org/pdf/quant-ph/0211140` into `work/paper.pdf` (12 pages, 214 KB). Verified authors + title from the PDF text: **van Dam, Hallgren, Ip, "Quantum Algorithms for some Hidden Shift Problems," 21 Nov 2002** — matches the task's expected metadata exactly.
2. **Text extraction** — Ran `pdftotext` (reading-order) into `work/paper.txt` and `pdftotext -layout` into `extraction/paper_layout.txt`. Skimmed both to locate Algorithm 1 (Sec. 4), Fig. 1 circuit, and the (1-1/q)² success probability claim.
3. **Corpus check for Marker/Nougat parses** — Searched `~/Dropbox` for pre-parsed versions of `0211140`. None found in `~/Dropbox/REPLICATE-PROJECT/pde_corpus` or `~/Dropbox/XFER/lucid_marker_queue`.
4. **Marker/Nougat install attempt** — `pip install marker-pdf nougat-ocr` inside the QC venv both required `torch>=1.4`, which the local wheel index could not resolve within the wave-time window. Killed the install and produced fallback extractions from `pdftotext` output with an explicit disclosure header at the top of both `extraction/marker.md` and `extraction/nougat.mmd`.
5. **Simulation design** — Chose exact numpy statevector (no Qiskit/Cirq needed for N≤32); implemented the paper's Fig. 1 circuit as four matrix-vector operations: (i) amplitude-encode `f(x)=g(x+s)`, (ii) QFT, (iii) diagonal phase `1/g_hat(y)`, (iv) inverse QFT + argmax.
6. **Boolean-g on Z_N** — Task brief asked for Boolean g. Boolean g with strictly flat spectrum does not exist on Z_N for the sizes required; used rejection sampling to get Boolean g with nowhere-zero spectrum (so the phase-uncompute step is well-defined). Documented in code.
7. **Chirp-g on Z_N** — For a clean "matches paper's flat-spectrum multiplicative-character setup" experiment we also ran the Zadoff-Chu chirp `exp(2πi a x²/(2N))` for each N. This gave deterministic (p=1.0) recovery.
8. **Legendre-symbol on F_13** — Implemented Algorithm 1 verbatim with `chi(x)=(x/13)`.
9. **Classical query lower bound** — Computed info-theoretic `ceil(log2 N)` bound and empirical worst-case ambiguity class size for k=1..6 random non-adaptive queries per N.
10. **Analysis** — Compared empirical peak probability to paper's `(1-1/q)^2`; explained the 0.923 vs 0.852 discrepancy on F_13 as our exact simulation skipping the Lemma-1 measurement branch (0.923 × (1-1/13) = 0.852 exactly).
11. **Report drafting** — Wrote LaTeX report `report/REPORT.tex`, five deep open questions `report/open_questions.json`, this workflow, `failure_analysis.md`, and `artifacts_summary.md`.

## 2. Tools & versions

| Tool | Version | Used for |
|---|---|---|
| Python | 3.13 (venv `~/.openclaw/workspace/venvs/qc-replicate/`) | driver |
| numpy | 2.5.1 | statevector arithmetic, DFT |
| sympy | latest (imported, unused) | reserved for future extension |
| pdftotext (poppler) | system `/usr/local/bin/pdftotext` | PDF -> text |
| curl | system | fetching arXiv PDF |
| bash / zsh | macOS default | shell |
| No Qiskit, Cirq, Stim, PennyLane | — | not needed at N≤32 |
| No Marker, no Nougat | — | install blocked by torch resolution; fell back to pdftotext-based extraction (disclosed) |
| No LLM | Argo endpoint not needed — self-verdict per brief when time budget tight | judging |

## 3. Code inventory

| File | LOC | Purpose |
|---|---|---|
| `report/evidence/hidden_shift_zn.py` | ≈ 300 | Full replication: Z_N + Legendre + classical bound |
| `report/evidence/hidden_shift_results.json` | — | Machine-readable results (all trials + summaries) |

## 4. Effort estimate

| Phase | Wall-clock | Notes |
|---|---|---|
| PDF fetch + skim | ~4 min | curl + pdftotext + read |
| Corpus check + marker/nougat install attempt | ~5 min | install killed after torch resolution failed |
| Simulation coding | ~15 min | ~300 LOC of numpy |
| Debug (bent function search, chirp construction, summary key rename) | ~5 min | one iteration cycle |
| Runs (all 40 shift trials + classical distinguisher, 3 group sizes + Legendre) | < 5 s | numpy exact |
| Report writing (REPORT.tex + open_questions + workflow + failure + artifacts) | ~15 min | this pass |
| **Total** | **~45 min** | single subagent turn |

Total compute: negligible (all runs finish in < 5 s on a laptop, no HPC / GPU).

## 5. Commands (reproducible recipe)

```bash
# 0. Prep
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0211140-quantum-algorithms-hidden-shift-vandam/{work,extraction,report/evidence}
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0211140-quantum-algorithms-hidden-shift-vandam

# 1. Paper
curl -sL -o work/paper.pdf https://arxiv.org/pdf/quant-ph/0211140
cp work/paper.pdf paper.pdf
pdftotext work/paper.pdf work/paper.txt
pdftotext -layout work/paper.pdf extraction/paper_layout.txt

# 2. Venv + numpy
python3 -m venv ~/.openclaw/workspace/venvs/qc-replicate
source ~/.openclaw/workspace/venvs/qc-replicate/bin/activate
pip install -q --upgrade pip
pip install -q numpy sympy

# 3. Run replication
python report/evidence/hidden_shift_zn.py

# 4. (Optional) compile LaTeX
pdflatex -output-directory=report report/REPORT.tex
```
