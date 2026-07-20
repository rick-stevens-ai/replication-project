# Failure Analysis — arXiv:1404.5920 replication

## Tooling failures encountered (and fixes)

### 1. Target directory did not exist
- **Symptom:** `TEXTURE-multipolar-chandra2014/` (with `paper.pdf` + `extraction/marker.md`)
  was described in the task but absent on disk.
- **Root cause:** dir had not been staged yet; the naming convention matched sibling
  `TEXTURE-*` projects.
- **Fix:** created the dir + 8-artifact skeleton and fetched `paper.pdf` from
  `arxiv.org/pdf/1404.5920` per the task's fallback rule. No fabrication.

### 2. `pdf` vision tool unavailable
- **Symptom:** `pdf` tool errored — Anthropic "credit balance too low", Google model name
  unknown, OpenAI PDF extraction plugin disabled. Also the Dropbox path was outside the
  tool's allowed roots.
- **Root cause:** all three PDF-capable vision backends down/disabled; media-path allowlist.
- **Fix:** used `pdftotext -layout` (poppler) to extract the full body text (719 lines) and
  read it directly. All equations/numbers transcribed from that dump and cross-checked against
  surrounding prose. Documented the fallback in `extraction/marker.md`.

### 3. JSON serialization of numpy bool
- **Symptom:** `TypeError: Object of type bool is not JSON serializable` on `json.dump`.
- **Root cause:** a `pass` flag was a `numpy.bool_` (from an `and` involving a numpy comparison).
- **Fix:** wrapped in `bool(...)` and added a custom `NpEnc` JSON encoder for np bool/int/float/ndarray.
  Re-ran clean.

## Scientific scope decisions (out of scope, marked not faked)
- **Microscopic mean-field curves (Figs. 3, 7):** g(θ), χ_xy, condensation entropy require a
  self-consistent solution of the two-channel Anderson lattice (Eqs. 20–24). This is a full
  many-body computation, beyond the "analytic/tractable" remit. Marked out of scope.
- **Resonant nematicity LDOS (Fig. 8b):** needs the same mean-field Green's functions. Out of scope.
- **Transverse-moment tension (~0.01 μB vs <0.0011 μB):** the paper itself lists this as an open
  puzzle; we surface it as open-question #5 rather than force a number.
- **No DFT:** the paper is analytic theory; a DFT g(θ) is a *suggested future experiment* in the
  paper, not a result to replicate.

## What went right
- The paper's analytic backbone is highly checkable and reproduced to high precision
  (C2 to 0.3%, C5 to 1e-7, C3 spin-zeros pinned to half-integers). The off-by-one in the
  spin-zero count (17 predicted vs 16 observed) is expected from using nominal g*·m* rather than
  the true FS average — flagged as open-question #2, not a failure.

## Lessons for future replications
- When the `pdf` vision tool is down, `pdftotext -layout` is a reliable, zero-cost fallback for
  text-heavy theory papers (equations survive reasonably well in layout mode).
- Always cast/serialize numpy scalars before `json.dump`; add an encoder proactively.
- Theory/review papers: prioritize closed-form relations and Landau/symmetry claims — they are
  the machine-checkable core; defer full mean-field/DFT to out-of-scope with concrete next steps.
