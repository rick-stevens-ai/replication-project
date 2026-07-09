# Failure analysis — Hansen, Hartong & Obers 2018 replication

Overall outcome: **REPLICATED** with 0 failures across ~5,600 symbolic assertions.
This document records the transient failures encountered during construction
and how each was resolved. None survived into the final verdict.

---

## F1 — Jacobi failures from double-registered antisymmetric brackets (Stage 2a)
**Symptom.** Initial pass of `verify_algebra.py` failed the Jacobi identity on
a large subset of triples at d=3, with an integer-doubling pattern in the
residuals.

**Root cause.** The paper's compact notation `2 δ_{c[a} X_{b]}` unpacks to
`δ_{ca} X_b − δ_{cb} X_a`. My `add()` helper auto-antisymmetrises brackets
(registers a bracket once and generates the flipped version automatically).
I initially registered BOTH `[X, Y] = +Z` and `[Y, X] = −Z` explicitly, then let
the helper flip again — every entry accumulated with coefficient 2.

**Fix.** Register each bracket exactly once and rely on the antisymmetriser
for the flipped orientation. After the fix: 220 / 220 (d=2), 1140 / 1140
(d=3), 4060 / 4060 (d=4) triples pass.

**Lesson.** With SymPy structure-constant tensors, decide upfront whether
your `add(a, b, c, coef)` helper is symmetric or antisymmetric under `a↔b`
and use it consistently. Cross-check by summing over ordered vs. unordered
triples.

---

## F2 — Sign-convention ambiguity in `[J_{ab}, X_c]` (Stage 2a)
**Symptom.** After F1 was fixed, ~15% of Jacobi triples involving `J_{ab}`
still failed at d=3 with a consistent sign pattern.

**Root cause.** The paper writes `[J_{ab}, X_c]` and
`[J_{ab}, J_{cd}]` with implicit index-flip conventions that are not spelled
out explicitly. Two natural sign choices exist; only one is Jacobi-compatible
with the given commutation relations. Specifically the compatible convention
is
```
[J_{ab}, X_c] = δ_{ca} X_b − δ_{cb} X_a
[J_{ab}, J_{cd}] = δ_{ac} J_{bd} − δ_{ad} J_{bc} − δ_{bc} J_{ad} + δ_{bd} J_{ac}
```

**Fix.** Adopt the sign convention above uniformly. Jacobi failures fell to
zero.

**Lesson.** For any paper that presents an algebra via index-heavy compact
notation, derive the sign convention from an internal consistency check
(Jacobi on one non-trivial triple) BEFORE running the full scan.

**Flag for errata.** The paper does not state its `J_{ab}` sign convention
explicitly. Recording this note explicitly in a follow-up communication
would spare future readers ~30 minutes of debugging.

---

## F3 — `pdf` tool routed to paid Anthropic direct API (Stage 1)
**Symptom.** Attempting to use the built-in `pdf` tool to summarise `paper.pdf`
returned an error like "credit balance too low", implying the tool routed
through Anthropic direct rather than through the free Argo proxy.

**Root cause.** The `pdf` tool defaults to Anthropic direct for its underlying
model call. Rick's standing rule is "free endpoints only".

**Fix.** Abandoned the `pdf` tool; used `pdftotext -layout` locally instead
(free, produces 46,265 B of clean text with all key equations legible).
Verified no chargeable call landed.

**Lesson.** Before any tool call that might route to a paid model, either
(a) confirm the tool's routing, or (b) prefer a shell equivalent (`pdftotext`,
local SymPy, `curl` against the Argo proxy). This is now standard practice.

---

## F4 — Choice of coordinate labels affects visible-diagnostics readability (Stage 2c)
**Symptom.** First version of `verify_poisson_reduction.py` used generic
coordinate labels `x0, x1, x2, x3`. The output listing
`Γ̄^{x_1}_{x_0 x_0} = ∂Φ/∂x_1` was hard to read/verify against the paper's
`t, x, y, z` convention.

**Root cause.** Symbolic-computation output readability lag.

**Fix.** Renamed to `t, x_1, x_2, x_3` (paper convention). No mathematical
change; results identical.

**Lesson.** When symbolic output is going to be read by humans (or later
LLM judges), pick coordinate labels that match the paper's convention from
the outset.

---

## F5 — LLM-judge prompt initial version leaked verdict language (Stage 3, minor)
**Symptom.** First draft of `judge_prompt.txt` included the phrase "this
appears to replicate the paper" in the framing, which would bias the judge.

**Root cause.** Author-side framing bias.

**Fix.** Rewrote the prompt to state neutrally: here are the paper claims,
here are the verification-script outputs verbatim; please issue an
independent verdict from {REPLICATED, PARTIAL, NOT-REPLICATED}. Both judges
subsequently returned REPLICATED independently — which is now a credible
signal, not a self-fulfilling one.

**Lesson.** LLM-judge prompts must be adversarial or at least neutral; if
the prompt telegraphs the desired verdict, the "cross-check" is worthless.

---

## Summary
Five transient issues encountered; all resolved before final verdict; none
undermine the final REPLICATED outcome. Two of the five (F2, F5) generated
process improvements worth carrying forward:
1. Always derive sign conventions from an internal consistency check before
   running full scans on index-heavy algebras.
2. LLM-judge prompts must not telegraph the desired verdict.

The one paper-side observation worth communicating: the `J_{ab}` sign
convention is under-specified in the paper's presentation of eq. (11) and
would benefit from an explicit statement in an erratum or follow-up.
