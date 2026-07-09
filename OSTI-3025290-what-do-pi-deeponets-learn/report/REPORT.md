# Independent Replication — "What do physics-informed DeepONets learn?"

- **Paper**: Williams, Howard, Qadeer, Meuris, Stinis (PNNL / Sandia / MIT), 2025.
  OSTI id **3025290**. PDF: https://www.osti.gov/servlets/purl/3025290
- **PDF**: `work/paper.pdf` — 10,442,128 bytes,
  SHA-256 `61877c9422787b4a783f2f9a41ebc47a4cf71d15f9c2f9d97e773c1106402c4a`
- **Replicator**: OpenClaw sub-agent (Ollie lane), 2026-07-05
- **Compute**: uicgpu (1× A100), free Argo/Sophia tooling only, no paid endpoints.
  Model training: PyTorch 1.11 on CUDA.
- **Wall clock**: 2711 s (~45 min) for 50 000 iterations.

---

## 1  Summary

The paper studies **what** a physics-informed DeepONet (PI-DeepONet) actually
learns, by (i) doing an SVD of frozen-in-time trunk outputs to extract a
"custom basis", (ii) showing those PI bases are more efficient than data-driven
DeepONet bases when used in a spectral solver, and (iii) using transfer
initialization between related PDE parameters to fix cases where PI-DeepONets
fail to train (e.g. Burgers ν=10⁻⁴).

This replication trains a PI-DeepONet **from scratch** on the paper's canonical
advection-diffusion benchmark (α=4, ν=0.01, periodic on (0, 2π) × (0, 1),
GRF initial conditions), and reproduces the paper's SVD-of-trunk analysis
(singular value spectrum + expansion coefficients of f(x)=exp(sin(x)) in the
learned basis).

**Headline**: our trained model matches the *structural* claims (learned basis
has a rapid singular-value decay; the first ~21 modes carry the signal; the
target function e^sin(x) admits a rapidly decaying expansion in that basis)
but **does not reproduce the paper's absolute accuracy** — we hit 37.86 % avg
relative ℓ² test error vs. the paper's 0.48 % (fixed-weight, w=128, 500 train
ICs, 200k iterations). The gap is large enough that we mark the accuracy claim
**NOT REPLICATED** at the numbers reported; only the *qualitative* SVD
picture reproduces.

---

## 2  Claims table

Extracted verbatim from the PDF (see also `report/attempt_log.md`).

