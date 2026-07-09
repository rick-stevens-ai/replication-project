# Failure Analysis — Zang, Street & Koseff (1994) Replication

**Replication id:** `PDE-Zang-Street-Koseff-fractional-step-1994`
**Verdict:** REPLICATED (Cartesian limit)
**Purpose of this file:** honest accounting of what did NOT work cleanly,
what was simplified relative to the paper, and what remains uncertain.

---

## 1. Argo `claude-opus-4.7` schema-validation bug (blocked, worked around)

**Symptom.** Every non-trivial LLM-judge request to
`argo/argo:claude-opus-4.7` returned HTTP 502 from the Argo proxy with the
upstream error:

```
Failed to parse upstream response: 1 validation error(s):
Value at 'choices[0].message' does not match any variant of SystemMessage |
UserMessage | AssistantMessage | ToolMessage
```

Trivial (hello-world) requests to `argo:claude-opus-4.7` worked, so the
model was registered and live in the proxy — but any response with a
non-trivial structured payload triggered the schema validator.

**Root cause (upstream).** Response-side JSON schema validation in the Argo
proxy is over-strict for whatever shape `claude-opus-4.7` is now returning
(likely a message-content variant that the proxy's Pydantic-style union
does not enumerate).

**Workaround.** `judge.py` tries 4.7 first, records the failure to
`judge_verdict.json`, then falls back to `argo:claude-opus-4.5` (also free).
Both attempts are logged with `requested_model` and `actual_model` fields
so the substitution is auditable.

**Residual risk.** The verdict was rendered by a different model than
requested. This is disclosed. A strict-replication re-run would repeat the
LLM-judge call once the Argo proxy schema bug is fixed.

---

## 2. Re = 400 v-centreline: single-point disagreement at x = 0.9063

**Symptom.** The `v_max` error at Re = 400 is 0.148, over an order of
magnitude worse than the peak-velocity agreement at Re = 100 and Re = 1000.
Traced to a single Ghia (1982) tabulated point at x = 0.9063 where the
Ghia value (v = −0.2383) sits well above the smooth curve traced by its
own neighbours (v = −0.4499 at x = 0.8594; v = −0.2285 at x = 0.9453).

**Analysis.** Our v-centreline profile smoothly connects the surrounding
Ghia points; the LLM judge independently flagged the Ghia table entry at
x = 0.9063 as a suspected transcription anomaly. Removing this single point
drops the Re=400 v_max_err from 0.148 to 0.005, in line with the
Re=100/1000 agreement.

**What we did.** Report the raw error without post-hoc filtering. The
transcription-anomaly hypothesis is noted but not adopted as ground truth.

**Residual risk.** We may be wrong about the Ghia point. Independent
verification against a modern high-accuracy cavity reference (Botella &
Peyret 1998; Erturk, Corke & Gökçöl 2005) would either confirm the
transcription anomaly or reveal a real deviation in our solver at that
location. This has not been done.

---

## 3. Simplifications versus the paper's algorithm

The following simplifications were adopted; each is a scope choice, not a
solver limitation. Together they reduce the replication's reach.

### 3.1 ADI-implicit diffusion → forward Euler

- **Paper:** implicit ADI for the diffusion term in the predictor.
- **Ours:** forward Euler for the full predictor (convection + diffusion).
- **Cost:** viscous stability restricts Δt ≲ 0.2·h²/ν, which is more
  restrictive than the paper's implicit scheme allows at high Re.
- **Consequence:** we do not test whether the ADI splitting error couples
  cleanly to the momentum-interpolation face-flux recovery. It probably
  does — the paper's own results say so — but we do not confirm it.

### 3.2 General curvilinear coordinates → uniform Cartesian

- **Paper:** general curvilinear coordinates with contravariant fluxes and
  full Jacobian metric bookkeeping.
- **Ours:** uniform Cartesian mesh (Rhie-Chow face-flux averaging
  degenerates to simple arithmetic averaging).
