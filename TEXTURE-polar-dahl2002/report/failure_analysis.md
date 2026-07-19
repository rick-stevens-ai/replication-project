# Failure Analysis — TEXTURE-polar-dahl2002

## Overarching: the paper is non-replicable *as posed*
The single biggest "failure" is inherent to the target: it is a **book-review /
terminology-and-priority polemic**, not a primary research paper. It has no
model, no dataset, no reproducible figure, and no headline number. The scaffold's
method extract correctly recommended DROP. We did not fabricate a nonexistent
result; instead we replicated the **domain physics the paper argues about** and
Dahl's own qualitative alternative-view proposals. Coverage is therefore
intrinsically capped (6/10) — you cannot reproduce numbers a paper never reports.

## What genuinely limited the replication

### F1. PDF tool blocked by write-scope policy
`pdf` tool refused `~/Dropbox/...` ("not under an allowed directory"). Worked
around by using the pre-extracted `extraction/marker.md` (pdftotext, complete)
via grep/sed. No information loss — the marker text is the full paper — but figure
*images* (e.g. the disputed early-experiment photos) were not visually inspected;
they are not quantitative anyway.

### F2. C2 absolute prefactor is not in the paper (partial)
The quoted law τ = γ/(Ps·E) is stated by Lagerwall (quoted by Dahl) as a
*scaling*, with no numerical prefactor and no definition of "switching time"
(10-90%? 1/e? full swing?). Our 10-90% time is 3.5× γ/(Ps·E). Root cause: the
prefactor is the definitional integral ∫sec φ dφ over the 10-90% window, which is
field-independent (verified numerically AND analytically, agreement <3%). So the
*scaling* is exact; only an undefined constant differs. Marked PASS(scaling), not
PASS(exact), to stay honest — we cannot match a number the paper never gives.

### F3. Model is qualitative (matching a qualitative source)
The uniform-director / rigid-cone reduction omits: spatial φ(z) domain-wall
structure, tilt-magnitude relaxation θ(z) at surfaces, chevron layer geometry,
and full disclination-line energetics. These are all out-of-scope for a minimal
tractable model and are logged as open questions (Q2, Q3, Q5), NOT faked.

### F4. Static-friction model (C5) is a reduced 1-DOF caricature
Dahl's static-friction bistability is real physics but our C5 implements it as a
threshold comparison (|driving| vs F_static), not a full multi-DOF dissipative
integration with a disclination-passage energy landscape (which Dahl describes
qualitatively, p.34). The reduced model demonstrates *self-consistency* of the
mechanism (memory + threshold) but does not derive F_static from surface
chemistry — flagged as open question Q1. This is a scope boundary, marked as such.

## No fabrication statement
Every number in `work/results.json` came from actually running
`code/ssflc_model.py`. The C2 prefactor discrepancy was investigated (not hidden)
with `verify_C2_prefactor.py`. Out-of-scope items (full DFT, domain-wall solver,
chevron energetics, surface-chemistry F_static) are explicitly marked out-of-scope
in open_questions.json, not simulated or asserted.

## Lessons
1. For review/opinion "papers," pivot to replicating the *domain physics under
   discussion* + any *original claims the author advances* (here Dahl's C3, C5),
   rather than forcing a nonexistent numerical reproduction.
2. When a quoted law lacks a prefactor definition, verify the *scaling* and
   explain the constant analytically rather than declaring pass/fail on an
   undefined absolute value.
3. Dropbox paths are outside the `pdf` tool's allowlist — use the pre-extracted
   marker text.
