# Workflow — Terhal & Smolin (quant-ph/9705041) Replication

## Objective
Independently reproduce the central numerical claim of Terhal & Smolin (1997):
a single quantum query using the Bernstein–Vazirani parity oracle retrieves an
n-bit database string y with probability 1, versus a classical bound of
n / log2(n+1) queries.

## Steps taken
1. **Fetch paper.** `curl` arXiv PDF (`https://arxiv.org/pdf/quant-ph/9705041`)
   into `work/paper.pdf` and copy to `<dir>/paper.pdf`.
2. **Skim + confirm claim.** `pdftotext` → read Sec. II and III. Confirmed
   authors (Terhal, Amsterdam; Smolin, IBM Watson), central claim
   (single-query P=1 for BV parity oracle), and note that the paper does NOT
   claim to beat Grover on Hamming-weight-1 search — that clarification
   reshaped the reproduction target (BV parity, not Grover N=4).
3. **Extractions.** `pdftotext -layout` → `extraction/marker.md`;
   `pdftotext -raw` → `extraction/nougat.mmd`. Both files carry a fallback
   header matching the sibling-dir convention because Marker/Nougat proper
   are not installed in this environment.
4. **Environment.** `python3 -m venv .venv && pip install qiskit qiskit-aer numpy`.
5. **Simulation code.**
   - `report/evidence/bv_single_query.py`: BV single-query circuit; enumerates
     all 16 databases in {0,1}^4; runs both exact statevector and 4096-shot
     sampled recovery; also computes analytic Grover 1-iteration baselines
     for N=16 and N=4.
   - `report/evidence/coin_weighing.py`: coin-weighing variant; n=4 with
     single defective coin (4 databases), plus n=8 sweep over all 256
     databases as a scaling check.
6. **Run.** Both scripts complete in seconds on CPU. All 16 (n=4) and all 256
   (n=8) databases recover with P_exact = 1.0 and P_shots = 1.0.
7. **Reporting.** `report/REPORT.tex` written (11 KB, section-by-section
   with claims table + per-claim what-worked/what-didn’t + verdict).
   `report/open_questions.json` written (5 questions, each with basis +
   next_steps). Companion `workflow.md` (this file), `artifacts_summary.md`,
   `failure_analysis.md`.
8. **Verdict.** REPLICATED (headline numerical claim exact match).

## Tools & versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14.x (system) | driver |
| qiskit | 2.5.0 | circuit construction |
| qiskit-aer | 0.17.2 | statevector + shot simulation |
| numpy | 2.5.1 | numeric baselines |
| pdftotext (poppler) | system | Marker/Nougat fallback |
| curl | system | fetch arXiv PDF |
| bash / zsh | system | orchestration |
| pip | 24.x | package install |

## Code / scripts written
| Path | Purpose | LOC |
|---|---|---|
| `report/evidence/bv_single_query.py` | Main BV n=4 replication | ~160 |
| `report/evidence/coin_weighing.py` | n=4 HW1 and n=8 sweep | ~80 |
| `report/REPORT.tex` | Detailed LaTeX report | ~180 |

## Effort estimate
- Wall-clock time: ~20 minutes end-to-end (1 subagent turn).
- Compute: <30 seconds total simulation time on a single CherryRd CPU core.
- LOC written: ~420 (Python + LaTeX + JSON).
- Simulation runs: 16 (n=4, exact + shots) + 4 (n=4 HW1) + 256 (n=8) = 276 BV runs.
- Human/agent steps: ~15 tool calls (fetch, pdftotext, venv+install, code, run x2, write 8 artifacts).
- Free-endpoint spend: 0 tokens on paid APIs; all work local except arXiv PDF fetch.

## Not done (deferred, tracked as open questions)
- Noise-model degradation sweep (Q1).
- Non-uniform Huffman variant (Q2).
- T-count / fault-tolerant depth cost (Q3).
- Random-coding empirical vs analytic collision rate (Q4).
- Dephasing threshold study (Q5).
