# Workflow

## Data flow

```
arxiv.org/pdf/quant-ph/0102014      curl        paper.pdf (174 KB, 12 pp)
                                                     |
                                                     v
                                            pdftotext -layout
                                                     |
                                                     v
                                            work/paper.txt (606 lines)
                                                     |
                                                     v
                                    hand-annotated -> extraction/marker.md
                                                     |
                                                     v
                              (Theorem-13 + Lemma-9 identified as testable primitives)
                                                     |
              +--------------------------------------+---------------------------------+
              v                                                                        v
   work/hsp_ims_theorem13.py                                            work/lemma9_verify.py
   (Qiskit statevector + numpy analytic)                                (exact Qiskit statevector)
              |                                                                        |
              v                                                                        v
   evidence/theorem13_wreath_results.json                            evidence/lemma9_verification.json
   evidence/theorem13_run.log                                        (20 trials, all machine-precision)
   (24 trials, k=1..4, all passed)                                          |
              |                                                             |
              +---------------------------+---------------------------------+
                                          v
                                    REPORT.md, REPORT.tex,
                                    failure_analysis.md,
                                    artifacts_summary.md,
                                    open_questions.json
```

## Tools & versions

| Tool | Version | Role |
|---|---|---|
| Python | 3.13 | Language |
| qiskit | 2.5.0 | Circuit construction, statevector interface |
| qiskit-aer | 0.14+ | `AerSimulator(method='statevector')` |
| numpy | current | Analytic sampling + linear algebra |
| poppler pdftotext | (macOS) | PDF -> text extraction (marker/nougat unavailable) |
| curl | system | Fetch arXiv PDF |
| `~/.openclaw/workspace/scripts/recall.sh` | – | (Not consulted; independent single-paper run) |

## Repro commands

From `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph0102014-nonabelian-hsp-grigni-schulman/`:

```bash
# 1. Paper
curl -sL -o paper.pdf 'https://arxiv.org/pdf/quant-ph/0102014'
pdftotext -layout paper.pdf work/paper.txt

# 2. Environment
python3 -m venv work/.venv
source work/.venv/bin/activate
pip install qiskit qiskit-aer numpy

# 3. Theorem 13 replication (24 trials, k=1..4)
python3 work/hsp_ims_theorem13.py     # ~20 s wall

# 4. Lemma 9 exact-statevector verification (20 trials)
python3 work/lemma9_verify.py         # ~5 s wall
```

Deterministic outputs go to `report/evidence/`.

## Effort estimate

- Total wall-clock (subagent thinking + all runs): ~25 minutes.
- Would-take-a-human estimate (from scratch, no prior knowledge of the paper): 1 day. Two hours to read the paper carefully, four hours to write the Theorem-13 pipeline plus the two group-theoretic helpers (`WreathGroup`, `kernel_z2`), one hour to debug the Qiskit endianness bug, remainder on Lemma-9 quantum-oracle construction + reports.
- Marginal cost for extending to k=5, k=6: seconds each (analytic path is O(|G|²) per sample, still fine at |G|=8192).
- Marginal cost for extending to non-wreath instances (matrix groups over F_2 with the "type (a)/(b)" generator pattern): ~2 hours to write the matrix-group class; then reuse Theorem 13 code as-is.
