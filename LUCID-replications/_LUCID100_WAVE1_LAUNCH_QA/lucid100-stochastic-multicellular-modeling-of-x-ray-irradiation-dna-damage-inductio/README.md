# Stochastic multicellular modeling of x-ray irradiation, DNA damage induction, DNA free-end misrejoining and cell death

## LUCID100 curated Wave 1 replication brief

- **Rank:** 35
- **Tier/score:** A / 20
- **DOI:** 10.1038/s41598-019-54941-1
- **Year / venue:** 2019 / Scientific Reports
- **Themes:** DNA repair / DDR; radiation quality / RBE; computational model / simulation
- **Worktype:** simulation/model replication
- **Source:** dropbox_pdf
- **PDF / URL:** /Users/stevens/Dropbox/XFER/LUCID-replication-targets/29892663dbd799e5eed06076d44cc4c56dcea1d7.pdf
- **QA decision:** KEEP: relevant and replication-plausible

## Replication target

TODO during artifact harvest:

1. Extract central quantitative/mechanistic claims.
2. Identify public code, data, supplement, tables, and figures.
3. Decide strict scope: exact rerun, independent reimplementation, table/figure digitization, or no-go.
4. Define acceptance criteria before running.

## Artifact harvest checklist

- [ ] Source PDF saved locally
- [ ] Full text extracted
- [ ] Supplementary files found/downloaded
- [ ] Code repository found/cloned, if any
- [ ] Public data accession found/downloaded, if any
- [ ] Environment plan written
- [ ] Acceptance metrics defined
- [ ] Blockers listed explicitly

## Execution checklist

- [ ] Smoke test / minimal calculation
- [ ] Main replication run
- [ ] Figures/tables regenerated or digitized comparison done
- [ ] Logs, hashes, environment, and provenance captured
- [ ] `REPORT.md` written
- [ ] Progress JSON written under OpenClaw memory

## Initial abstract/notes

The repair or misrepair of DNA double-strand breaks (DSBs) largely determines whether a cell will survive radiation insult or die. A new computational model of multicellular, track structure-based and pO2-dependent radiation-induced cell death was developed and used to investigate the contribution to cell killing by the mechanism of DNA free-end misrejoining for low-LET radiation. A simulated tumor of 1224 squamous cells was irradiated with 6 MV x-rays using the Monte Carlo toolkit Geant4 with low-energy Geant4-DNA physics and chemistry modules up to a uniform dose of 1 Gy. DNA damage including DSBs were simulated from ionizations, excitations and hydroxyl radical interactions along track segments through cell nuclei, with a higher cellular pO2 enhancing the conversion of DNA radicals to strand breaks. DNA free-ends produced by complex DSBs (cDSBs) were able to misrejoin and produce exch
