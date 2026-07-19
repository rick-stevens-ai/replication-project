# Workflow --- huang2022 (arXiv:2202.11348) replication

## Paper
Kai Huang, Ding-Fu Shao, Evgeny Y. Tsymbal, *Ferroelectric control of magnetic
skyrmions in two-dimensional van der Waals heterostructures*, arXiv:2202.11348.
System: Fe$_3$GeTe$_2$/In$_2$Se$_3$ (bilayer) and In$_2$Se$_3$/Fe$_3$GeTe$_2$/In$_2$Se$_3$
(trilayer) vdW heterostructures. Claim: ferroelectric polarization of In$_2$Se$_3$
controls the interfacial DMI in Fe$_3$GeTe$_2$, creating/annihilating skyrmions
(bilayer) and reversing their chirality (trilayer).

## Method class
DMI-stabilized skyrmion micromagnetics (interfacial DMI + FE/gate control).
Anchor: analytic critical DMI $D_c=(4/\pi)\sqrt{AK}$; the control knob (DMI) is
the swept variable. Distinct from scale-invariant Belavin--Polyakov skyrmions
because here DMI is essential and is what FE polarization tunes.

## Pipeline: acquire -> parse -> extract -> build -> run -> compare -> report
1. **Acquire.** PDF present: `textures-polar-huang2022.pdf` (3.7 MB, verified).
2. **Parse.** `pdftotext` (+ `-layout`) -> extraction artifacts. `marker`/`nougat`
   binaries absent; pdftotext used as documented interim (see extraction headers).
3. **Extract recipe.** Method = discrete-lattice micromagnetics (exchange +
   interfacial Neel DMI + uniaxial anisotropy), overdamped-LLG relaxation of a
   circular seed. No author code -> from-scratch rebuild. Key params from text:
   $D_\uparrow=0.28$, $D_\downarrow=0.06$, $D_{\uparrow\uparrow}=0.22$,
   $D_{\downarrow\downarrow}=-0.24$ mJ/m$^2$; adopted $K=0.04$ MJ/m$^3$;
   $60\times60$ nm supercell. $A$ only in Fig.4 (not in text) -> assumed 1 pJ/m.
4. **Build.** `work/skyrmion.py` --- square-lattice energy + effective field,
   sign-aware circular seed, overdamped-LLG relaxer, Berg--Luscher topological
   charge, reversed-core diameter, analytic $D_c$.
5. **Run.** `/home/stevens/comfyui-env/bin/python work/skyrmion.py` (60x60 grid,
   5000 steps/case, ~seconds). Live re-run during packaging reproduced the saved
   `huang2022_result.json` to the quoted digits.
6. **Compare.** $D_c=0.255$ mJ/m$^2$ brackets $D_\downarrow<D_c<D_\uparrow$ ->
   create/annihilate switch reproduced; $|Q|\approx1$ confirms skyrmions; size
   trend reproduced; absolute diameter ~2-3x high (unknown $A$).
7. **Report.** This 8-artifact package.

## Tools & versions
| Tool | Version / path | Role |
|------|----------------|------|
| Python | `/home/stevens/comfyui-env/bin/python` | run kernel |
| numpy | 2.3.5 | array math / relaxation |
| pdftotext (poppler) | `/usr/bin/pdftotext` | extraction interim |
| marker / nougat | NOT installed | (preferred extraction; absent) |
| pdflatex | NOT installed | (REPORT.tex ships as source) |

## Effort estimate
- Physics (build + run + verify): already complete prior to packaging (~1--2 h).
- Packaging (this pass): ~45 min --- extractions, evidence copy, 5 report
  artifacts, JSON validation, audit.

## Verdict
**PARTIAL** (mechanism REPLICATED). Coverage ~6/10, Agreement ~7/10.
