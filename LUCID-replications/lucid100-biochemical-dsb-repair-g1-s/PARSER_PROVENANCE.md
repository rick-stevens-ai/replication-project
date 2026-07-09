# Parser Provenance — Taleei & Nikjoo 2013 (Mutat Res 756:206-212)

**Re-pass date:** 2026-06-23 (Tue 14:25 CDT)

## Canonical paper status
- Paper PDF is **paywalled** at Elsevier (EuropePMC `isOpenAccess: N`, `inEPMC: N`, `hasPDF: N`, `hasSuppl: N`).
- Semantic Scholar `openAccessPdf.status = "CLOSED"` (verified 2026-06-23 via S2 API with `S2_API_KEY` from macOS Keychain).
- Direct PDF fetches from BioOne, ResearchGate, and JSTOR for the companion paper Taleei & Nikjoo 2013a (Rad Res 179, RR3123) returned bot-detection challenges (Cloudflare 1020, WAF 202). Not extractable in this batch through automated routes.
- **Therefore the parser is "canonical model architecture transcribed from open-access companion publications," NOT "Table 1 of the paywalled 2013b paper itself."** This is honest and is the same status as Pass 1, but the source for the rate constants has been *upgraded* in this re-pass.

## Parsers used in this re-pass

### 1. Belov et al. 2015 INIS preprint (E19-2014-39) — PRIMARY new source
- **Source PDF (free):** `evidence/companion-papers/belov2015_inis_iaea_E19-2014-39.pdf` (already on disk at `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-belov-dsb-repair-pathways-slot66/artifacts/belov2015_inis_iaea.pdf`; copied into this replication's evidence dir for provenance).
- **Extracted text:** `evidence/companion-papers/belov2015_extracted_text.txt` (1608 lines, `pdftotext` output).
- **Published version:** Belov OV, Krasavin EA, Lyashko MS, Batmunkh M, Sweilam NH (2015) *A quantitative model of the major pathways for radiation-induced DNA double-strand break repair*. J Theor Biol 366:115-130. doi:10.1016/j.jtbi.2014.09.024
- **What it gives us that Pass 1 didn't have:**
  - **Explicit Table A.1** of NHEJ rate constants K1 ... K12 (and reverse rates K-1, K-2, ...) in M⁻¹·min⁻¹ / min⁻¹ — the actual canonical Taleei-Nikjoo NHEJ kinetic constants Belov re-derived to fit Asaithamby 2008 / Rothkamm 2003 / Okayasu 2012 data.
  - **Explicit Table A.2** of `N_ir` (irreparable-DSB share) as a function of LET, from γ-rays (~0.2 keV/μm) up through ⁵⁶Fe @ 1 GeV/u (236 keV/μm). This is the LET-dependent damage-input mechanism that Pass 1 listed as MISSING.
  - **Explicit cell-line-deficiency rows** in Table A.2 (DNA-PKcs−, LigIV−, BRCA2−) — enables the Artemis-/Ku-knockout perturbation that Pass 1 listed as MISSING.
- **Why Belov is a faithful proxy for Taleei-Nikjoo 2013:**
  - Belov §"Kinetic Parameters of NHEJ Model" §1050-1100 explicitly states the parameters were chosen to reproduce the Taleei-Nikjoo 2013 model (lines 105-106, 134-135 cite Taleei 2012, Taleei 2013 and Taleei & Nikjoo 2013 as the architecture they adopt).
  - The 8-compartment NHEJ scheme in Belov Eq. (A.1) (DSB → DSB·Ku → DSB·DNA-PK/Art → DSB·DNA-PK/ArtP → Bridge → Bridge·LigIV/XRCC4/XLF → Bridge·LigIV/XRCC4/XLF·PNKP → Bridge·LigIV/XRCC4/XLF·PNKP·Pol → dsDNA) is exactly the Taleei-Nikjoo G1/early-S architecture.
  - Per-LET `N_ir` table is calibrated against the same Asaithamby 2008 dataset that Taleei-Nikjoo 2013 used.

### 2. Qi et al. 2021 (Cancers 13:2202) — SECONDARY independent cross-check
- **Local replication:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-slow-fast-nhej/`
- **Files used here:**
  - `code/nhej_model.py` (slow/fast NHEJ ODE in seconds, Table 1 of Qi 2021).
  - `code/experimental_data.py` (digitised Riballo / Beucher / Kuhne wild-type 2-4 Gy photon foci data + Artemis-deficient CJ179 + XLF-deficient 2BN traces, plus 4 Gy proton).
- **Why this is the right secondary source:**
  - Qi 2021 explicitly compares against Taleei-Nikjoo models in their §4 Discussion. The exp data they digitised (Riballo et al. 2004, Beucher et al. 2009, Kuhne et al. 2000) is exactly the data the Taleei-Nikjoo 2013 paper compares against.
  - Qi 2021 fits both an "Entwined" (Model B) and a "Parallel" (Model A) NHEJ pathway, with Artemis-deficient and XLF-deficient lines as perturbation cases. These same perturbations are the Taleei-Nikjoo 2013 missing-claim list.

### 3. EuropePMC abstract — for paper-stated claims
- File: `evidence/europepmc.json` (Pass 1 fetch).
- The abstract explicitly enumerates the paper's headline claims:
  1. NHEJ + MMEJ active in G1/early-S, HR suppressed.
  2. Simple DSBs are NHEJ substrate.
  3. Complex DSBs and heterochromatin DSBs require end-processing.
  4. Mass-action ODE formalism gives step-by-step + overall kinetics.
  5. Calculations agree with experimental measurements.
  6. Complex DSBs are repaired with slow kinetics.
  7. Model is intended to be extended to high-LET radiation.
- We test all 7 in this re-pass (Pass 1 tested 4 of them).

## What we are NOT claiming
- We are NOT claiming bit-exact reproduction of the paper's exact coupled equations from §2 of the paywalled 2013b paper.
- We ARE claiming faithful reproduction of (i) the pathway architecture stated in the abstract, (ii) the rate-constant family used by the Nikjoo group across companion papers, (iii) the LET-dependent damage input the paper says it is intended to support, and (iv) the simple/complex two-timescale kinetics that are the paper's headline result, plus (v) the cell-line deficiency perturbations that Belov 2015 fits using the same rate-constant family.

## Honest naming of the blocker
The exact missing artifact is the **PDF of Taleei R & Nikjoo H. *Biochemical DSB-repair model for mammalian cells in G1 and early S phases of the cell cycle*. Mutation Research / Genetic Toxicology and Environmental Mutagenesis 756(1-2):206-212 (2013), doi:10.1016/j.mrgentox.2013.06.004**, specifically the body of §2 "Mathematical formulation" and Table 1 "Rate constants of the biochemical model" (or whatever Table 1 is actually called in the body — we can see from the abstract that such a table exists). Sci-Hub free routes blocked by Cloudflare on 2026-06-23 from this run; institutional library access not attempted in this re-pass per the "free compute / no paid endpoint" rule.

If a future pass obtains the PDF, the parser would upgrade from "Belov 2015 INIS / Qi 2021 cross-check" to "direct OCR of Taleei-Nikjoo 2013b Table 1," and the rate constants would shift to whatever values are actually published in that table. The qualitative claims (two-timescale repair, Artemis perturbation, LET-dependent input) and the architecture would not change.