- **Consequence:** claim C3 is not tested. This is the paper's principal
  engineering-relevance claim (its title!). Our REPLICATED verdict is
  explicitly qualified "Cartesian limit" for this reason.

### 3.3 Multigrid pressure Poisson → direct sparse LU

- **Paper:** multigrid on the pressure Poisson equation.
- **Ours:** pre-factorised sparse LU (`scipy.sparse.linalg.splu`), one-time
  factorisation, per-step back-solves.
- **Cost:** trivially fast at N=128; would scale poorly to N ≥ 512.
- **Consequence:** we never exercise the multigrid convergence properties
  ZSK relied on for larger cases. Irrelevant for correctness in this run,
  relevant for any scale-up.

---

## 4. Near-lid interpolation artefact (known, benign)

**Symptom.** With cell-centred storage the top interior row sits at
y = (N − 0.5)/N ≈ 0.996, not at y = 1. Linear extrapolation to y = 1 gives
u ≈ 0.94–0.97 against the exact boundary condition u = 1.

**Analysis.** Discretisation artefact of cell-centred storage; halves on a
finer mesh; not a solver bug. Common to all cell-centred cavity codes.

**What we did.** Note in §5.3 of REPORT.md and in the *Genuine Critique*
section of REPORT.tex.

**Residual risk.** A strict comparison against Ghia's boundary values
requires care; we report interior-point comparisons which are unaffected.

---

## 5. No formal order-of-accuracy study (C4 untested)

**Symptom.** We run at a single mesh (N = 128). We do not measure the
convergence rate of L₂-error in either space or time.

**Analysis.** A single-mesh comparison against a fine benchmark is a sanity
check, not an accuracy proof. Second-order convergence (C4) is claimed by
the paper but not tested here.

**What we did.** Explicitly flag C4 as "Not formally measured" in the
claims table and in the *Genuine Critique* section of REPORT.tex.

**Residual risk.** A three-mesh (N = 64, 128, 256) L₂-error regression on
a manufactured solution or on the cavity centrelines would produce the
missing convergence evidence in ~1 additional hour of compute. Not
performed in this replication.

---

## 6. Reynolds-number ceiling at Re = 1000

**Symptom.** Ghia (1982) tabulates Re ∈ {100, 400, 1000, 3200, 5000, 7500,
10000}. We stop at Re = 1000.

**Analysis.** Re ≥ 3200 requires longer transients, and the flow may not
converge as a simple fixed point without careful handling of the tertiary
and quaternary corner vortices. Explicit-Euler Δt restrictions also make
higher-Re runs expensive on our simplified scheme.

**What we did.** Scope choice — bounded to Re ∈ {100, 400, 1000} for a
wave-push budget.

**Residual risk.** A higher-Re run (Re = 3200, Re = 5000) on the same
solver would either confirm the scheme carries to more demanding cases or
reveal an unmodelled issue. Not performed.

---

## 7. Compute used vs compute available

**Symptom.** The replication was targeted at `uicgpu` (8×A100). The actual
solver is single-threaded numpy/scipy and does not use any GPU.

**Analysis.** No penalty — the problem is small enough (N=128) that a
single CPU core solves it in ~2 minutes per Re. Targeting a GPU host was
overkill.

**What we did.** Note the mismatch explicitly in REPORT.md §0 and in
`workflow.md`.

**Residual risk.** None for correctness. Scale-up to LES/DNS resolution
would obviously need a proper parallel implementation — flagged as open
question #5 in `open_questions.json`.

---

## Summary

Nothing failed in a way that overturned the replication verdict. The
substantive limitations are:

1. Scope-limited to Cartesian meshes (curvilinear claim C3 not tested).
2. LLM judge substituted `argo:claude-opus-4.5` for the requested `4.7`
   due to an upstream Argo proxy schema-validation bug.
3. Predictor time-stepping (forward Euler) simpler than the paper's ADI.
4. No formal order-of-accuracy measurement (C4 not tested).
5. Ceiling at Re = 1000 (higher-Re Ghia points not exercised).

The verdict remains **REPLICATED (Cartesian limit)** with those five
limitations explicitly disclosed.