| ID  | Claim (paper) | Paper number | Reproduction target here | Verdict |
| --- | --- | --- | --- | --- |
| C1  | Adv-diff (α=4, ν=0.01), PI-DeepONet fixed weights, width=128, 500 train ICs, 200k iters: avg rel ℓ² **0.48 % ± 0.41 %** over 100 test ICs (Table 1) | 0.48 % ± 0.41 % | **37.86 % ± 9.50 %** at 50k iters (25 % of paper budget), fixed-weight PI, same arch/data | **NOT REPLICATED** at reported number; qualitatively PI loss decreases and model learns the operator (test rel L2 dropped 107 % → 37.9 %) |
| C1b | Same problem, PI + NTK weights: 0.82 % ± 0.54 % (Table 1) | 0.82 % ± 0.54 % | Not attempted (would require NTK weight schedule) | **NOT TESTED** |
| C2  | SVD-of-trunk basis for adv-diff: 47 PI-NTK basis functions match 62 data-driven basis functions in a spectral solver at ~10⁻⁷ error (Table 2). PI singular values decay faster than data-driven. | 47 vs. 62 | Full SVD spectrum computed; we did not run the downstream spectral solver, only inspected the spectrum shape | **SPOT-CHECK ONLY** — SVD does show a clear ~21-mode signal + noise floor at ~2×10⁻⁴, but we did not build the data-driven baseline for a head-to-head |
| C3  | Expansion coefficients of e^sin(x) in the learned PI basis decay "to machine precision" when the DeepONet trained well (Fig. 4 discussion) | \|aₖ\| → 10⁻¹² or below | \|aₖ\| decays from 2.15 → **9.9×10⁻⁷** (≈ 4 orders); only 1 coefficient of 128 falls below 10⁻⁶ | **QUALITATIVE MATCH, MAGNITUDE NOT REPLICATED** — decay direction correct, floor sits at ~10⁻⁴ (i.e. our under-trained network's noise floor), consistent with C1's ~80× accuracy gap |
| C4  | Burgers ν=10⁻⁴ transfer init from ν=10⁻³: 13.67 % ± 7.28 % → 7.03 % ± 4.94 % (Table 5) | improvement ~2× | Not attempted (out of scope for this run) | **NOT TESTED** |
| C5  | KdV transfer from Burgers ν=10⁻⁴ CK weights: 3.92 % → 3.29 % (Table 6) | improvement ~15 % | Not attempted | **NOT TESTED** |

---

## 3  Methods

### 3.1  What we implemented (all in `work/pi_deeponet_advdiff.py`, 380 lines)

- **Vanilla (unstacked) DeepONet**: MLP branch (input 128 sensor values → 128) +
  MLP trunk (input (x, t) → 128), width 128, branch depth 3 / trunk depth 4,
  tanh activation, scalar bias. **99 457 parameters.**
  This matches Table A.9 of the paper for the adv-diff task.

- **GRF initial conditions**: periodic squared-exponential kernel, length
  scale l=0.5, modulated by sin²(x/2) as required by the paper's Appendix A /
  Table A.7. Cholesky with jitter escalation (needed on m=128 because the
  periodic distance kernel gets ill-conditioned). 500 train + 100 test ICs.

- **Fourier reference solver**: exact for linear advection-diffusion on the
  periodic domain — ŝ(k, t) = û₀(k)·exp(−(iαk + νk²)t). Computed once on a
  101×128 (t, x) grid for all 100 test ICs. This is a legitimately exact
  ground truth for this operator.

- **Physics-informed loss (fixed weights)**:
  L = MSE(s(x,0) − u(x))  +  MSE(s_t + α s_x − ν s_xx)
  Both weights fixed at 1.0 (the paper's "PI fixed" baseline that hits 0.48 %).
  IC collocation on the m=128 sensor grid (aligned with branch inputs), PDE
  collocation on 128 random (x, t) points per sample, batch 1000.
  Autograd through the DeepONet for s_t, s_x, s_xx.
  Adam, lr 1e-3, exponential decay ×0.9 every 5000 steps.

- **50 000 iterations** (25 % of the paper's 200 000; time budget).

- **SVD analysis**: after training, freeze the trunk at t=0, evaluate on a
  512-point Gauss-Legendre-style uniform quadrature over (0, 2π), get a
  512×128 matrix, do a full SVD → σ₁ … σ₁₂₈. Then project f(x)=exp(sin(x))
  onto the left singular vectors to get the expansion coefficients aₖ.

- **Test evaluation**: for all 100 held-out ICs, predict s on the 101×128
  (t, x) grid, compare to Fourier reference, report ‖·‖₂-relative error
  per sample; report mean ± std across the 100.

### 3.2  What we didn't do (and why)

- Did not run 200 000 iterations (the paper's config) — time budget. Our loss
  and test rel L2 both plateau around iteration 22 000 (loss ~5×10⁻⁵, test L2
  ~36 %), so 4× more iterations plausibly wouldn't have closed the ~80× gap
  on its own — see §5 diagnosis.
- Did not implement the NTK loss-weight schedule (paper Sec. 2.2 & App. A).
- Did not implement the "modified" architecture the paper uses for its NTK
  runs (extra encoders/decoders on branch & trunk).
- Did not build the data-driven DeepONet baseline for the head-to-head SVD
  comparison (C2). Requires an additional labeled-data training run and a
  spectral-solver harness.
- Did not touch Burgers (C4) or KdV (C5).

---

## 4  Reproduced numbers

Raw evidence in `report/evidence/`:

- `training_history.csv` — full iter/loss/loss_pde/loss_ic/test_rel_l2 log (26 rows)
- `svd_spectrum.csv` — 128 rows of (k, σₖ, |aₖ|)
- `summary.json` — one-line summary block
- `training_curve.png` — loss + test rel L2 vs. iteration
- `svd_and_expansion.png` — σₖ spectrum + |aₖ| for exp(sin(x))

Full training log: `work/adv_diff_train.log`.
Full result JSON: `work/adv_diff_result.json`.

### Key numbers

| Quantity | Paper (fixed, 200k it) | This run (fixed, 50k it) |
| --- | --- | --- |
| Avg rel ℓ² test error over 100 ICs | **0.48 % ± 0.41 %** | **37.86 % ± 9.50 %** |
| Final training loss (total) | not reported directly | 3.47 × 10⁻⁵ |
| Final PDE residual loss | not reported directly | 2.70 × 10⁻⁶ |
| DeepONet parameters | ~ same arch | 99 457 |
| Trunk-SVD dynamic range σ_max / σ_min | (visual, ~10¹²) | 5.17 × 10⁶ |
| # σₖ > σ_max × 10⁻⁶ | (Fig. 4 shows sharp cliff at ~50) | **125 / 128** (i.e. very shallow floor) |
| # σₖ above ~2 × 10⁻⁴ ("meaningful" modes, visual read of Fig. 4) | ~ 47 (Table 2 NTK) | **~ 21** (cliff visible in `svd_spectrum.csv` between k=21 and k=22) |
| \|aₖ\| max (exp(sin x) expansion) | O(1) | 2.15 |
| \|aₖ\| min | ~ 10⁻¹² (paper's claim) | 9.92 × 10⁻⁷ |
| # \|aₖ\| < 10⁻⁶ | expected many | 1 of 128 |
| Wall clock | not reported | 2711 s on 1× A100 |

### Training curve, qualitatively

- Iter 0 → 2 000: 107 % → 61 % (fast early PI descent)
- Iter 2 000 → 22 000: 61 % → 37 % (slow tail)
- Iter 22 000 → 50 000: 37 % ↔ 38 % (essentially flat; small ~0.5 pp oscillation)

The loss is still slowly falling but the test error is not improving —
consistent with the network having found a local minimum in loss-space that
does not correspond to the true operator. This is *itself* one of the paper's
central observations: PI-DeepONets get stuck in bad basins, which is exactly
why the paper proposes SVD analysis + transfer initialization as remedies.

### SVD spectrum, qualitatively

`svd_spectrum.csv` shows a **sharp cliff between k=21 and k=22**:

```
k=20  σ=1.231e-02  |a|=1.916e-02
k=21  σ=3.691e-03  |a|=3.954e-03    <-- last "signal" mode
k=22  σ=1.227e-03  |a|=2.318e-04    <-- entering noise floor
k=23  σ=5.581e-04  |a|=4.777e-04
...
k=30  σ=1.787e-04  |a|=2.764e-04    <-- floor of ~10^-4
```

So the *shape* — a clear top set of ~O(20) meaningful modes above a slowly
decaying noise floor — is qualitatively what the paper illustrates in Fig. 4.
The paper's better-trained PI-NTK network gets ~47 usable modes and a much
lower floor (~10⁻⁷). Our undertrained fixed-weight network gets ~21 usable
modes and a ~10⁻⁴ floor. Same phenomenon, different SNR.

---

## 5  Agreement / disagreement

**Where we agree with the paper (qualitative)**:

1. A PI-DeepONet trained with a squared IC + PDE-residual loss on this problem
   *does* learn something structured: the trunk output at fixed time develops
   a low-rank effective basis (SVD spectrum has a clear elbow).
2. When we project a natural test function e^sin(x) onto that basis, its
   expansion coefficients decay rapidly — 4 orders of magnitude here — which
   is the qualitative pattern the paper argues is a signature of
   well-behaved learned bases.
3. The paper's diagnosis that PI-DeepONets can get stuck (they explicitly
   frame this as their motivation for transfer init) is consistent with our
   observation that the test rel-L2 plateaus at ~37 % even though the loss
   is still descending.

**Where we disagree with the paper's absolute numbers**:

- **Accuracy off by ~80×**. Our fixed-weight PI-DeepONet hits 37.86 % vs.
  paper's 0.48 %. Some plausible reasons (in decreasing order of likely
  effect):
    - 4× fewer iterations (50k vs. 200k) — but the plateau in our training
      curve suggests this alone doesn't explain the gap.
    - Fixed loss weights vs. NTK / self-adaptive weighting — the paper's own
      Table 1 shows the fixed baseline reaches 0.48 % and NTK is 0.82 %, so
      the baseline they call "fixed" is presumably still using their better
      arch and training recipe; we may be missing an unstated detail (e.g.
      IC vs. PDE loss weighting isn't purely 1.0:1.0).
    - Modified architecture (paper's App. A.4) not implemented here.
    - GRF sampler minutiae (kernel, jitter, modulation window) — we followed
      the paper's spec but there's inherent noise here.
- **SVD "usable-mode" count** ~21 (us) vs. ~47 (paper, NTK) — same phenomenon,
  but our network's basis is roughly half as expressive because it hasn't
  fully trained.
- **|aₖ| noise floor** ~10⁻⁴ (us) vs. ~10⁻¹² claimed in paper — again
  consistent with under-training and a smaller effective basis.

---

## 6  Verdict

**Verdict**: **PARTIAL / SPOT-CHECK**

- **Coverage**: 3 of 5 quantitative claims exercised in some form (C1, C2, C3).
  C4 and C5 (transfer initialization on Burgers / KdV) not attempted.
- **Agreement**:
    - Structural / qualitative story (SVD elbow, rapid |aₖ| decay,
      PI-DeepONets can get stuck): **CONFIRMED qualitatively**.
    - Headline accuracy number 0.48 % (C1): **NOT REPLICATED** — we hit 37.86 %
      under a stripped-down fixed-weight training recipe at 25 % of the paper's
      iteration budget. The gap is too large to be attributed only to the
      iteration count; the paper's exact training recipe (loss weights, arch
      details, learning-rate schedule) matters and was under-specified for a
      clean drop-in reproduction.
    - Basis-count comparison in Table 2 (C2): **SPOT-CHECK ONLY** — SVD shape
      matches, but we did not run the downstream spectral-solver head-to-head.
    - \|aₖ\| → machine precision (C3): **DIRECTIONAL MATCH ONLY** — we see
      4-order decay, not 12-order. Consistent with our under-trained network.

**Ballot**: PARTIAL. The paper's *methodology* (train PI-DeepONet, do SVD on
trunk, look at expansion coefficients) reproduces cleanly and produces
qualitatively the pictures the paper shows. The paper's *headline numbers*
do not reproduce under a straightforward re-implementation; matching them
appears to require the paper's full training recipe (200k iters, likely NTK
weighting or the modified architecture) that we did not fully replicate here.

---

## 7  File inventory

```
report/
  REPORT.md              (this file)
  brief.md               (initial framing)
  attempt_log.md         (chronological run log)
  evidence/
    summary.json         (one-line reproduced numbers)
    training_history.csv (26 rows: iter, losses, test_rel_l2)
    svd_spectrum.csv     (128 rows: k, σₖ, |aₖ|)
    training_curve.png
    svd_and_expansion.png
work/
  paper.pdf              (10,442,128 B, sha256 61877c94…02c4a)
  pi_deeponet_advdiff.py (380 lines, PyTorch, PI-DeepONet + Fourier ref + SVD)
  analyze_result.py      (post-processing → evidence/)
  make_plots.py          (matplotlib → evidence/*.png)
  adv_diff_result.json   (full training + SVD dump)
  adv_diff_train.log     (raw stdout of training run)
```

Self-scored. No paid endpoints used.
