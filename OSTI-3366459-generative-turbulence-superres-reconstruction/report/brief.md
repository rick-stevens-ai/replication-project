# Brief

**Paper:** Oommen, Khodakarami, Bora, Wang & Karniadakis, "Learning turbulent flows with generative models for super resolution and sparse flow reconstruction," *Nature Communications* 17:3707 (2026). OSTI 3366459.

**Core claim tested:** Combining an operator-learning UNet with an adversarial loss (adv-NO) mitigates the spectral bias of a conventional L2-trained neural operator (NO) when super-resolving turbulent-flow fields, reducing energy-spectrum error at the cost of a small increase in point-wise (field) error.

**What we did:** Because the paper's Schlieren jet dataset is proprietary (Tsinghua), we generated a public proxy — 1,000 snapshots of 2-D forced Kolmogorov turbulence at 128×128 via our own pseudo-spectral DNS (RK4, vorticity form, 2/3 dealiasing) — then trained two matched UNets for 4× super-resolution (32→128): (i) L2-only ("NO analog") and (ii) L2 + PatchGAN + spatial-gradient feature loss ("adv-NO analog"). Both models: 60 epochs, Adam lr=1e-4, single A100.

**What we found:** Adv-NO reduced log-energy-spectrum NRMSE by 2.6× vs the L2 baseline (0.887 → 0.340 on the resolved band), while field NRMSE rose 30% (0.120 → 0.156). E(k=30) recovery: NO 4% of DNS, adv-NO 79% (19× improvement at that scale). Direction and mechanism match the paper exactly; the 15× reduction reported on Schlieren was not fully matched in magnitude (2.6× here) — expected given smaller model, shorter training, simpler feature loss, and different flow. **Verdict: PARTIAL.**
