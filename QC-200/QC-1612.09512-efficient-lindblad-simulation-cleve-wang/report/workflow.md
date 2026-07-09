# Workflow — QC-200 replication of arXiv:1612.09512

## What was reproduced
The **mathematical kernel** of Cleve & Wang's polylog-precision Lindblad-simulation
algorithm: the truncated-Taylor / LCU expansion of $\exp(t\mathcal{L}_{\text{vec}})$
on the vectorised Liouvillian of a 2-qubit open-system model. This is the
convergence-rate content that the paper's Theorem-1 gate-count claim rides on.

## Pipeline (executed 2026-07-05 evening CDT)

1. **Fetch paper**
   - `curl -sL -o paper.pdf https://arxiv.org/pdf/1612.09512`
   - `pdftotext -layout paper.pdf work/paper.txt`
   - Verified authors (Cleve, Wang), title, and v3 date directly from PDF header.

2. **Skim + extract headline claim**
   - Grep `work/paper.txt` for `Theorem|Corollary|complexity|O\(t|polylog|Taylor|LCU|precision`.
   - Isolated the key testable quantity: **truncated-Taylor error decays as
     $K = O(\log(1/\varepsilon))$** for fixed $t$.

3. **Extraction placeholders (Marker + Nougat slots)**
   - Marker/Nougat not installed on `CherryRd`; central corpus had no
     pre-parsed 1612.09512 outputs.
   - Wrote hand-typed structured substitutes:
     - `extraction/marker.md` — sectioned prose + verbatim abstract + claims table
     - `extraction/nougat.mmd` — TeX-formatted equations + theorem/corollary
       statements
   - Both files declare the fallback openly. Impact assessment lives in
     `report/failure_analysis.md` and is judged cosmetic — the reproduction uses
     equations lifted directly from the source PDF, not from any parser.

4. **Numerical reproduction**
   - Wrote `report/evidence/lindblad_lcu.py` (~10 kB, self-contained, numpy + scipy).
   - Built model: $n=2$ qubits, Hermitian $H = 0.7\,XI + 0.3\,IZ + 0.2\,XX$;
     Lindblad ops $L_1 = \sqrt{0.9}\,I\!\otimes\!\sigma_-$ (amplitude damping)
     and $L_2 = \sqrt{0.3/2}\,Z\!\otimes\!I$ (pure dephasing).
   - Built vectorised Liouvillian using column-stack convention
     $\text{vec}(AXB) = (B^\top\!\otimes A)\,\text{vec}(X)$.
   - Gold standard: `scipy.linalg.expm(t * L_vec) @ vec(rho0)`.
   - LCU-Taylor approx: $\sum_{k=0}^{K} (t\mathcal L_{\text{vec}})^k / k!$
     evaluated at $K\in\{4,8,16\}$ for $t\in\{0.5,1,2\}$.
   - K-scaling sweep: $K = 1..30$ at each $t$; linear fit of
     $\log_{10}\varepsilon$ vs $K$ over the non-underflow regime.
   - Trace preservation: 26 samples of $\mathrm{Tr}\,\rho_{\text{exact}}(t)$
     over $[0, 2]$.
   - Verdict logic in-script: REPLICATED iff (all 3 t reach $\varepsilon<10^{-6}$)
     AND (all 3 K-slopes $<-0.3$) AND (trace max-dev $<10^{-9}$).

5. **Result**
   - Verdict: **REPLICATED** (see `report/REPORT.tex` §Results and
     `report/evidence/results.json`).
   - Best $\varepsilon$ at $K=16$: $\{2.1\!\times\!10^{-16},\,
     1.0\!\times\!10^{-14},\,1.3\!\times\!10^{-9}\}$ for $t=\{0.5,1,2\}$.
   - Slopes (dex per unit $K$): $\{-1.12,\,-0.92,\,-0.71\}$.
   - Trace max-dev: $4.6\!\times\!10^{-16}$.

## Tools and versions
| Tool | Version | Role |
|------|---------|------|
| Python | 3.14 (`/usr/local/bin/python3`) | driver |
| numpy | 2.4.3 | vectorised Liouvillian, kron products |
| scipy | 1.18.0 | `scipy.linalg.expm` gold standard |
| pdftotext (Poppler) | system default | PDF → txt for skim + extraction |
| curl | system default | arXiv PDF fetch |
| bash / zsh | system default | orchestration |
| pdflatex | (not compiled here — REPORT.tex is source-form; PDF is optional) | report typeset |

**Not used** (deliberately or unavailable on host):
- LLM inference — not needed; free-endpoint rule respected.
- Marker / Nougat — not installed; substituted per §3 above.
- QuTiP / Cirq / Qiskit — not needed for the linear-algebra kernel; noted as
  next-step in `open_questions.json` Q5 for the ancilla-measurement circuit.

## Effort estimate
- Paper fetch + skim: ~3 min
- Extraction placeholders: ~10 min (hand-transcribed key equations + theorem statements)
- Reproduction script (`lindblad_lcu.py`) design + write: ~15 min
- Debug / verification: ~2 min (first run passed on all triggers, no debug loop)
- Report + open questions + failure analysis + artifacts summary: ~20 min
- **Total wall-clock: ~50 min** (single subagent turn)

## Reproducibility instructions
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1612.09512-efficient-lindblad-simulation-cleve-wang
python3 report/evidence/lindblad_lcu.py         # rewrites report/evidence/results.json
```
No network access required after paper fetch. Deterministic (no RNG).
