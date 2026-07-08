# Attempt Log — QC-barren-plateaus-tensor-network (arXiv:2209.00292)

Chronological record. All times CDT, 2026-07-02.

1. **Selection.** Read WAVE_BRIEF + STATUS_AUDIT + QC100_CANDIDATES tsv. Confirmed the
   *tensor-network simulation* direction was completely untaken (grep of QC-100/ dirs +
   dedup list). Highest-ranked clean tensor-network barren-plateau paper with a reproducible
   classical-simulator core + OA = rank 28, arXiv:2209.00292. Created non-colliding target dir
   `QC-barren-plateaus-tensor-network-Liu2022/`.
   (Dir slug uses "Liu2022" as a placeholder tag from the wave naming convention; the actual
   authors are Cervero Martín & Lubasch, 2022/2023 — corrected throughout the report text.)

2. **Paper fetch.** Pulled abstract via arxiv.org/abs and full body via ar5iv.org (NOT the paid
   pdf tool). Extracted core claims: Thm 1 (McClean BP: E[grad]=0, Var∈O(c^-N)); Thm 2 (ZX-calculus
   per-term variance formula); main result = variance ~ exp(-distance-to-canonical-centre); qMPS
   linear distance → exponential in N (BP), qTTN/qMERA log distance → polynomial (trainable).

3. **Simulator build.** Wrote a from-scratch numpy statevector simulator: RX/RZ/RY/H/CNOT gates,
   tensordot-based 1q apply, flip-based CNOT. Validated: Bell state amps exact, <ZZ>=1, <Z0>=0,
   parameter-shift gradient of RX matches analytic -sin(θ) to 5 dp, CNOT correct for both
   control<target and control>target orderings and on 3-qubit registers.

4. **Iteration on experiment geometry (3 dead ends, all diagnosed):**
   - v1 (probe RZ centre gate vs Z observable): variances ~1e-33 (machine zero). Root cause: RZ on
     the |0> initial state commutes with Z observable → trivially zero gradient. Killed, fixed.
   - v2 (linear-chain qMPS, probe centre RX vs distant Z): still machine-zero for dist≥1. Root cause:
     single-CNOT-per-bond light cone does not carry the centre gate's derivative to distant Z
     (genuine causality zero, not decay).
   - v3 (probed RY as FIRST gate on |0>, grow blocks between it and observable): variance *increased*
     with distance (grew from zero as the cone reached the observable) — opposite geometry to a BP.
   All three failures logged as light-cone / 2-design-placement issues (see failure note below).

5. **Correct experiment (McClean geometry, qc_bp4.py).** Random deep hardware-efficient brickwork,
   depth L=N (2-design regime), probe a middle parameter, cost=<Z0 Z1>, 2000 samples. Local sanity
   at reduced samples showed monotonic exponential decay. Ran full on uicgpu (source ~/env.sh),
   PID 1372092, ~213 s. Result: Var vs N ln-linear slope -0.506, R^2=0.945, c=1.66; mean~0; depth
   control showed BP onset once cone reaches observable. Copied results.json + run.log + plot to
   evidence/.

6. **First LLM judge (argo:gpt-5.2):** PARTIAL, cov 6 / agr 7. Critique: the *distinctive*
   tensor-network distance result (qMPS vs qTTN scaling) was a projection, not a direct simulation.

7. **Strengthening (qc_bp5.py).** Built GENUINE qMPS (chain brickwork, depth~N) and qTTN (balanced
   binary tree of scrambled 2q blocks, depth~log2 N) circuits; observable at canonical centre so it
   stays in the cone (nonzero signal); measured Var[grad_centre] vs N directly. Ran on uicgpu
   PID 1374619. qMPS N=4..14 completed: ln(Var)=-0.381 N-1.62, R^2=0.893 (exponential in N).
   qTTN N=4,8 completed (0.102→0.039); N=16 single 16384-dim tree point exceeded ~30 min and was
   terminated for runtime — 2-point qTTN slope -0.24/qubit vs qMPS -0.38/qubit (qMPS 1.59x steeper),
   qTTN power-law exponent ~ -1.4. Direct dichotomy established.

8. **Second LLM judge (argo:gpt-5.2 + argo:claude-opus-4.8, both free Argo):** both PARTIAL.
   opus-4.8 cov 7 / agr 8. Consensus: core theorems corroborated in trend; qTTN under-sampled,
   qMERA not simulated, Thm 2 formula not re-derived symbolically.

9. **Wrote REPORT.md** with claims table, method, results-vs-paper, verdict PARTIAL.

## Failure note (for failure-log carry-over)
Barren-plateau numerical experiments are geometry-sensitive: differentiating a gate that (a) commutes
with the observable through the initial state, or (b) sits outside the observable's causal cone, yields
*machine-precision zero*, which is easy to mistake for "exponentially small variance." The correct BP
probe requires the differentiated gate embedded in a 2-design-approaching bulk with the observable
inside its light cone. Always sanity-check that the dist=0 / shallow-depth control gives a healthy O(0.1)
variance before trusting any decay curve.
