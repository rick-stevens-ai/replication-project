# Workflow: Replication of arXiv:1211.0762 (Zhang, Liu & Zhang 2012)

**Paper:** *Spin-orbital Texture in Topological Insulators*
**Method class:** analytic / effective $k\cdot p$ model-Hamiltonian (closed-form verification)
**Verdict:** REPLICATED — Coverage 8/10, Agreement 9/10

## Pipeline (acquire → parse → extract → build → run → compare → report)

1. **Acquire.** PDF already in the corpus dir (`textures-polar-zhang2012.pdf`, 576 KB, arXiv:1211.0762v1).
2. **Parse.** `pdftotext` (+ `-layout`) → interim text extractions (marker/nougat binaries absent — see below).
3. **Extract recipe.** Read the paper's Eqs. 1–10 directly; identified the model as the isotropic
   TI surface Dirac Hamiltonian + p-orbital-resolved first-order-in-k wavefunctions. **Key reading:
   the paper contains NO hexagonal-warping term** (contrary to the task framing) — replicated the
   actual paper.
4. **Build.** From-scratch Python (`zhang2012_replicate.py`): construct the 6-dim orbital⊗spin
   eigenstates |Φ±⟩ (Eqs. 4–5), the 6×6 projectors |p_i⟩⟨p_i|⊗s_η, and the projection tensor
   D^±_{i,η} (Eq. 6). No author code exists / was used.
5. **Run.** `/home/stevens/comfyui-env/bin/python zhang2012_replicate.py` — 24-point circular
   Fermi contour, <1 s runtime. Re-verified 2026-07-19: output identical to saved JSON.
6. **Compare.** Each paper formula (pz texture, Eqs. 7/8, 2θ orbital-diff, Eq. 10 polarization)
   asserted as max angular deviation. Machine-precision (~1e-16) on angular forms + correct
   signs/handedness. One exact factor-2 prefactor gap on the total in-plane spin magnitude
   (convention, not physics).
7. **Report.** 8-artifact package (this pass).

## Tools & versions

| Tool | Version / path | Role |
|------|----------------|------|
| Python | `/home/stevens/comfyui-env/bin/python` | solver interpreter |
| numpy | 2.3.5 | linear algebra (6-dim states, projectors) |
| scipy | 1.17.0 | available; not strictly needed here |
| pdftotext (poppler) | `/usr/bin/pdftotext` | interim text/math extraction |
| marker | **not installed** | would produce `extraction/marker.md` (prose) |
| nougat | **not installed** | would produce `extraction/nougat.mmd` (math) |
| pdflatex | **not installed** | REPORT.tex ships as source, compiles off-host |

## Effort estimate

- Physics build + verification: ~2–3 h (already complete before this pass).
- Packaging (this pass, 8 artifacts): ~1 h, mechanical.
- Total from-scratch to full package: ~half a day for an analytic k·p paper of this size.

## Reproduce block

```bash
cd /home/stevens/textures-100/corpus/textures-polar-zhang2012
/home/stevens/comfyui-env/bin/python zhang2012_replicate.py
# prints per-claim errors; writes zhang2012_checks.json
# compare against report/evidence/zhang2012_result.json (verdict + per-claim)
```
