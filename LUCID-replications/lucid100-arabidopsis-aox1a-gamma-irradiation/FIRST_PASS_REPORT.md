# FIRST-PASS REPORT — LUCID100 slot 40

**Paper.** Belykh ES, Velegzhaninov IO, Garmash EV. *Responses of genes of
DNA repair, alternative oxidase, and pro-/antioxidant state in Arabidopsis
thaliana with altered expression of AOX1a to gamma irradiation.*
Int J Radiat Biol 98(1):60–68 (2022).
DOI: `10.1080/09553002.2022.1998712`, PMID `34714725`.

**Verdict.** **NO-GO for quantitative replication; PARTIAL-GO for lateral
directional cross-validation.**

---

## 1. Claim map (8 primary claims from the abstract)

| # | Claim | Replicability from public data |
|---|---|---|
| C1 | At 200 Gy γ-IR, 12 h post, XX-2 (AOX1a-OE) plants have the highest AOX1a transcript and AOX protein | ❌ no public dataset combines XX-2 with IR |
| C2 | XX-2 plants have the *lowest* expression of DNA-repair genes (irradiated and control) | ❌ same — needs XX-2 RNA |
| C3 | WT Col-0 + AS-12 (AOX1a-AS) upregulate AOX1d under γ-IR | ❌ no public AS-12 IR data; AOX1d not in GSE112773 DREM scaffold |
| C4 | WT Col-0 + AS-12 upregulate DDR genes under γ-IR | ✅ qualitatively confirmed in WT against GSE112773 (RAD51, RAD54, BRCA1, PARP1, PARP2 all land in WT-γ-IR-induced DREM paths) |
| C5 | AS-12 plants show higher Mn-SOD enzymatic activity post-IR | ❌ wet-lab enzymology only; not transcriptional |
| C6 | AS-12 plants accumulate more superoxide anion than Col-0 | ❌ wet-lab DAB/NBT staining only |
| C7 | XX-2 plants have the lowest ROS levels among the three genotypes | ❌ wet-lab only |
| C8 | AOX1a is *key* in regulating WT plant γ-IR stress response | ⚠️ partially contradicted — in GSE112773 AOX1a lands in WT-*repressed* path W4 and is SOG1-dependent (S2), not in any WT-induced path |

**0/8 quantitatively replicated.** **1/8 directionally validated from
independent public data** (C4). **1/8 partially contradicted by independent
public data** (C8).

## 2. Openness assessment

- **Paper.** Closed access at Taylor & Francis. Unpaywall `oa_status=closed`,
  no green/gold/hybrid/bronze copy anywhere it indexes. Europe PMC marks
  it `isOpenAccess=N`, `inEPMC=N`. Crossref returns no license URL.
- **Supplementary.** Behind T&F paywall via the same DOI page. Did not
  attempt to bypass.
- **Raw RNA-seq / microarray.** None — the paper uses qPCR + biochemistry,
  not sequencing.
- **Deposit.** No GEO / SRA / ArrayExpress / BioStudies accession. NCBI
  esearch for `AOX1a Arabidopsis gamma irradiation` returns 0 hits in
  both `gds` and `sra`.
- **Code.** None.
- **Biological materials.** AS-12 (antisense) and XX-2 (overexpression)
  AOX1a lines are Komi / Syktyvkar lab-internal lines descending from
  Umbach 2005 *Plant Physiol* constructs; not commercially distributed
  (no ABRC / NASC stock visible). Would need MTA for wet-lab
  re-execution.
- **Equipment.** 200 Gy γ-source at high dose-rate (typical ⁶⁰Co or
  ¹³⁷Cs research irradiator at ~10–50 Gy/min). Not present on CherryRd
  or any compute target.

## 3. Approach actually used by this slot

`code/smoke_check.py` builds a 27-gene AGI panel from the Belykh abstract
and cross-references it against the **per-DREM-path AGI gene lists**
in GSE112773 Source_Data_2 (Bourbousse 2018 SOG1 + MYB3R γ-IR Arabidopsis
DREM model). For each panel gene we report which WT and *sog1* DREM
dynamic paths it appears in, and classify "concordant with the Belykh
directional claim" = panel gene in a WT-γ-IR-induced path (W1/W2/W3/W6/W7/W8).

### Per-gene mapping (machine-readable: `results/smoke_output.json`)

| Symbol | AGI | WT-induced | WT-repressed | sog1 | Class |
|---|---|---|---|---|---|
| AOX1a | AT3G22370 | — | **W4** | **S2** | AOX primary target |
| AOX1b | AT3G22360 | — | — | — | AOX family |
| AOX1c | AT3G27620 | **W7** | — | S3 | AOX family |
| AOX1d | AT1G32350 | — | — | — | AOX stress-induced |
| AOX2 | AT5G64210 | — | — | — | AOX family |
| ATM | AT3G48190 | — | — | — | DDR kinase |
| ATR | AT5G40820 | — | — | — | DDR kinase |
| SOG1 | AT1G25580 | — | — | — | DDR master TF |
| **RAD51** | AT5G20850 | **W2** | — | S3 | HR |
| **RAD54** | AT3G19210 | **W3** | — | S3 | HR |
| **BRCA1** | AT4G21070 | **W1** | — | S2 | HR |
| **PARP1** | AT4G02390 | **W1** | — | S2 | BER |
| **PARP2** | AT2G31320 | **W3** | — | S3 | BER |
| KU70 | AT1G16970 | — | — | — | NHEJ |
| KU80 | AT1G48050 | — | — | — | NHEJ |
| LIG4 | AT5G57160 | — | — | — | NHEJ |
| OGG1 | AT1G21710 | — | — | — | BER |
| APE1L | AT3G48425 | — | **W4** | S3 | BER |
| WEE1 | AT1G02970 | — | **W4** | S3 | cell-cycle checkpoint |
| MSD1/MnSOD | AT3G10920 | — | — | — | antioxidant |
| FSD1/FeSOD | AT4G25100 | — | — | — | antioxidant |
| CSD1 | AT1G08830 | — | — | — | antioxidant |
| CSD2 | AT2G28190 | — | — | — | antioxidant |
| CAT1 | AT1G20630 | — | — | — | antioxidant |
| CAT2 | AT4G35090 | — | — | — | antioxidant |
| APX1 | AT1G07890 | — | — | — | antioxidant |
| GR1 | AT3G24170 | — | — | — | antioxidant |

