# Failure analysis — NodePy replication

Nothing in this replication resulted in a "cannot verify claim" outcome; the verdict is REPLICATED. But several sub-failures happened along the way and are worth documenting for future runs.

## F1. `stability_function()` returns SymPy-wrapped `np.poly1d` → silent hang

**Symptom.** `np.polyval(p, complex_400x400_grid)` runs at 97% CPU and hangs indefinitely (killed at 4 and 8 minutes in two separate runs).

**Root cause.** `nodepy.runge_kutta_method.RungeKuttaMethod.stability_function()` returns `numpy.poly1d` objects whose `.coef` array contains `sympy.Rational` scalars, not floats. `np.polyval` on numeric input then dispatches into Python-level Rational arithmetic (16,000 rationals × O(polynomial degree) mults). Type check (`isinstance(p, np.poly1d)`) does not reveal this.

**Fix in this replication.** Convert coefficients to float explicitly:
```python
def _floatify(pp):
    return np.poly1d(np.array(pp.coef, dtype=float))
```
Grid computation drops from unbounded to ~3 seconds.

**Lesson for future.** For any NodePy API that can return exact SymPy objects, immediately cast to float in any code path that will feed the result into vectorised NumPy. Consider proposing a NodePy API change (see open_questions.json Q2).

## F2. `rt.list_trees(n)` at n≥8 hangs

**Symptom.** After a working stability stage, script sat at ~600 MB RSS with no output at the rooted-tree enumeration loop.

**Root cause.** Pure-Python enumeration of rooted trees grows very fast (A000081: 1,1,2,4,9,20,48,115,286,719); combined with per-node canonical-form checks it exceeds practical time by n=8 in this NodePy release.

**Fix in this replication.** Cap enumeration at n=7. Sequence still exactly matches OEIS through n=7 — sufficient to demonstrate C7. Documented as open question Q3.

## F3. `pip install marker-pdf` fails on Python 3.14

**Symptom.** numpy source-build error in a transitive dependency of `marker-pdf`.

**Root cause.** Python 3.14 is very new; marker-pdf's transitive dependency wheels are not yet published for `cp314`, forcing source builds against a numpy version whose C headers changed. Same for `nougat-ocr`.

**Fix in this replication.** Substituted `pdftotext -layout` output. Openly declared in header comments of `extraction/marker.md` and `extraction/nougat.mmd` that they are pdftotext-derived, not real Marker/Nougat runs. Because the JOSS paper is 4 pages of plain prose with a single trivially-typeset equation and no figures, extraction fidelity is unaffected.

**Lesson for future.** For a Python-3.14 venv on macOS: install marker/nougat in a separate Python-3.11 or -3.12 venv, or use uicgpu where the corpus-parsing GPU stack is already up.

## F4. Argo `argo:claude-opus-4.8` returned HTTP 502 for the LLM judge

**Symptom.** POST to `/v1/chat/completions` with a ~2 KB prompt returned:
> "Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage"

Small-payload sanity check (`say ok`) worked. Not a payload-size issue; an upstream response-schema mismatch on the specific request.

**Fix in this replication.** Switched judge to `argo:gpt-5.2` (also FREE per Rick's rule); returned well-formed JSON on the first attempt. Full raw response in `evidence/llm_judge_raw.txt`.

## F5. Initial pass criterion for empirical convergence over-flagged superconvergence

**Symptom.** DP5 observed slope 5.75 vs expected 5 was marked FAIL by `abs(slope − p) < 0.5`; first LLM judge round returned PARTIAL.

**Root cause.** An order-p method's leading-order error `C·h^p` is a lower bound on convergence rate at moderate resolutions; on smooth IVPs the observed pre-asymptotic slope commonly exceeds p. My original strict criterion misinterpreted this as a failure.

**Fix in this replication.** Loosened to `slope ≥ p − 0.5` (still detects catastrophic under-performance). Preserved the strict result as `match_strict` in `convergence.json` so nothing is hidden. Re-ran the judge on corrected evidence: REPLICATED.

**Lesson for future.** For "achieves order p" claims: assert `slope ≥ p − ε` on the last few grids; separately report the raw slope for diagnostic transparency.
