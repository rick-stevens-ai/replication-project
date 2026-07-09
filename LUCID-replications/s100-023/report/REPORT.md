# LUCID Second-100 Replication Report — s100-023

**Paper:** Geometrical structures for radiation biology research as implemented in the TOPAS-nBio toolkit
**Authors:** McNamara A, Geng C, Held K, Perl J, Ramos-Méndez J, Faddegon B, Paganetti H, Schuemann J (McNamara et al. 2018)
**Venue:** Phys. Med. Biol. 63(17):175018, 2018
**DOI:** 10.1088/1361-6560/aad8eb
**Second-100 rank:** 23 (track_structure_monte_carlo / geometry catalogue)

---

## VERDICT

**SPOT-CHECK — Coverage 6 / 10 · Agreement 9 / 10**

This is a **descriptive geometry-catalogue paper** for the TOPAS-nBio DNA/cell
geometry classes; it contains **no headline DSB-yield or dose–response numbers of
its own** (biological yield validation is delegated to the companion paper
McNamara et al. 2017, Phys. Medica 33:207–215, which requires a working
TOPAS-nBio + Geant4-DNA install). What is reproducible here is the paper's
**geometric/arithmetic claims**, and those reproduce essentially exactly: **9 of 10
numeric checks PASS**. Verdict is SPOT-CHECK (not REPLICATED) because the paper's
scientific payload is the simulation toolkit itself, which cannot be end-to-end
re-run without the MC engine.

---

## Reproduced claims (numpy/arithmetic, no MC engine)

| # | Claim | Paper | Reproduced | Result |
|---|---|---|---|---|
| C1b | Whole-genome chromatin fibres (diploid) | ~342,204 | 2 × 170,902 = 341,804 (abs diff 400) | ✅ |
| C2b | Whole-genome bp (diploid) | ~6.0×10⁹ | 2 × 3.080 Gbp = 6.160 Gbp | ✅ |
| C3 | Implied bp/fibre vs 90 nucl × 200 bp | 18,000 | 18,021 (+0.12%) | ✅ |
| C5 | Hilbert-curve fibres, n=1 / 2 / 3 | 7 / 64 / 512 | 7 / 64 / 512 | ✅ |
| C6 | Solenoid bp/histone sanity | 150–200 | 177.0 (10.8 kbp / 61 histones) | ✅ |
| C7 | Chromatin packing in 13×10×3 µm ellipsoid | ≤ 1.0 | 2.51% (physically fits) | ✅ |
| C1a/C2a | Table 2 sums are HAPLOID | (text quotes diploid) | 170,902 fibres / 3.080 Gbp | ⚠️ see below |

**Overall: 9/10 numeric checks PASS.**

## The one "FAIL" — a real paper bookkeeping ambiguity

The single non-pass is a deliberate haploid-vs-diploid contrast, not an error in
our reproduction. The paper's **Table 2 columns sum to the HAPLOID genome**
(170,902 fibres; 3.080 Gbp), while the running **text quotes DIPLOID values**
(~342,204 fibres ≈ 2×; ~6×10⁹ bp ≈ 2×). The ratio is 2.00 in both cases,
confirming the table/text mismatch is exactly the haploid↔diploid factor. This is a
genuine (minor) bookkeeping ambiguity in the source paper worth flagging to anyone
reusing Table 2 — the per-chromosome fibre/bp counts are per-haploid-copy, not the
whole-cell totals the text describes.

---

## Reproducibility-blocker critique (6/22 rule)

- **Method/engine blocker (named):** the paper's actual deliverable — the
  TOPAS-nBio geometry classes (fibre/solenoid/Hilbert/ellipsoid nucleus builders)
  and their use in DNA-damage simulation — **cannot be end-to-end reproduced
  without compiling and running TOPAS-nBio on top of Geant4-DNA.** That engine is
  installed on uicgpu (Geant4 11.4.2 + G4EMLOW 8.8, C++ build), so a future full
  run is feasible; it was out of scope for this lightweight pass.
- **Data blocker (precise missing artifact):** the paper publishes **no machine-
  readable geometry files or per-fibre coordinate dumps** — Table 2 is the only
  numeric artifact, and its **haploid/diploid basis is not stated explicitly**,
  forcing the reader to infer it from the 2.00× text/table ratio. The precise
  missing artifact is a documented "Table 2 is haploid per-copy counts" note (or
  the diploid table) plus the actual TOPAS geometry input files.
- **No code release** accompanying the paper (the toolkit ships separately as
  TOPAS-nBio); all reproduced numbers here came from transcribing Table 2 and the
  paper's stated nucleosome/Hilbert/solenoid arithmetic.

---

## Artifacts
`source/paper.pdf`, `ocr/paper.txt`, `code/reproduce.py` (10 numeric checks),
`evidence/run_output.txt` (full PASS/FAIL log). Compute: arithmetic only, no MC run.

## Follow-up
A true end-to-end replication would compile a TOPAS-nBio geometry example on uicgpu
(engine already built) and reproduce a companion-paper (McNamara 2017) DSB-yield
figure — promotable from SPOT-CHECK toward PARTIAL/REPLICATED.

---
*Verdict authored from disk-verified subagent artifacts (9/10 numeric PASS), 2026-06-25.*
