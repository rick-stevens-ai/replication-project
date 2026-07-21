# Workflow --- textures-polar-verga2014 (Verga 2014, arXiv:1409.0256)

## Pipeline
`acquire -> parse -> extract -> build -> run -> compare -> report`

This paper is a **dynamics/mechanism** paper. It has been replicated in two passes:
(1) the **static + scaling core** (BP energy, topological charge, self-similar
exponents), then (2) a **coverage-flip pass** that BUILDS the full coupled
Schrodinger + Landau-Lifshitz time integrator and reproduces the DYNAMIC
current-driven collapse.

## Steps taken

1. **Acquire.** `textures-polar-verga2014.pdf` (arXiv:1409.0256v2) present (1.9 MB).
2. **Parse.** `pdftotext` (poppler) -> `textures-polar-verga2014.txt` (1088 lines)
   + layout text. **Marker/Nougat NOT installed** -> `extraction/marker.md` and
   `extraction/nougat.mmd` are pdftotext-based interim stand-ins.
3. **Extract recipe.** Model read directly from the paper: electron Hamiltonian
   Eq. 2 (tight-binding + Peierls phase from E-field + Js S.sigma + Bp.sigma),
   Landau-Lifshitz Eq. 3 with STT `Js s` and exchange dissipation `d=beta grad^2 f`
   (Eq. 7), BP seed Eq. 8, self-similar Eqs. 15-17, params line 205
   (Js=1, J=0.4, alpha=Bp=ne=0.1, E=1e-3, L=128, lambda=20), paper collapse
   times t* = 5936/1748/1236 for beta = 0.001/0.01/0.1 (Fig. 3).
4. **Build (static).** `work/verga2014_repl.py` --- BP field, discrete exchange
   energy, Berg-Luscher charge, exponent-balance solve.
5. **Build (dynamic, THIS pass).** `work/verga2014_coupled.py` --- coupled solver:
   - **Electrons (Schrodinger):** 2nd-order Strang operator-splitting,
     norm-conserving. Kinetic term diagonal in k-space via FFT with the
     time-dependent Peierls phase eps_k(t) = -2[cos(kx - E t) + cos(ky)]; local
     spin term h_i = -(Js S_i + Bp).sigma exponentiated analytically (2x2
     rotation). Itinerant Fermi sea reduced to a single spin-coherent field
     (mean-field), density ~ne, keeping the self-consistent coupling.
   - **Spins (Landau-Lifshitz):** classical RK4 of
     dS/dt = S x (f - alpha S x f + Js s) - beta grad^2 f, with f = J grad^2 S.
   - Seed = relaxed BP skyrmion; measure Q(t), core size(t), t*.
6. **Run.**
   - Static: `/home/stevens/comfyui-env/bin/python work/verga2014_repl.py` (seconds).
   - Dynamic: `.../python work/verga2014_coupled.py` --- 7 coupled runs
     (baseline + 3-beta dissipation scan + 3-lambda scaling scan) in **122 s**
     wall on CPU (L=48, dt=0.1, up to 6000 t0). Save-early to result JSON.
7. **Compare.** Per-claim tables in `REPORT.tex`: static (energy 4piJ <0.5%,
   Q=-0.980, exponents 1 & 1/2) + dynamic (Q:-1->0 collapse; t* decreases with
   beta; t* increases ~linearly with lambda0; sqrt shrink law).
8. **Report.** 8-artifact package updated (this pass).

## Tools / versions
- `pdftotext` (poppler-utils) --- `/usr/bin/pdftotext`
- Python: `/home/stevens/comfyui-env/bin/python` (numpy + numpy.fft)
- marker / nougat: **not installed** (interim pdftotext used)

## Compute target
`nuc13` / local CPU class. The coupled solver runs in ~2 min on CPU at L=48 via
the mean-field electron reduction + FFT kinetic propagation. Scaling to the
paper's full-spectral L=128 electron sea (exact t* ~ 5936 t0) and the Fig. 4
b-field maps / Fig. 3 full Q(t) family would route to uicgpu (A100); the
(lambda0, Bp, ne, beta) phase-boundary sweep (open Q5) fans out to ALCF Crux.

## Effort estimate
- Static + scaling replication: ~2-3 h equivalent.
- Coupled dynamic solver build + run + verify (this pass): ~2-3 h equivalent.
- Remaining fine-detail (full-spectral L=128 exact t*, b-field maps, f(X)
  profile, phase sweep): estimated 1-2 days of focused build+run.
