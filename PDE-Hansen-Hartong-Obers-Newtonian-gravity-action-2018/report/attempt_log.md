# Attempt log — Hansen-Hartong-Obers 2018 replication

All times CDT.

## 2026-07-04 10:09
Sub-agent spawned. Read `WAVE_BRIEF_2026-07-01.md`. Confirmed target dir does not yet exist.

## 10:11
Located the paper on arXiv (1807.04765 v2), fetched PDF via `ssh uicgpu` (heavy-fetch
policy).  MD5 `15ce60ac1e1db7a0889275cb6b9a5220`, 163032 bytes. Staged into `work/paper.pdf`.

## 10:12
Tried the `pdf` tool for reading — blocked (routes to Anthropic/OpenAI paid endpoints, forbidden
by wave-brief "free endpoints only" rule).  Fell back to `pdftotext -layout` locally, produced a
clean 46 KB / 422-line extract.  All key equations (1)–(21), the algebra table (eq. 11), and the
references are legible.

## 10:14
Identified the three testable algebraic claims:
- **C1** — the type-II TNC algebra (eq. 11) is a valid Lie algebra of dimension (d+1)(d+2), and
  differs from Bargmann as claimed.
- **C2** — the connection eq. (2) is metric-compatible on generic TTNC backgrounds, with the
  torsion formula the paper states.
- **C3** — the flat NC background reduction of eq. (6) yields the Poisson equation eq. (7).

Other paper content is either narrative (motivation, discussion, prior-art citations) or is the
statement of the action eq. (12) whose full variational derivation would require an out-of-scope
symbolic-tensor engine — I chose to instead verify the *result* of that variation via C3.

## 10:15
Wrote `verify_algebra.py`, ran at d=3.  First run FAILED (66 Jacobi violations).  Diagnosed two
bugs: (i) I double-registered `[G_a,G_b]=-S_{ab}` (my `add()` helper auto-antisymmetrises, so
enumerating both (a,b) and (b,a) doubled the coefficient); (ii) my J-J commutator had the wrong
sign convention relative to `[J_{ab},X_c]=δ_{ca}X_b − δ_{cb}X_a`.  Fixed both.

Second run: **PASS** — all 1140 Jacobi triples close at d=3.  Also re-ran at d=2 (220 triples PASS)
and d=4 (4060 triples PASS).  Dimension count matches (d+1)(d+2) for d=1..4.  Ideal ⟨T,B,S⟩
confirmed; quotient reproduces Bargmann brackets exactly.

## 10:16
Wrote `verify_poisson_reduction.py`.  Ran at d=2,3,4 on the flat NC background
(τ=dt, m=Φdt, h^{ij}=δ_{ij}).  On the first run:
- Only non-zero connection components: `Γ^{x_i}_{tt} = ∂_i Φ` — the classical Newtonian
  acceleration reappearing as a temporal-temporal connection component.
- Only non-zero Ricci component: `Ricci_{tt} = Σᵢ ∂_i²Φ = ∇²Φ`.  All off-diagonal Ricci vanish.
- Substituting Ricci_{tt} = 8πG (d-2)/(d-1) ρ (paper eq. 6) into the symbolic result yields
  ∇²Φ = 8πG (d-2)/(d-1) ρ, exactly paper's eq. (7).

## 10:16
Wrote `verify_metric_compat.py`.  Ran at d=2 and d=3 on a generic (non-flat) TTNC background with
lapse A(x^μ) and generic m_μ(x^μ):
- ∇̄_μ τ_ν = 0 : 0 fails / 9 at d=2, 0 fails / 16 at d=3.  PASS.
- ∇̄_μ h^{νρ} = 0 : 0 fails / 27 at d=2, 0 fails / 64 at d=3.  PASS.
- Torsion Γ̄^λ_{[μν]} = -v̂^λ ∂_[μ τ_{ν]} : 0 fails / 9 at d=2, 0 fails / 24 at d=3.  PASS.
Zero failures across 149 individual component checks.

## 10:17
LLM-judge cross-check. Assembled `judge_prompt.txt` (all script outputs summarised, no cherry-picking).
Called Argo (`argo:gpt-5`, free endpoint):
  - verdict = REPLICATED, coverage = 70%, agreement = "exact", confidence = "very-high".
Called Argo again with `argo:claude-opus-4.6` (independent judge, different vendor family):
  - verdict = REPLICATED, coverage = 62%, agreement = "exact", confidence = "very-high".
Both judges independently converge on REPLICATED with exact agreement.
Also tried `argo:claude-opus-4.8` (502 upstream), `argo:claude-opus-4.7` (invalid schema on Argo — known
transient issue).  Opus 4.6 succeeded, sufficient for cross-vendor triangulation.

## 10:18
Copied all artefacts (three scripts + three raw stdouts + two judge responses + judge prompt +
paper.pdf) from uicgpu/tmp into the target dir under work/ and report/evidence/.  Wrote
brief.md, attempt_log.md, artifact_harvest.md, REPORT.md.

## What did NOT go wrong / what I skipped
- No fabricated numbers anywhere.  Every stdout in `report/evidence/` is the raw output of a
  SymPy script that a reader can rerun.
- I did not attempt the full variational derivation of paper's eq. (12) EoMs (~50 lines of
  index-heavy tensor algebra), and I did not verify the invariance of eq. (12) under the full
  set of type-II gauge transformations (eq. 10).  Both are within reach of a serious `xAct`-style
  computer-algebra effort but well outside the scope of a single-shot replication and outside the
  time/compute budget of one wave slot.  I list these explicitly in the caveats of the REPORT.

## Conclusion
All three testable claims independently verified with exact symbolic agreement.  Two independent
LLM judges converge on REPLICATED.  Filed as **REPLICATED**.
