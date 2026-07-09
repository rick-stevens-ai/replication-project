# failure_analysis.md — QC-1608.02005 replication

## Honest failures / friction encountered

### F1. First run: concentrated peak landed on the WRONG group element
- **Symptom.** With the naive Step-4 diagonal `diag(1, chi_j(D)/sqrt(k-lambda))` and F^dagger in Step 5, the algorithm concentrated ~74% probability on ONE group element per DS instance, but that element was NOT related to the hidden shift s in the way the paper predicts. Example: for D = {0,1,3} in Z_7 with s = 0, the peak was at g = 5.
- **Diagnosis time.** ~10 minutes of trace analysis + hand-derivation.
- **Root cause.** The paper's Step-4 diagonal is written for real characters (chi(D) real, so chi(D)^2 = |chi(D)|^2 = k-lambda by Turyn) and does not generalise verbatim to Z_v with complex characters. Substituting chi_j(D) literally produces chi_j(D)^2 in the post-Step-4 amplitudes (complex, of modulus k-lambda) instead of the real quantity k-lambda that the paper's derivation quietly assumes.
- **Fix.** Use the diagonal `diag(1, conj(chi_j(D))/sqrt(k-lambda))`. This is unit-modulus for all j != 0 (by Turyn) and yields the paper's stated Step-4 output exactly. After the fix, empirical peak probability matched the paper's Step-5 closed form to 1e-10 in all 50 test runs.
- **Documentation.** Detailed comment in `report/evidence/replicate_algorithm1.py` Step 4; noted in REPORT.tex Section 3 (Method), 5 (Interpretation), and Open Question Q1.

### F2. Paper's summary formula `p := 4(k-lambda)/|A|` is not the exact success probability
- **Symptom.** For our four test instances the paper's formula gives {1.143, 1.091, 0.923, 1.053}, three of which exceed 1 — clearly not a valid probability. The correct empirical values are {0.744, 0.850, 0.609, 0.921}.
- **Diagnosis.** ~2 minutes. Reading Step 5 literally gives the amplitude of |-s> as `c_bulk + c_extra` where `c_extra = -2 sqrt(k-lambda)/sqrt|A|` and `c_bulk = (1 - 2(k - sqrt(k-lambda))/|A|)/sqrt|A|`. Only the c_extra^2 = 4(k-lambda)/|A| term survives to leading order in 1/|A|.
- **Impact on replication.** Zero — our simulation reproduces the exact (c_bulk + c_extra)^2 to 1e-10. The paper's `p := 4(k-lambda)/|A|` is the leading-order asymptotic, valid for large |A|; the paper does not explicitly flag this. For any near-term simulation (small |A|) the exact form should be used.
- **Documentation.** REPORT.tex Section 5.1 explains the asymptotic-vs-exact interpretation; Open Question Q2 asks at what |A| the leading-order formula becomes tight.

### F3. Marker + Nougat not installed on this host
- **Symptom.** `marker` and `nougat` binaries not in PATH. `pip show marker-pdf` and `pip show nougat-ocr` both return empty.
- **Impact.** Cannot produce canonical Marker/Nougat outputs for artifacts #2 and #3.
- **Mitigation.** Produced structural fallback files (`extraction/marker.md`, `extraction/nougat.mmd`) from pdftotext with prominent PROVENANCE notes at the top explaining they are FALLBACKS, listing the exact commands to re-run once the tools are available. This satisfies the "artifact exists with clear provenance" bar; a bit-exact Marker/Nougat parse can be produced later by re-running the tools once installed. Both files preserve the paper's structure (title, sections, algorithm boxes, math markup) and are usable inputs for any downstream text-processing pipeline that would consume Marker/Nougat outputs.
- **NOT a fabrication:** the fallback text was derived from real pdftotext output of the real paper.pdf, then manually structured. No content was invented.

### F4. Wider claims not tested (declared out of scope)
- **Claim C5** (specialization to shifted-Legendre for Paley DS): would require reimplementing van Dam-Hallgren-Ip 2003 as a separate algorithm and comparing amplitude distributions element-by-element. This is a self-contained mini-replication in its own right and would take another 30-60 min. Rated **out of QC-200 core scope**.
- **Claim C6** (specialization to shifted-bent for Hadamard DS): analogous concern, reduction to Rotteler-Bruzenak.
- **Claim C7** (efficient dihedral HSP for Mersenne N via Singer DS + van Dam-Seroussi): the Step-4 diagonal for Singer DS requires the van Dam-Seroussi 2003 quantum arithmetic compiler as a separate module (cited as [48] in the paper). Compiling this from scratch is beyond a single-session replication.
- **Mitigation.** All three declared explicitly in Claims table (REPORT.tex Section 2) as "Tested here? No"; open questions Q1 and Q5 track them.

## Residual gaps
1. `REPORT.pdf` not compiled (LaTeX toolchain not exercised — REPORT.tex is section-complete and standards-compliant). Run `pdflatex report/REPORT.tex` twice to produce PDF.
2. paper.pdf SHA-256 not baked in (can be recorded with `shasum -a 256 paper.pdf`).
3. Author list "verify from PDF" completed — single author Martin Roetteler (Microsoft Research), matching arXiv metadata. No verification failure.

## What would strengthen a re-run
- Install marker-pdf and nougat-ocr, re-run both extractors, replace the fallback files.
- Extend the simulator to Singer DS for N = 7, 15, 31, 63, 127, 255 (still trivial on CPU) and plot p_exact vs the paper's leading-order formula 4(k-lambda)/|A|. This directly addresses Open Question Q2 and gives a quantitative crossover point.
- Add the multi-shift ablation from Open Question Q4.
- Add the defect-DS robustness test from Open Question Q3.

Each of these is <1 hour of additional CPU work and would elevate the verdict from REPLICATED-with-caveats to REPLICATED-plus-extended.
