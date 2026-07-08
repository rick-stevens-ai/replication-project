# LUCID-100 Replication Verdicts — 2026-06-21 session (Ollie)
*Owner: Ollie (full LUCID-100 corpus per Rick 2026-06-21). Free endpoints only, AUDIT_PROTOCOL.*

| Row | Paper | Verdict | Cov | Claims | Blocker (reproduction ceiling) |
|---:|---|---|---|---|---|
| #30 | Rusin 2021 doserate×cell-cycle (PLoS ONE) | **REPLICATED** | 88% | 41/52 | none — raw data on Mendeley (10.17632/8t594k4w8z) |
| #6  | Costes 2007 nuclear-subdomain (PLoS CB) | PARTIAL | sim 100% / exp 0% | — | DATA: raw HMEC image stacks + 2007 Matlab/DIPimage code never archived |
| #10 | Wang 2018 cell-survival from DSBs (Sci Rep) | PARTIAL | 27% | 6/30 | DATA: Wang's MCDS Y-input table unpublished (PIDE/Furusawa NOW CONFIRMED LOCAL — refit queueable) |
| #53 | GLOBLE / Friedrich 2012 DSB-clustering (Rad Res) | PARTIAL | 80% | 9/11 | ACCESS: target BioOne-paywalled; model recovered via OA follow-up Herr 2014. 2 cell-line-fit claims locked behind paywall |
| #11 | Friedland 2010 stochastic NHEJ (Rad Res) | SPOT-CHECK | 36% | — | ACCESS: hard BioOne paywall, no PMC/preprint; full Methods/Tables/rate-constants locked |
| #31 | Stelcer 2018 iPSC-chondrocyte IR (PLoS ONE) | SPOT-CHECK | 13% | 8/15 | DATA: full OA text but no raw flow/qPCR deposited (no GEO/SRA/FlowRepository) |

## Pattern (Rick's reproducibility-ceiling question)
ZERO method failures across 6 papers. Verdict tier is set entirely by data/access:
- REPLICATED ⟺ authors deposited raw data
- PARTIAL ⟺ model reproducible but inputs unpublished OR raw experimental data un-archived
- SPOT-CHECK ⟺ hard paywall on full text, or no raw data deposited

## Highest-leverage unblocks (via Rick @anl.gov)
1. BioOne institutional access → unlocks #11 + #53 full text (2 papers, 1 credential)
2. PIDE/Furusawa confirmed on disk (phase3_pide32_tidy.csv) → #10 refit queueable now
3. Run MCDS (free tool) → closes #10's last gap (Wang's unpublished Y table)

## In progress (Wave 3, launched 2026-06-21 ~17:05 CDT)
- #15 space-radiation gut microbiome (Microbiome, OA)
- #35 IRI-DICE hypothesis (Rad Env Biophys) — conceptual-paper audit
- #54 chromosomal-aberration time-dep model (Rad Res, paywall-risk, proxy)

## Wave 3 verdicts (added 2026-06-21 ~17:18 CDT)
| Row | Paper | Verdict | Blocker |
|---:|---|---|---|
| #35 | IRI-DICE hypothesis (Langen 2020, Rad Env Biophys) | SPOT-CHECK | N/A — conceptual "Controversial Issue" essay, no model/data; logic+citation audit passed |
| #54 | Ponomarev/Cucinotta 2014 chromosomal-aberration time-dep model (Rad Res) | SPOT-CHECK | ACCESS: RR paywall (is_oa=False, predecessor RR2659 also walled); proxy reconstruction via McMahon-Medras/Belov-RITCARD lineage, 7/10 abstract claims qualitative, 0/10 numeric |
| #15 | space-radiation gut microbiome (Microbiome 2017) | **REPLICATED** | none for 16S arm — raw SRA SRP098151 deposited, all 80 libs re-analyzed; metabolome arm Dryad-link-generic (gap) |

## HARVEST COMPLETE (2026-06-21 ~17:18 CDT) — Ollie owns LUCID-100
- 75/100 source PDFs on disk (~/Dropbox/XFER/LUCID-replication-targets/), up from 48 at Kukla handoff (+27 via Unpaywall-first + 1 S2-keyed recovery)
- 63 unfetched, two classes:
  - 16 truly CLOSED (real paywall): dominated by Radiation Research (5: rr1965/rade-24-00164/rr2964/rr13303/rade-25-00194) + Taylor&Francis (3, 09553002) + IJROBP/Thyroid/MutRes/Proteomics
  - 47 OA-but-BOT-WALLED: open access but publisher endpoints (36× MDPI 10.3390, OUP, etc.) reject scripted fetch even with S2 openAccessPdf URL — need browser-tool/Playwright or prokko exit-node, NOT a paywall
- Tooling: priority-lists/lucid100_harvest.py (Unpaywall-first), lucid100_recover_oa.py (S2-keyed), LUCID100_access_blockers.tsv (63 typed rows)
- LESSON: S2 API key (keychain semantic-scholar-api-key / S2_API_KEY in .env) MUST be used for S2 calls — Rick's standing reminder 2026-06-21. plain urllib UA gets bot-walled by MDPI/Cloudflare; real reproducibility ceiling for LUCID-100 = 16 paywalled (need @anl.gov) + 47 mechanically-recoverable-via-browser.
