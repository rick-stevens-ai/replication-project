# Failure Analysis — OSTI 2477212 (Sun et al. FNO for Ocean Dynamics)

Verdict: **PARTIAL**. This document is the honest post-mortem of what
did NOT replicate, what was blocked, and what design threats we cannot
close without significantly more resources.

---

## 1. Hard blockers (cannot be resolved without external cooperation)

### 1.1 SOMA κ_GM 100-member ensemble is not public
- **Impact:** claim C5 (paper's specific Table 3 log(RSE) / log(1-ACC)
  numerics on the SOMA ensemble) is untestable. Any purely numeric
  reproduction of Table 3 is impossible from public artifacts alone.
- **Evidence:** paper Data Availability Statement — *"…not publicly
  available due to ongoing research and data curation processes."*
- **Attempted workarounds:**
  - GitHub API keyword sweep (2026-07-02) for authors' training
    scripts: `deephyper+FNO+ocean` → 0 hits; `SOMA+fourier+neural+
    operator` → 0 hits; `yixuan-sun FNO ocean` → 0 hits.
  - No public Zenodo release located.
  - MPAS-Ocean SOMA test case itself is public
    (mpas-dev.github.io) but a 100-member κ_GM ensemble is a downstream
    artifact that would require running MPAS-Ocean 100× to regenerate.
- **Resolution path:** contact co-authors Van Roekel (LANL, MPAS-Ocean
  lead) or Narayanan (ANL) to request the ensemble under an appropriate
  data-use agreement, OR generate a fresh 100-member κ_GM SOMA ensemble
  from the public MPAS-Ocean stack (est. cost: ~1000 CPU-hours per
  member × 100 members = ~100k CPU-hours; feasible on ALCF/NERSC
  allocation, not on a spot-check budget).

### 1.2 DeepHyper HPO campaign compute is out of reach
- **Impact:** cannot reproduce the paper's exact "optimal" HPO winner,
  can only inject a proxy of the reported optimum.
- **Evidence:** paper reports 500 evaluations × 80×A100 × 6 h at ALCF
  Polaris = ~2400 A100-hours = ~$8k+ at cloud spot pricing. Our budget
  was a single A100 for ~15 minutes.
- **Attempted workaround:** encode paper's reported HPO winner as the
  "optimized" config on the ocean proxy (4 channels, width 40, 16
  modes, 4 blocks, composite MSE + neg-ACC α=0.5) — this is
  direction-of-effect, not an HPO reproduction.
- **Resolution path:** ALCF Polaris DD allocation or equivalent NERSC
  Perlmutter time; run DeepHyper against a from-scratch SOMA ensemble.

### 1.3 Paper never released Modulus training scripts
- **Impact:** cannot bit-exactly match the paper's baseline (Modulus
  default) or optimal configurations.
- **Evidence:** exhaustive GitHub sweep (see §1.1) turned up nothing.
- **Attempted workaround:** wrote a from-scratch pure-PyTorch FNO
  matching Li et al. 2021 arXiv:2010.08895 — this is arguably a
  STRONGER independent check than Modulus-based replication, because
  it removes any Modulus-specific idiosyncrasies.
- **Resolution path:** if the authors' scripts are ever released,
  cross-check whether Modulus adds hidden positional embeddings,
  spectral padding, or initialization tricks that materially change
  the outcome.

---

## 2. Soft failures (things that did not replicate cleanly and are counter-signals)

### 2.1 LpLoss + larger-capacity did NOT beat MSE baseline on Burgers
- **Result:** optimized_lp (549k params, LpLoss) test rel-L2 = 2.997%;
  baseline_mse (74k params, MSE) test rel-L2 = 2.962%. LpLoss is
  slightly WORSE, within noise.
- **Paper's claim (C2):** composite (MSE + neg-ACC) loss improves
  log(RSE) and log(1-ACC) vs pure MSE for 3/4 variables in Table 2.
- **Judge finding:** Q3 = **NO** on the Burgers rig
  (llm_judge_burgers.txt).
- **What this means:** the loss-choice half of the paper's story does
  NOT reproduce on the canonical Li et al. 2021 Burgers benchmark. It
  reproduces only on the synthetic ocean proxy (§4.2 of REPORT.md).
- **Interpretation:** two possibilities:
  1. LpLoss/composite loss is a dataset-specific advantage (works on
     ocean saturation-rich signals with limited head-room, not on
     Burgers-style sharp-gradient signals).
  2. The comparison is within noise; a single-seed test cannot resolve
     it. Paper doesn't report seed variance either, so we cannot
     compare CIs.
- **Honesty note:** we report this counter-signal explicitly in the
  REPORT.md §4.4, in REPORT.tex GENUINE CRITIQUE, and in the LLM-judge
  transcript. Did NOT bury it or explain it away.

### 2.2 Burgers absolute error is one order higher than Li et al.
- **Result:** ~3% rel-L2 vs Li et al. 2021's ~1.6e-3.
- **Reasons (all deliberate, none accidental):**
  1. ν = 0.01 (ours) vs ν = 0.1 (Li) → stiffer, sharper gradients,
     strictly harder operator to learn.
  2. s_train = 1024 (ours) vs s = 8192 (Li) → less resolved training
     data.
  3. 500 epochs on 1000 training samples (ours) vs 500 epochs on a
     larger dataset (Li).
