# Workflow — Replication of Kesharpu 2023 (arXiv:2305.13423)

Texture class: **polar**. Method class: **theory / su(2) path-integral → tight-binding**.

## 1. Inputs (pre-existing, read-only)
- `paper.pdf` — the source manuscript.
- `extraction/marker.md` — 4941-line full-text OCR extraction.
- `report/method_extract.md` — prior method summary.
- `META.json` — scaffold metadata.

## 2. Claim identification
Read `extraction/marker.md` sections II (Method), II A (S=1 Chern), II A 2 / III A
(general S, Eq. 7), III C (Haldane comparison, Eq. 11). Extracted the concrete,
computationally-reproducible headline claims:

1. **Eq. (5):** For S=1, `c1 = sgn[sin(q2x)]` — Chern number depends only on the
   azimuthal modulation q2x and flips sign as q2x crosses 0.
2. **THE sign-flip:** increasing the modulation vector flips the sign of the
   topological Hall conductivity σ^THE (Abstract + Sec. III A).
3. **Eq. (7) / Sec. III A:** for S≥2 a polar (q1x) factor `(1 + S g2/2 cos 2q1x)`
   formally appears but the paper concludes it is subdominant (g<1), so the Chern
   number "depends only on the azimuthal modulating vector q2x."
4. **Eq. (11) / Fig. 9:** a phenomenological sublattice mass M competes with the
   chiral mass — Haldane-model analogy, topological→trivial transition.

## 3. Model construction (`code/kesharpu2023_replication.py`)
- Built a self-contained two-band honeycomb Bloch Hamiltonian
  `H(k) = H0 I + Hx σx + Hy σy + Hz σz`.
  - **NN hopping** (A↔B) gives Dirac cones via `f(k)=Σ exp(i k·a_n)`;
    amplitude modulated by the polar vector q1 through the g'_n weights.
  - **NNN complex hopping** carries the **Haldane phase φ_n = S (q2·b_n)** — this
    is the paper's own Sec. III C statement that "S q2x plays the analogous phase
    accumulation role due to NNN hopping." The topological mass is
    `Hz = -2 t2 Σ sin(k·b_n) sin(φ_n)`, whose sign = sign of `sin(S q2x)`.
  - Optional sublattice mass **M** for the Eq. (11) test.
- **Convention note:** the paper's printed NN/NNN vectors and its stated Dirac
  point K=(π/√3,0) are not mutually consistent (OCR/sublattice-convention
  artifact). We adopted one self-consistent standard-honeycomb convention that
  carries the identical physics; documented in code + `failure_analysis.md`.

## 4. Chern-number evaluation
- **Fukui–Hatsugai–Suzuki (FHS)** plaquette method over an N×N BZ mesh
  (gauge-invariant, integer-robust). Reciprocal vectors from the primitive
  Bravais lattice. Default N=20 (claims), N=14 (phase-diagram figure).

## 5. Scoring
- Each claim → structured entry in `work/results.json` with paper_value,
  reproduced_value, match bool, note.
- Claim 1: sign-agreement fraction over a q2x scan (≥0.85 ⇒ match).
- Claim 2: count Chern sign flips across a q2x sweep (≥1 ⇒ match), ignoring
  gap-closing zeros.
- Claim 3: numeric Chern q1x-independence + analytic polar-factor |S g2/2|<1 in
  the well-defined lobe (|S q2x|<π).
- Claim 4: |c|=1 for small |M|, c=0 for large |M|.

## 6. Outputs
- `work/results.json` — structured results (saved incrementally so nothing is
  lost on timeout).
- `figs/chern_phase_diagram.png` — Chern number over (q1x, q2x) for S=1 and S=3
  (cf. paper Fig. 7).
- `report/REPORT.tex` (+ `REPORT.pdf` via pdflatex).

## 7. Environment
- CPU-only, Python 3, numpy 2.4.3 / scipy 1.18.0 / matplotlib.
- Total runtime ≈ 30 s (well under the 1200 s budget).
- Host: CherryRd (macOS). pdflatex available.

## Reproduce
```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/TEXTURE-polar-kesharpu2023
python3 code/kesharpu2023_replication.py
pdflatex -output-directory report report/REPORT.tex   # compile the report
```
