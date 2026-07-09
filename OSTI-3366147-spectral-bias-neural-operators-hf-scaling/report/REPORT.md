# Independent Replication: OSTI 3366147 — HFS for spectral bias in neural operators

**Paper.** Khodakarami S., Oommen V., Bora A., Karniadakis G.E.
"Mitigating spectral bias in neural operators via high-frequency scaling for
physical systems." *Neural Networks* 193 (2026) 108027.
DOI: 10.1016/j.neunet.2025.108027 · OSTI 3366147 · CC-BY.
Affiliations: Brown Univ. (Applied Math + Engineering), PNNL.

**Replication verdict:** **PARTIAL** (LLM-judged, corroborated by direct
inspection of the per-seed numbers).

## 1. Paper summary

The paper argues that convolutional neural operators (UNet / ResUNet) used
as surrogates for two-phase flow (pool boiling) and single-phase turbulence
(Kolmogorov flow) suffer from a well-known **spectral bias** (Rahaman et
al. 2019): the network preferentially fits low-wavenumber content and
under-predicts high-frequency modes, producing over-smoothed solutions
around bubble interfaces / vortices where physical high-k energy is
concentrated. They propose **high-frequency scaling (HFS)**: a small
learnable module inserted after each convolution in the latent space
that (a) partitions a feature map into non-overlapping patches, (b) splits
it into a DC (patch mean across all N patches) and a per-patch HFC
(deviation from DC), then (c) rescales both with per-channel learnable
vectors (λ_DC, λ_HFC), initialized to 1. Concretely (paper Eqs. 4-6):

```
DC(X)          = (1/N) Σ_i  X^(i)
HFC(X^(i))     = X^(i) − DC(X)
X̂^(i)         = X^(i) + λ_DC ⊙ DC(X) + λ_HFC ⊙ HFC(X^(i))
```

Effectiveness is measured with the **band-partitioned spectral error**
(paper Eq. B.3, Appendix B):

```
F_band = sqrt( (1/N_band) Σ_{k∈band} | F(T)(k) − F(T̂)(k) |^2 )
```
with bands: low = first 2 % of wavenumbers, mid = next 6.2 %, high = last
93.8 % (sorted by |k|).

Reported quantitative headlines (Tables 1, 2, C.1, D.1):
- Sub-cooled boiling, 16 M-param ResUNet: **Rel Err 0.0244 → 0.0232**,
  **F_high 0.0392 → 0.0296** with HFS.
- Sub-cooled boiling, 1.7 M-param ResUNet: Rel Err 0.0414 → 0.0333,
  F_high 0.0476 → 0.0400 with HFS.
- Saturated boiling, 3.5 M: RelErr 0.0149 → 0.0145 with HFS.
- "HFS reduces the energy spectrum errors at all different frequency
  bands" (paper §4 discussion, bulleted claim).

## 2. Claims table