### Summary metrics

- DDR panel concordance with Belykh directional claim, **among DDR
  genes detected in scaffold = 5/7 (71%)**; among all DDR panel genes
  = 5/14 (36%). The 5 concordant: RAD51, RAD54, BRCA1, PARP1, PARP2 —
  i.e. the canonical HR/BER DSB-response machinery, all landing in
  WT-γ-IR-induced DREM paths. **Zero** DDR-panel genes detected in
  WT-induced *and* WT-repressed paths inconsistently.
- 2 discordant DDR panel genes detected: **APE1L** (BER AP-endonuclease)
  and **WEE1** (post-DDR cell-cycle checkpoint), both in WT-repressed W4.
  WEE1 repression on this timescale is model-dependent (in some
  studies WEE1 is induced early then represses CDK targets).
- **AOX1a discordance** is the lateral finding worth flagging: the
  Bourbousse scaffold puts AT3G22370 in WT-repressed W4 and
  SOG1-dependent S2, partially contradicting C8 (the Belykh paper's
  core thesis that AOX1a is a primary WT γ-IR target). Caveat: time
  course (12 h post 200 Gy vs 0–24 h post 100 Gy in Bourbousse) and
  tissue (5-wk plant leaves vs seedlings) differ.
- 13/27 panel genes not detected at all in the Bourbousse DREM
  significance-filtered set — expected; DREM publishes only genes that
  pass dynamic-segmentation cutoffs.

## 4. Compute

- Smoke script: pure stdlib Python 3.14, ~50 ms wall, <30 MB RAM, CPU-only,
  zero network. Ran on CherryRd. **No heavy-compute job plan needed.**

## 5. Blockers

1. Paper closed access at T&F; no OA copy anywhere Unpaywall / EPMC index.
2. No GEO / SRA / ArrayExpress / BioStudies deposit (paper is qPCR + biochem).
3. Author contact disallowed by task scope.
4. AS-12 and XX-2 Arabidopsis lines are lab-internal (Komi); not in
   ABRC / NASC stock catalogs visible from public APIs.
5. 200 Gy high-dose-rate γ-source required for any wet-lab re-execution.
6. The Bourbousse scaffold time course and dose differ from Belykh's
   (12 h post 200 Gy, 5-wk plants vs Bourbousse 0–24 h post 100 Gy
   seedlings), so the scaffold cross-validation is *directional*, not
   quantitative.

## 6. Friction tags (proposed for the QA TSV)

`wet-lab-only`, `no-deposit`, `closed-access`, `paywall-supplement`,
`requires-custom-aox1a-line`, `requires-high-dose-rate-gamma-source`,
`qpcr-biochem-only`, `no-rna-seq`, `lateral-scaffold-cross-validated`.

## 7. QA retag recommendation (LUCID100_SOLID_MASTER_QA.tsv row 71)

- **Current worktype.** `omics/signature replication`.
- **Proposed worktype.** `wet-lab qPCR + biochem / no public deposit / lateral-scaffold-cross-validated`.
- **Current themes.** `DNA repair / DDR; dose-rate / low-dose response;
  radiation quality / RBE; omics / biomarkers / signatures`.
- **Proposed themes.** Drop `dose-rate / low-dose response` (single 200 Gy
  acute dose, not low-dose), drop `radiation quality / RBE` (γ-only, no
  comparator), drop `omics` (qPCR panel, not omics). Add
  `plant-radiobiology`, `mitochondrial-AOX`, `pro-/antioxidant-state`.
- **Current decision.** `KEEP: relevant and replication-plausible`.
- **Proposed decision.** `KEEP-for-corpus / QUANTITATIVE-REPLICATION-NOT-FEASIBLE;
  retain as mechanistic anchor for the AOX-mitochondrial-retrograde × DDR
  axis. Lateral directional cross-validation against GSE112773 already
  performed and partially supports the WT-DDR-induction claim while
  partially contradicting the AOX1a-primary-target claim.`
- **Friction tags to add.** see §6.

## 8. Next actions

1. **Apply the QA retag** in `LUCID100_SOLID_MASTER_QA.tsv` row 71 per §7
   (main agent, separate edit pass — not done here).
2. **Optional follow-up slot:** open a new LUCID100 slot for the
   Bourbousse 2018 *Genome Res* paper (PMID 30060114) itself as a much
   higher-yield Arabidopsis-γ-IR DDR computational anchor (full
   transcriptome + processed source data already in hand from this slot).
3. **Optional escalation:** institutional Wiley/T&F access via ANL
   Shibboleth could unlock the Belykh supplementary qPCR Cq table for
   numerical comparison against the scaffold — still no genotype × IR
   matrix would be replicable, but the qPCR ΔΔCq values could be
   spot-checked against scaffold log2FC.
4. **Heavy compute:** none required; not requested.


## Verdict

**Verdict: BLOCKED**. — Closed paper, wet-lab qPCR, no deposit, lab-internal lines; 0/8 quantitative, only lateral scaffold cross-validation possible

<!-- census-verdict: BLOCKED assigned 2026-07-08 by LLM judge (Argo Opus) -->
