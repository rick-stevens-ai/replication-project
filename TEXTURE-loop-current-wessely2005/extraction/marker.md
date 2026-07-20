# Extraction Marker — arXiv:cond-mat/0511224

- **Title:** Current driven magnetization dynamics in helical spin density waves
- **Authors:** Ola Wessely, Björn Skubic, Lars Nordström (Uppsala University)
- **Ref:** arXiv:cond-mat/0511224v2 → Phys. Rev. B 73, 144431 (2006)
- **Extraction method:** `pdftotext -layout paper.pdf work/paper.txt` (266 lines). Vision/PDF-model credit not required; layout text was clean enough for equations and the C matrix.

## Classification audit (IMPORTANT)
- **Assigned class:** loop-current (kagome flux-phase).
- **Actual content:** spin-transfer torque (STT) in a **helical spin density wave / spin spiral**. Current along the spiral axis rigidly rotates ("slides") the spiral.
- **Verdict: MISCLASSIFIED.** No orbital/loop current, no Peierls flux, no kagome lattice, no TRS-breaking kinetic term. The shared `loop_current_kagome_kernel.py` is **not applicable** and was **not imported**. We replicated the actual in-scope core (STT in a spin spiral) with real, runnable tight-binding code instead.

## Central claims (verbatim-grounded)
1. A charge current along the spiral axis of a helical SDW exerts a spin-transfer torque that rigidly rotates/translates the spiral (bulk effect, unlike interfacial multilayer STT).
2. Torque–current tensor (Eq. 6) for Er, moment ∥ [100], q ∥ [001]:
   `C = ħ · [[0,0,0],[0,0,0.5],[0,0,0]] Å²` — only current ∥ axis drives rotation.
3. Microscopic (DFT C-matrix) result: 10⁷ A/cm² → spiral precesses at **0.07 GHz**.
4. Crude analytic estimate → rotation freq = (P q A)/(4 J e); gives **~4×** the C-matrix value ("catches the order of the effect").
5. FS spin polarization P ≈ −0.5 ⟹ conduction spins tilted **30°** from spiral axis.
6. Per-layer coherent spin rotation: transverse spin advances **q·π rad per layer** (q in 2π/c units); q = 0.20·2π/c minimizes energy for Er.
7. Rotation frequency scales **linearly** with current (above an anisotropy critical current).

## Machine-checkable claims selected (5)
- C1: single-nonzero-component structure of C (axis current ⟹ rotate-spiral torque; out-of-plane spin flux vanishes for a planar spiral).
- C3: |P|=0.5 ⟹ 30° tilt (arithmetic + geometry).
- C4: q=0.20·2π/c ⟹ 0.20·π rad per atomic layer.
- C5: linear scaling f_rot ∝ j.
- C6: crude-vs-microscopic order-of-magnitude ratio (paper claims ~4×).

## Not reproduced (honestly flagged)
- Absolute 0.07 GHz and the numeric C₂₃=0.5 ħ Å²: these come from FP-APW+lo LSDA DFT of Er (Eq. 8 band-resolved Q tensor, 41³ k-mesh). We do **not** run DFT. We verify convention-independent structural/scaling claims with a minimal spin-spiral tight-binding model (generalized Bloch theorem), which is the genuine in-scope mechanism.