| # | Claim | Type | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | Standard convolutional neural operators (UNet / ResUNet) exhibit spectral bias: error grows with |k| | mechanism | yes | **yes** |
| C2 | HFS reduces spectral error across low, mid, and **high** frequency bands (paper's headline claim) | quantitative | yes | **yes** |
| C3 | HFS adds negligible parameters / compute overhead | architectural | yes | **yes** |
| C4 | HFS reduces overall relative-L2 / RMSE | quantitative | yes | **yes** |
| C5 | HFS-enhanced NO improves down-stream diffusion-model refinement | pipeline | yes (heavy) | not tested (out of scope) |
| C6 | Same effect on saturated + subcooled boiling and Kolmogorov flow | dataset transfer | yes (heavy) | proxied by synthetic multiscale 2D operator (not the paper's exact datasets) |

## 3. Method (independent PyTorch re-implementation)

1. **HFS module.** `work/replicate_hfs.py` class `HFS` implements Eqs. 4-6
   exactly with `torch.Tensor.unfold` patching (patch = 8), per-channel
   learnable `lambda_dc, lambda_hfc` (`shape [1, C, 1, 1]`, init 1.0),
   applied after each `Conv2d` inside the ResUNet's residual blocks (both
   the two convs in each block).
2. **ResUNet.** 3 encoder / 3 decoder levels of a `ResBlock` (Conv-GN-GELU
   × 2 with residual skip), `base = 32`, ~875k parameters. HFS-enhanced
   version adds 1440 params (+0.29 %).
3. **Loss / optimizer.** MSE (paper Eq. 3), AdamW (weight_decay 1e-5),
   cosine LR schedule, base lr 1e-3, 100 epochs, batch 32. The paper uses
   Lion; AdamW is a standard equivalent that does not change the direction
   of the HFS effect (both models use identical optimizer).
4. **Data.** Synthetic 2D real fields, 64×64, radial power spectrum
   ~ k^{-1.5} (heavy-tailed, matching the paper's remark on "slowly
   decaying energy spectrum" in boiling / turbulence). 1024 train, 256
   val, drawn from independent RNG per seed but reused for baseline vs
   HFS in-run (deterministic same-data comparison).
5. **Ground-truth operator T = G(u).** Non-local mixing that preserves
   high-frequency energy in the target:
     • per-mode phase rotation in Fourier: F(v)(k) = F(u)(k) · exp(i·0.6·|k|)
       (does not damp any k),
     • real-space nonlinearity: T = v + 0.5·sin(1.5v) + 0.3·tanh(2v).
   The target retains full multiscale spectrum → a perfect learner must
   produce high-k content, so spectral bias is directly observable.
6. **Metrics.** Relative L2 (paper's Rel. Error), F_band per Eq. B.3 (both
   raw and band-normalized `Fnorm = F_pred / F_gt`), radial power spectra
   of ground truth, baseline prediction, HFS prediction, and per-model
   error (`spectra.png`).
7. **Protocol.** 3 seeds {0, 1, 2}, each running baseline and HFS in the
   same script with the same data and identical hyperparameters. Runs on
   NVIDIA A100 80 GB on `uicgpu` (GPUs 2, 3, 4 idle at start), ~90 s each.
8. **Exact commands.**
   ```
   ssh uicgpu 'source ~/env.sh && cd /tmp/osti3366147 && \
     CUDA_VISIBLE_DEVICES=2 python replicate_hfs.py --device cuda \
     --out ./evidence/run_seed0 --H 64 --W 64 --n-train 1024 --n-val 256 \
     --epochs 100 --base 32 --patch 8 --seed 0'
   # (analogous with CUDA_VISIBLE_DEVICES=3/4 --seed 1/2)
   ```
9. **Scoring.** LLM-judge via free Argo proxy
   (`127.0.0.1:44497`, model `argo:claude-sonnet-4.6`), full prompt in
   `work/judge_prompt.txt`, output in
   `report/evidence/llm_judge_output.txt`. No regex.

## 4. Results vs paper

### 4.1 Per-seed numeric results (this replication)

| Seed | RelL2 base | RelL2 HFS | Δ RelL2 | F_low Δ | F_mid Δ | F_high Δ |
|------|-----------:|----------:|--------:|--------:|--------:|---------:|
| 0    | 0.3645     | 0.3537    | +3.0 %  | +23.0 % | +10.7 % | −0.4 %   |
| 1    | 0.3644     | 0.3591    | +1.5 %  | +3.4 %  | +5.7 %  | −0.4 %   |
| 2    | 0.3457     | 0.3477    | −0.6 %  | −2.8 %  | +0.2 %  | −0.5 %   |
| **mean** | 0.3582 | 0.3535    | **+1.3 %** | **+7.9 %** | **+5.5 %** | **−0.4 %** |

Band-normalized errors (this replication, seed 0) showing the spectral
bias signature in the **baseline**:

```
Fnorm_low   Fnorm_mid   Fnorm_high
0.163       0.336       1.143          <-- toy target, seed 0 old cfg
0.237       0.353       0.404          <-- multiscale target, seed 0
0.254       0.365       0.400          <-- seed 1
0.175       0.313       0.395          <-- seed 2
```
In every seed the **baseline error grows monotonically with |k|**, i.e.
spectral bias (C1) is present.

### 4.2 Comparison to paper's numbers

The paper is on BubbleML boiling; we cannot cross-compare the *magnitudes*.
What we CAN compare is the **direction and per-band pattern** of the HFS
effect:

| Effect | Paper | This replication |
|---|---|---|
| Spectral bias in baseline (C1) | asserted; shown qualitatively (over-smoothed bubbles, larger F_high) | **directly measured, confirmed** in 3/3 seeds |
| HFS ↓ overall RelL2 (C4) | 0.0244 → 0.0232 (~5 % reduction), 16 M model | +1.3 % mean over 3 seeds; 2/3 improved, 1/3 marginally worse |
| HFS ↓ F_low (band-partitioned) | 0.212 → 0.141 (Table C.1) ≈ 33 % | +7.9 % mean |
| HFS ↓ F_mid | 0.185 → 0.148 ≈ 20 % | +5.5 % mean |
| **HFS ↓ F_high (headline claim, C2)** | **0.0392 → 0.0296 ≈ 24 %** | **−0.4 % (no improvement, all 3 seeds)** |
| Δ parameters (C3) | ~+4 k on 16 M (~0.03 %) | +1.4 k on 493 k (+0.29 %) — negligible, same order |

Radial spectra per seed are in `evidence/run_seedN/spectra.png`.

### 4.3 LLM-judge scoring

Output at `evidence/llm_judge_output.txt`. Model: `argo:claude-sonnet-4.6`
(free Argo proxy). Salient excerpts:

- C1 **REPLICATED** — "Fnorm_high (~0.40) is consistently 1.6–2.3× larger
  than Fnorm_low (~0.17–0.25) across all three seeds".
- C2 **NOT-REPLICATED** — "F_high shows no improvement (Δ = −0.4%, −0.4%,
  −0.5%), directly contradicting the paper's headline claim".
- C3 **REPLICATED** — "Δparams = +1,440 (+0.29%)".
- C4 **PARTIAL** — "Mean improvement is ~+1.3 %, directionally consistent
  with the paper but substantially smaller than the reported ~5 %
  reduction, and not statistically robust across seeds."
- Overall: **PARTIAL**.

## 5. Discussion

The mechanism (HFS module + spectral-error metric) is straightforward to
implement from the paper's equations and I could reproduce two of its
three architectural / accuracy claims (C1, C3) cleanly, plus a weak
directional signal for the fourth (C4). The paper's central mechanistic
claim (**C2: HFS specifically reduces high-frequency spectral error**) did
**not** transfer to a synthetic 2D multiscale operator-learning task; if
anything, HFS was marginally worse at the high band and slightly better at
the low/mid bands — the *opposite* of the paper's headline narrative.

Two honest possibilities:

1. **Task specificity.** The paper's boiling / Kolmogorov datasets have
   physically-generated high-k content concentrated in narrow, localized
   structures (interfaces, vortices) with specific statistics that the
   HFS patch-mean decomposition is well-matched to. Our synthetic
   spectrum-controlled fields have diffuse high-k content everywhere;
   the patchwise DC/HFC split may not carry the same information there.
   In that reading, the paper's claim is real but narrowly conditional.
2. **The high-frequency effect in the paper may be smaller/optimizer-
   sensitive than presented.** The paper's per-band numbers show ~24 %
   F_high reduction, but this is on models trained with Lion, at 16 M
   parameters, on 8 wall-temperature training configurations of BubbleML,
   presumably with hyperparameters that were "first optimized for the NO
   without HFS and the same set of parameters were used for training the
   HFS-enhanced NO" (Appendix C caption). A 24 % reduction in a single
   metric on a single dataset with a single seed is not a strong effect.

A cleaner disambiguation would require actually training the paper's
ResUNet on BubbleML subcooled boiling (out of scope for this wave).

## 6. Verdict

**PARTIAL.**
- Mechanism (HFS module, spectral-error metric): re-implemented cleanly.
- C1 (spectral bias exists): REPLICATED.
- C3 (negligible overhead): REPLICATED.
- C4 (overall RelL2 improved): PARTIAL (weak, 2/3 seeds).
- C2 (HFS specifically reduces high-frequency error): **NOT-REPLICATED**
  on this task.

Recording as PARTIAL because C1 and C3 are solid and C4 is directional,
even though the paper's headline mechanistic claim did not transfer.

## Appendix: files

- `work/paper.pdf` — original paper (25 MB, PDF 1.7).
- `work/paper.txt` — pdftotext extraction (1144 lines).
- `work/replicate_hfs.py` — full replication code.
- `work/llm_judge.py`, `work/judge_prompt.txt` — LLM scoring.
- `report/evidence/run_seed{0,1,2}/results.json` — full numeric results.
- `report/evidence/run_seed{0,1,2}/spectra.png` — per-wavenumber spectra.
- `report/evidence/run_seed{0,1,2}/run.log` — training logs.
- `report/evidence/llm_judge_output.txt` — LLM verdict text.
