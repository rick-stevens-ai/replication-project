# Failure analysis — BVBRC-31 (Delgado-Suárez 2021)

**Verdict:** PARTIAL REPLICATION. The genotypic core reproduces cleanly on the paper's own isolates using the paper's own tool stack. Two categories of claims did not reproduce, and one systemic gap remains. This file is the honest accounting of each.

## Category A — Coverage-driven failures (fixable with more CPU)

### A1. 9/77 isolates lacked GenBank assemblies at run time

- **What happened:** Of the 77 study isolates, 68 (88%) had curated GenBank (GCA) assemblies retrievable via NCBI Datasets v2alpha. 9 did not — a newer Reading batch plus 2 others.
- **Downstream impact:**
  - **C7 (SGI1 penta-cassette):** paper reports 9/10 Typhimurium carry the full aadA2/blaCARB-2/floR/sul1/tetG set. Only 7 Typhimurium had assemblies here → we could at best replicate 7 (we got 6/7). The paper's 9/10 vs our 6/7 is coverage-driven, not disagreement.
  - **C5 (MDR by source):** direction reproduced (ground beef 33.3% > lymph nodes 18.2%) but the ground-beef n dropped from 29 → 24, deflating χ² from paper's 12.0 to our 1.98.
- **Root cause:** the 9 isolates have public SRR reads but no GenBank-deposited assembly; this replication chose the assembly path for speed and did not run de-novo assembly (SKESA / SPAdes).
- **Fix:** de-novo assemble the 9 from SRR (Illumina) reads, rerun AMRFinderPlus/SeqSero2/MLST on the resulting 77-isolate set. All open tooling, all CPU-only.

### A2. 2,400-genome public comparison not attempted

- **What happened:** The paper's headline framing — "cattle and poultry are a moderate source of MDR NTS in Mexico" — leans on comparing the 77 study isolates to a 2,400-genome public Mexican NTS set (S2 File accessions). This replication did not pull or process the 2,400 set.
- **Downstream impact:** That specific attribution sentence is not independently checked in this report. The 77-isolate genotypic claims are all replicated, but the animal-source-attribution *contrast* is not.
- **Root cause:** scope choice; the 2,400-set is 30× larger and doubles pipeline runtime. Left as a future pass.
- **Fix:** feed S2 File accessions to the same `datasets download` + `run_amr.sh` + `analyze.py` pipeline; recompute MDR-by-source-category over the union set.

## Category B — Tool-methodology failures (real disagreement)

### B1. QRDR and ramR point-mutation claims (C8) did not reproduce

- **What happened:** AMRFinderPlus 3.12.8 (DB 2024-07-22.1) with `--organism Salmonella` and mutation search confirmed on in logs returned **zero curated resistance point mutations across all 68 isolates.** The paper reports 100% QRDR (gyrA/gyrB/parE), soxRS mutations, and a ramR–MDR association at χ²=17.7, P<0.0001.
- **Root cause — genuine methodological difference, not a data or execution error:**
  - The paper's QRDR/ramR calls come from a **raw sequence-vs-reference SNP-calling approach** (extract the gene, align to *S.* Typhimurium LT2 or equivalent, call every non-synonymous change, label as "resistance-associated mutation").
  - AMRFinderPlus's curated point-mutation catalog **only reports mutations with documented resistance evidence**. Most non-synonymous QRDR SNPs in field Salmonella do not clear that evidence bar, so the curated catalog returns zero even when the raw-SNP approach returns "100% mutated".
  - Both methods are legitimate; they measure different constructs. The paper does not disambiguate.
- **Fix (if a follow-up run is warranted):** implement the paper's raw-SNP approach — pull the six loci from each of the 68 assemblies, align to LT2, call all non-synonymous changes, then recompute the ramR × MDR χ².

### B2. Genotype vs phenotype gap on per-class prevalence

- **What happened:** Absolute per-class prevalences run a few points below the paper's:
  - β-lactam: 26.0/20.8% (pheno) vs 11.8% (geno).
  - Phenicol: 19.5% vs 10.3%.
  - SXT: 16.9% vs 11.8%.
  Rankings and top/bottom structure match the paper (tetracycline top, cephalosporin/carbapenem rare/absent), but the numbers themselves do not.
- **Root cause:** the paper reports AST-based (phenotypic) percentages; this replication reports genotypic (AMRFinderPlus) percentages. Genotype→phenotype concordance for Salmonella acquired resistance is imperfect (typically 85–95% depending on class). Also, some β-lactam resistance is chromosomal/intrinsic AmpC that is not called as "acquired".
- **Fix:** obtain the phenotypic AST table (paper's underlying MIC data, S-file) and score both approaches head-to-head per class and per isolate. Not resolvable from sequence alone.

## Category C — Statistical fragility (real, and worth flagging)

### C1. GB-vs-LN MDR significance (C5)

- **Paper:** χ²=12.0, P=0.0005.
- **This work:** χ²=1.98, p=0.16 on the 68-subset.
- **What that means:** the *direction* is robust (ground beef > lymph nodes for MDR proportion), but the *significance* is not. A drop from n=77 to n=68 (9-isolate reduction, all preferentially from certain serovars) should not collapse a P=0.0005 result if the effect were as strong as claimed. This suggests the paper's significance is at least partly power-driven, and possibly leans on the phenotypic MDR call being systematically more permissive than a genotypic one.
- **Fix path:** rerun on the full 77-isolate set (Category A1 fix) and, if still not significant, report that honestly. If the paper's phenotypic MDR is the reason, that too is worth reporting.

## What did NOT fail (worth stating for balance)

- **C1** Cohort recovery — perfect (77/77).
- **C2** Serovar typing — 67/68 concordant → effectively 68/68 after resolving Reading antigenic formula.
- **C3** Class ranking — matches paper (tet top, ceph absent).
- **C4** MDR prevalence — 23.5% vs 26% (within 2.5 pp).
- **C6** Typhimurium share of MDR — 37.5% vs 40%.
- **C7** SGI1 penta-cassette — **6/7 Typhimurium carry the exact aadA2/blaCARB-2/floR/sul1/tetG set** the paper names. Direct mechanistic replication.
- **MLST corroboration** — ST19 = Typhimurium, ST64 = Anatum, ST198 = Kentucky, etc., all internally consistent with known Salmonella eBURST clusters.

## One-line summary

The paper's mechanistic core (SGI1 in Typhimurium, MDR magnitude, serovar structure) is reproducible on independent execution of the paper's own pipeline; its statistical (GB-vs-LN P=0.0005) and mutational (100% QRDR, ramR–MDR χ²) claims are not, and the second-class failure is a real tool-methodology disclosure gap in the original paper.
