# Workflow — brazovskii2003 replication packaging

**Paper:** S. Brazovskii, *Theory of the ferroelectric phase in organic conductors:
optics and physics of solitons*, arXiv:cond-mat/0306006v2 (ECRYS-2002 proceedings).
**Class:** analytic / theory proceedings paper — closed-form relations, **no numerical tables**.
**Verdict:** PARTIAL (mechanism-level REPLICATED), coverage 8/10, agreement 9/10.

## Pipeline
1. **Acquire** — PDF already present (`textures-polar-brazovskii2003.pdf`) + reading-order
   text (`textures-polar-brazovskii2003.txt`).
2. **Parse / extract** — `pdftotext -layout` -> `extraction/marker.md` (prose artifact);
   `pdftotext` (reading order) -> raw dump appended under a hand-transcribed LaTeX
   equation block -> `extraction/nougat.mmd` (math artifact). Real `marker`/`nougat`
   binaries are NOT installed (interim fallback; flagged in-file and in artifacts_summary).
3. **Build** — independent reimplementation of every stated analytic relation as a
   machine-checkable identity (`work/brazovskii2003_replication.py`). NOT author code
   (the paper ships none). Method: turn each closed form into a numerical assertion;
   treat `≈`/`~` formulas as criticality limits and verify by monotone convergence.
4. **Run** — executed with the numpy-capable interpreter (below). Small algebraic /
   small-matrix build; finishes in <1 s.
5. **Compare** — no single headline number (proceedings paper). Scored against functional
   forms + order-of-magnitude claims; 10/10 checks pass. Headline ratio
   `omega_t/(2*Delta) = pi*gamma/2 = 0.393` at gamma=0.25.
6. **Verify-before-package** — live re-ran the solver; printed output matches the saved
   `work/brazovskii2003_result.json` / `brazovskii2003_output.json` to the quoted digits
   (10/10). This makes the "reproduce" claims literally true, not a stale-file assertion.
7. **Report** — 8-artifact package (this directory).

## Tools / versions
| Tool | Version / status |
|------|------------------|
| Python | `/home/stevens/comfyui-env/bin/python` |
| NumPy | 2.3.5 |
| SciPy | 1.17.0 (available; not required by this kernel) |
| pdftotext (poppler) | present (`/usr/bin/pdftotext`) |
| marker | **NOT installed** — pdftotext interim used for `extraction/marker.md` |
| nougat | **NOT installed** — pdftotext interim used for `extraction/nougat.mmd` |
| pdflatex | **NOT installed** — `REPORT.tex` delivered as source, compiles off-host |

## Reproduce
```bash
cd textures-polar-brazovskii2003/
/home/stevens/comfyui-env/bin/python report/evidence/brazovskii2003_replication.py
# -> prints results JSON; verdict.checks all true, n_passed=10, n_total=10
```

## Effort estimate
- Physics (independent reimplementation of all analytic relations): ~2–3 h (already done).
- Packaging (this pass: extraction, REPORT.tex, questions, analyses, evidence copy,
  live re-verify): ~45 min.
- Compute footprint: negligible (single-node CPU, <1 s run).
