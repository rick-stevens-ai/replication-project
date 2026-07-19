# Workflow --- textures-polar-verga2014 (Verga 2014, arXiv:1409.0256)

## Pipeline
`acquire -> parse -> extract -> build -> run -> compare -> report`

This paper was replicated for its **static + scaling core** (a dynamics/mechanism
paper; the full coupled solver was scoped out per the wall-clock budget and the
`computational-replication-execution` skill's Verga2014 guidance).

## Steps taken

1. **Acquire.** `textures-polar-verga2014.pdf` (arXiv:1409.0256v2) already present
   in the paper dir (1.9 MB, valid PDF).
2. **Parse.** `pdftotext` (poppler `/usr/bin/pdftotext`) -> linear text
   (`textures-polar-verga2014.txt`, 1088 lines) and layout text
   (`extraction/_pdftotext_layout.txt`, 612 lines). **Marker and Nougat are NOT
   installed** on this host (`which marker` / `which nougat` -> not found), so the
   `extraction/marker.md` and `extraction/nougat.mmd` artifacts are **pdftotext-based
   interim** stand-ins (marker.md = readable text + recovered structure;
   nougat.mmd = hand-transcribed key equations in Mathpix-Markdown/LaTeX).
3. **Extract recipe.** Read the paper's model and closed-form results directly
   (BP skyrmion Eq. 8, exchange energy `4piJ` line 429, self-similar Eqs. 15-17).
   No LLM extraction call needed --- the checkable physics is three closed forms.
4. **Build.** From-scratch numpy code `verga2014_repl.py` (no author code exists):
   BP field builder, discrete Heisenberg exchange energy, Berg-Luscher lattice
   topological charge, and the exponent-balance linear solve. Mirrors the helpers
   in `computational-replication-execution/scripts/lattice_skyrmion_probes.py`.
5. **Run.** `/home/stevens/comfyui-env/bin/python work/verga2014_repl.py`
   (numpy). All checks complete in a few seconds on CPU; no heavy compute.
   *(Physics already reproduced prior to this packaging pass; not re-run.)*
6. **Compare.** Per-claim table in `REPORT.tex`: energy `4piJ` to <0.5% (lam=8-16),
   `Q=-0.980` correct sign, barrier-free collapse mechanism, exponents
   `alpha=1, beta=1/2` exact.
7. **Report.** 8-artifact package assembled (this pass).

## Tools / versions
- `pdftotext` (poppler-utils) --- `/usr/bin/pdftotext`
- Python: `/home/stevens/comfyui-env/bin/python` (numpy)
- marker: **not installed** (interim pdftotext used)
- nougat: **not installed** (interim pdftotext used)

## Compute target
`nuc13` / local CPU class (analytic + small-lattice numpy, L<=512 dense arrays).
No GPU/HPC needed for the replicated static+scaling core. The *unbuilt* coupled
Schrodinger+LL solver (open questions) would route to uicgpu (A100) for the
electron propagation and ALCF Crux for parameter sweeps.

## Effort estimate
- Static + scaling replication (code + verification): ~2-3 h equivalent.
- This packaging pass (8 artifacts + report): ~1 h.
- Unbuilt coupled solver (open Q1-Q5): estimated 1-2 days of focused build+run.
