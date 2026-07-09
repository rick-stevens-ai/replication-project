# Bulletised claims — Park et al. 2024 (ijmm.2024.5380)

Anchors below refer to PMC11093554 sections; verbatim quotes from the JATS-XML in `artifacts/europepmc_fullText.xml`.

## C1 (Selection)
> "A total of 16 proteins were selected based on published findings [8, 10]" — Introduction §3.
Full panel (Discussion §2): ATM, CHK2, p53, NBS1, BRCA1, H2AX, CHK1, ERK, p53 (listed twice in source — likely typo for a second isoform/phospho-form), EGFR, IL-1α, MIF, MCP1, GDF-15, IL-7, MIP1α.
Down-selection criteria (Introduction §3): (i) detectable in low-dose IR range; (ii) concentration-dependent response; (iii) applicable to blood samples.

## C2 (Surviving panel)
> "ATM, p53, CHK2, and H2AX respond to low-dose radiation in a dose-dependent manner." — Results §"Expression of DDR signaling molecules following low-dose radiation".

## C3 (Cytokine exclusion)
> "cytokine expression was detected in only four out of six cases at 24 h following irradiation, and therefore, cytokines were excluded from the study due to significant fluctuations and delayed responses" — Discussion §2 (Fig S2).

## C4 (Cell-line caveat)
- ATM activation absent in HuT 78. p53 not observed in HuT 78 (p53 mutant p.Arg196Ter(c.586C>T)). IM-9 is p53 WT. — Results §1.
- CHK2 activation undetectable in irradiated hPBMCs (anomaly, no mechanism given). — Results §1.

## C5 (Fit form)
Fig 1B dose–response data fit with "asymmetrical sigmoidal, five-parameter curves" (5PL).

## C6 (Pharmacology, in vitro)
GI50 (CCK-8, 24 h):
- KU60019 (ATM inh): IM-9 3.28 µM, HuT 78 4.65 µM
- BML-277 (CHK2 inh): IM-9 13.45 µM, HuT 78 13.40 µM
- Pifithrin-α (p53 inh): IM-9 97.28 µM, HuT 78 110.6 µM
- Nutlin-3a (p53 act): IM-9 38.77 µM, HuT 78 64.38 µM

## C7 (Headline drug result)
> "BML-277 attenuates radiation-induced cell death by inhibiting CHK2 activation, with a more potent effect in the presence of p53." — Results §"Effects of DDR modulators on radiation exposure".

## C8 (In vivo cinobufagin)
- 8 Gy TBI, n=8/group; survival 37.5% at day 11 with 5 mpk cinobufagin vs 0% in vehicle; not statistically significant (Mantel-Cox).
- 3 Gy TBI: increased BM cellularity in cinobufagin-treated mice; no change in RBC/platelets; lymphocyte/neutrophil decrease.

## C9 (Headline)
> "ATM, CHK2, p53 and γH2AX can serve as predictive markers for low-dose IR ... the CHK2 inhibitor, BML-277, provided the most efficient radiation protection by reducing radiation-induced DNA damage." — Conclusion.

## Data/code availability
- **No deposited data**, no code repo, no accession numbers.
- Supplementary Data PDF (Figs S1, S2; tables) referenced as `Supplementary_Data.pdf` on Europe PMC. Direct fetch attempted 2026-06-09 — Europe PMC PDF backend returned "Empty reply from server"; PMC HTML hit reCAPTCHA. Available manually via Europe PMC HTML article page.
- "Datasets ... available from the corresponding author on reasonable request" (Song JY, immu@kirams.re.kr). Not contacted per task rule.

## Source-of-truth provenance vs paper reality

The LUCID master TSV (rank 43) tags this paper as `worktype = simulation/model replication`. **This is incorrect**: the paper is a wet-lab biomarker / pharmacology study with literature-curated candidate selection. The only "model" content is a 5PL regression on dose-response data. Flag for QA: consider re-tagging to `wetlab biomarker; literature curation; pharmacology` and `replication tier = digitisation + selection-logic replay`.
