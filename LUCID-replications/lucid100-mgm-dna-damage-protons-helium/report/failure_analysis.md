# Failure Analysis — `lucid100-mgm-dna-damage-protons-helium`

Honest post-mortem of what this replication did NOT achieve, why, and how
the on-disk evidence maps against the queue-level classification.

## 1. Verdict-mismatch flag (CRITICAL)

- **Queue verdict (project-level bookkeeping): `REPLICATED`.**
- **On-disk actual verdict (from `PROMO_RESULT.txt` and REPORT.md §8):
  `PARTIAL`** (coverage 4/10, agreement 7/10).
- **Preserved verdict: PARTIAL** (on-disk authoritative — the queue label
  is downgraded here in favour of the actual audit).
- **Root cause of the mismatch:** the paper's central deliverable
  (TOPAS-MGM C++ extension code + its per-cell histograms, FWHM scan,
  Bragg-peak depth scan, RPT histograms, and timing table) is
  **unpublished**. The on-disk replication reproduces only the
  analytical MGM core polynomials (Bertolet 2023, already public) and
  extends them with an independent LET-anchor sweep from the sibling
  BNCT slot. That covers ~4/10 of the analyzable units, which is below
  the ~5/10 threshold most reviewers would set for `REPLICATED`.
- This matches the task-brief statistic: **~33% of queue-REPLICATED
  LUCID dirs sampled this session had on-disk PARTIAL/NO-GO downgrades**
  (9/27); this slot is one of them.
- **Recommended queue action:** re-label this slot from REPLICATED to
  PARTIAL pending release of TOPAS-MGM source. Alternative: retain
  REPLICATED but attach a "MC-code-not-re-run" caveat in queue metadata.

## 2. What was NOT reproduced

### 2.1 The Monte-Carlo transport was not re-run
- **Not a single TOPAS, TOPAS-nBio, or Geant4-DNA transport step was
  executed** as part of this replication. Every quantitative check
  evaluates published MGM analytical polynomials in Python.
- **Why:** (a) TOPAS-MGM extension source is unreleased; (b) even with
  it, reference TOPAS-nBio runs are multi-day HPC jobs; (c) CherryRd is
  disallowed for heavy MC per project policy; (d) no uicgpu / Aurora /
  Polaris allocation was set up for this slot.

### 2.2 Published aggregate numbers were REUSED, not re-derived
- All C1–C9 anchors are the paper's own summary/headline numbers (mean
  complexity, MDS/Gy/Gbp, Bragg-peak ratios) as read from the paper's
  figures and text. There is no independent MC dataset for cross-check.
- The closest independent evidence is the P1–P3 use of Geant4-DNA LET(E)
  tables from the sibling BNCT slot — **but those are LET values, not
  yF spectra**, so they only anchor the LET axis, not the true yF
  distribution the paper uses.

### 2.3 The proton-vs-helium LET-matched comparison (paper Fig 3) was NOT reproduced
- On the contrary, P3 explicitly demonstrates that analytical MGM
  **cannot** reproduce it: MGM He/p ratio ≈ 1.0 at matched LET
  ≤ 35 keV/μm, whereas the paper's TOPAS-MGM shows He > p.
- This is an important intellectual finding (identifying an MGM model
  LIMIT) but it is NOT a positive reproduction of Fig 3.

### 2.4 Damage complexity SPECTRUM was NOT tracked — only aggregate mean was checked
- The paper reports per-MDS complexity histograms (Fig 4c) and cMDS
  fractions (C ≥ 3, C ≥ 5). The replication reports mean C̄ and coarse
  fractions from evaluating the paper's own a(yF), b(yF) polynomials.
- **Full distribution shape** (mode, kurtosis, tail behaviour beyond
  C ≥ 5) was NOT compared.