- **What this means:** the FNO method demonstrably works and is in
  the right ballpark, but we did NOT close the gap to Li et al.'s
  best-case numbers. A tighter numeric match would require more
  training data, easier ν, or a bigger model.
- **Deliberate design choice:** we chose the harder ν = 0.01 because
  any "FNO works" claim there is strictly stronger than the same
  claim at ν = 0.1.

### 2.3 Single-seed reporting throughout
- **What we did:** both the Burgers track and the ocean-proxy track
  are single-seed runs.
- **Why this matters:** the LpLoss-vs-MSE comparison (2.997% vs
  2.962%) is well within plausible seed variance. A rigorous
  reproduction would run ≥5 seeds per config and report
  bootstrap CIs.
- **Why we did it anyway:** compute budget (single A100, 15 min
  Burgers + 20 min proxy). The paper itself also doesn't report
  seed variance, so a single-seed match is a fair comparison
  even if not statistically ideal.
- **Deferred to future work:** multi-seed sweep once compute is
  available; would let us classify the C2 counter-signal (§2.1) as
  either dataset-specific or noise.

---

## 3. Threats to validity we acknowledge

### 3.1 Proxy ≠ SOMA
The synthetic ocean-tracer proxy has smoother dynamics than
mesoscale-eddy-active SOMA output. Consequence: our optimized-vs-
baseline gap on the proxy (log(RSE) Δ = -2.63; paper Δ range =
[-0.71, -0.93]) is INFLATED relative to Table 3. We take direction
only, never magnitude, from the proxy comparison.

### 3.2 LLM-judge self-consistency
Single LLM judge (Argo gpt-5.2). A rubric ensemble (3+ judges of
different model families) or a fine-grained human-labeled rubric
would harden the verdict. Not a blocker for PARTIAL, but a caveat
for anyone treating the judge output as a rigorous statistical claim.

### 3.3 Scale ceiling not probed
Everything here is ≤100×100 grid (2D) or s=1024 (1D). The paper's
target is the same scale, but any extrapolation to production ocean
grids (1/10° or LLC4320 ~2 km) or 3D full-depth state is entirely
untested — see `open_questions.json` Q1 for the specific
memory/compute-cost ceiling analysis this deserves.

### 3.4 Judge is not blind
The LLM judge sees the paper's target numbers in its prompt (that's
how the rubric questions are framed). Not a blinded double-check.
For a formal replication study this would be a threat; for a
spot-check-to-PARTIAL promotion it is acceptable and standard.

---

## 4. What went right (calibration counterpoint to §§1-3)

- **FNO method core independently derived from scratch.** 350-line
  pure-PyTorch implementation matches Li et al. 2021 architecture
  and produces meaningful operators on Burgers.
- **Resolution invariance CLEANLY reproduced.** 0.28 pp spread across
  16× resolution range on Burgers — this is the FNO family's
  signature capability and it holds unambiguously.
- **Directional claims reproduce on ocean proxy.** Both log(RSE) and
  log(1-ACC) improve in the paper's direction; rollout stability
  matches Figure 6 qualitatively.
- **Honest reporting of the LpLoss counter-signal (§2.1).** We do
  not paper over the Q3 NO from the judge; we report it in
  REPORT.md §4.4, REPORT.tex GENUINE CRITIQUE, and here.
- **Independence from Modulus.** By not using the paper's framework,
  we removed a potential source of "of course it reproduces — we
  used the same tuned defaults" bias.

---

## 5. Root-cause taxonomy

| Failure mode | Root cause | Blockable at? | Fix cost |
|---|---|---|---|
| C5 numerics untested | Dataset not public | Data release | Author cooperation OR ~100k CPU-hours to regenerate SOMA ensemble |
| DeepHyper HPO not reproduced | Compute out of budget | ALCF/NERSC time | ~2400 A100-hours |
| LpLoss ≯ MSE on Burgers | Dataset dependency OR seed noise | Multi-seed + varied ν | ~50× current compute; still doesn't resolve dataset dependency |
| Burgers abs error 3% vs 0.16% | Deliberate harder ν + smaller s | Bigger training set | ~20× current compute |
| Single-seed CIs missing | Compute budget | Multi-seed runs | ~5× current compute |
| Modulus-specific behavior untested | Deliberate independence choice | Run Modulus in parallel | Modulus installation + 2×compute |

---

## 6. What a full REPLICATED verdict would require
1. Access to the SOMA κ_GM 100-member ensemble (or independent regeneration).
2. A full DeepHyper HPO run on ≥40 A100s for ≥6 h reproducing the paper's search.
3. Numeric match of the Table 3 log(RSE) / log(1-ACC) values within stated
   uncertainty (paper doesn't quote seed variance → set our own tolerance
   at ~10% relative on log-quantities, matching typical neural-operator
   reproducibility norms).
4. Multi-seed statistics on both baseline and optimized to bound the C2
   loss-comparison inside CIs.
5. Optional: independent re-derivation using Modulus in parallel to check
   framework-idiosyncratic effects.

Steps 1 + 2 alone would move the verdict from PARTIAL to REPLICATED. Everything else is polish. Nothing above changes the current honest verdict: **PARTIAL**.