### 2.5 Bragg-peak claims were only spot-checked at 2 depths
- C8 (proton BP ratio 1.07 vs 1.12) and C9 (helium BP ratio 1.6–1.9 vs
  4.0) test 1 depth each; the full Fig 6 depth scan (~50 depths ×
  2 particles) was NOT reproduced.
- C9's factor-of-2 FAIL for helium is left as a known open gap — the
  most likely cause is missing yF(depth) data plus the MGM b(yF)
  zero-crossing near yF ~ 164 keV/μm, but this was not investigated
  further.

### 2.6 Table 1 timing benchmark: NOT REPRODUCED
- Requires both TOPAS-MGM (unreleased) and TOPAS-nBio (not installed).
  No timing measurement of any kind was made.

### 2.7 RPT histograms (Fig 7, ²¹¹At + ²²⁵Ac): NOT REPRODUCED
- Requires the extension code + radionuclide MC source terms. Nothing
  attempted.

### 2.8 Supplementary material was NOT retrieved
- PMC SI for PMC12905799 is reCAPTCHA-gated. Contains (likely) the
  exact a(yF), b(yF) fit parameters, AAPM TG-268 reporting, and per-MDS
  histograms — all of which would tighten C1–C5.
- **Recovery path:** open PMC12905799 in a human browser session,
  download the SI PDF, place at `artifacts/supplementary.pdf`.

## 3. What WAS achieved (positive record)

1. Full clone + smoke of the public MGM analytical engine (Bertolet
   2023, Python, MIT) with 5 anchor points reproducing paper C1
   polynomial coefficients to < 0.3 %.
2. SPOT-CHECK claims C1–C9: 5 VERIFIED, 1 PARTIAL, 1 CONTRADICTED-with-
   explanation (C9), 1 CONTRADICTED-or-ambiguous (C6, later resolved by
   P4).
3. Promotion checks P1–P5: 4 VERIFIED, 1 CONTRADICTED-but-informative
   (P4). P3 documents a previously-undocumented MGM model LIMIT.
4. P2 sweep of 29 (E, particle) points via MGM anchored to independent
   Geant4-DNA LET(E) tables from a sibling slot — adds genuine U3
   coverage that a strict "MGM library only" pass would miss.

## 4. Root causes of the gap between on-disk and REPLICATED

| Cause | Class | Fixable? |
|---|---|---|
| TOPAS-MGM extension code unpublished | External (author) | Only by author release. Contact `MGHPhysicsResearch` or paper corresponding author. |
| TOPAS-nBio yF spectra not tabled numerically | External (paper) | Only by author release of raw yF distributions. |
| PMC SI reCAPTCHA-gated | External (PMC) | Fixable in one human-browser session. |
| No HPC allocation set up for TOPAS-nBio reference runs | Internal | Fixable via uicgpu or Aurora allocation + TOPAS academic license + build. Est. multi-day MC per run. |
| MGM has no track-structure knob | Model | Not fixable in current MGM; requires model extension (see open-question 1). |

## 5. Prevention notes for future LUCID-100 backfill passes

- Always cross-check queue verdict against `PROMO_RESULT.txt` and
  `REPORT.md` §Verdict. **Do NOT trust queue label as authoritative.**
- Any slot that classifies as REPLICATED but relies entirely on
  analytical/model-arithmetic reproduction of a paper whose central
  deliverable is unreleased Monte-Carlo code should be automatically
  flagged for downgrade review.
- When paper's central figures require an unreleased extension, the
  replication should either: (a) get the code from the authors,
  (b) build an independent MC replacement, or (c) explicitly document
  the limit and stay at PARTIAL. Silently classifying (c) as REPLICATED
  overstates the reproduction claim.

## 6. One-line summary

**Replication of Onecha 2025 MGM extension is analytical-only; the
paper's central TOPAS-MGM C++ code was NOT re-run and the queue
REPLICATED label is not supported by the on-disk evidence. Preserved
verdict = PARTIAL (coverage 4/10, agreement 7/10).**
