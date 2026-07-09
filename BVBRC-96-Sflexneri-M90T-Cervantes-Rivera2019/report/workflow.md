# Workflow — BVBRC-96 replication of Cervantes-Rivera, Tronnet & Puhar (2020)

**Paper:** *Shigella flexneri* serotype 5a M90T complete genome + dRNA-seq TSS.
BMC Genomics 21:285 (2020). DOI 10.1186/s12864-020-6565-5.
**Set:** BVBRC-96 · **Analyst:** Ollie (OpenClaw AI subagent) · **Date:** 2026-07-04
**Compute:** uicgpu (8×A100, 255 cores, 2 TB RAM) for heavy work; CherryRd local workspace
for light data pulls. **Free endpoints only** (NCBI Datasets REST v2 unauth; Argo proxy
`localhost:44497` for LLM inference).

---

## Step 0. Duplicate check (wave-brief rule)

Scanned `~/Dropbox/REPLICATE-PROJECT/` for prior work on the same paper.
- Sibling found: `BVBRC-54-Sflexneri-M90T-genome-Cervantes2020/` (verdict: PARTIAL, strong).
- Per wave-brief "do not overwrite existing sibling" rule, that dir was NOT touched.
- Created fresh target `BVBRC-96-Sflexneri-M90T-Cervantes-Rivera2019/` and worked in a
  separate uicgpu directory.

## Step 1. Assembly identification

- **Target accession:** `GCF_004799585.1` (deposited by Umeå University via BioProject
  PRJNA510559; the paper's own submitter).
- **API call:** NCBI Datasets REST v2 `dataset_report` endpoint.
- **Confirmation:** Complete Genome · 2 replicons · released 2019-04-18 · total 4,828,909 bp
  (= 4,596,714 chromosome + 232,195 plasmid, matching paper exactly).

## Step 2. Genome package download

- `curl` on NCBI Datasets v2 `download` endpoint for FASTA + GFF + PROT + SEQUENCE_REPORT.
- **Output:** `work/genome.zip` (2,695,927 bytes).
- **FASTA MD5:** `b42e8cb5771af766febc5a841847ed3e`.
- **Replicons:**
  - Chromosome `NZ_CP037923.1` (4,596,714 bp).
  - Plasmid pWR100 `NZ_CP037924.1` (232,195 bp).

## Step 3. PlasmidFinder (BVBRC-96 workflow leg: PlasmidFinder + Similar Genome Finder)

- **Environment (uicgpu):** conda env `/data/stevens/envs/bvbrc28`.
- **Command:** `abricate --db plasmidfinder --nopath --quiet <FASTA>`.
- **Result:** single hit **IncFII_1** on `NZ_CP037924.1` @ 101,994–102,253, coverage 99.62%
  (261/261), identity 96.17%, accession AY458016 (DB date 2017-03-19).
- **Interpretation:** pWR100 is IncF-family (IncFII), independently confirming the paper's
  virulence-megaplasmid characterization.

## Step 4. Specialty Genes (BVBRC-96 workflow leg: VFDB + Victors, CARD context)

- **VFDB scan:** `abricate --db vfdb`. 172 total hits: 108 chromosome + 64 plasmid.
- **Cross-check:** enumerated the full plasmid VF hit list; matched against paper's
  virulence-factor description.
- **CARD scan:** `abricate --db card`. 57 hits (resistance-context, not a paper claim).

## Step 5. Master regulators via PGAP GFF `gene=` search

- **Command family:** `grep 'gene=vir[FB]' <GFF>` on `NZ_CP037924.1`.
- **Result:** `virF` at 52,310–53,098 (+ strand); `virB` at 203,045–203,974 (+ strand).
- **Interpretation:** independently confirms the paper's description of the plasmid-encoded
  T3SS regulatory cascade (virF → virB → mxi/spa/ipa operons).

## Step 6. Comprehensive Genome Analysis (BVBRC-96 workflow leg: RASTtk-equivalent)

- **Method:** parse the deposited PGAP GFF for CDS / tRNA / rRNA / ncRNA / pseudogene /
  riboswitch totals; per-replicon CDS breakdown; grep IS transposases.
- **Results (this replication):** 5,003 CDS (4,706 chr + 297 plasmid) · 102 tRNA · 22 rRNA
  (= 7 operons) · 3 ncRNA · 7 riboswitch · 757 pseudogene · 585 IS transposases
  (grep `product=IS[0-9]`) / 617 (grep `transposase`).
- **Note on IS count discrepancy vs paper's ~402:** driven by pipeline choice (PGAP here vs
  BV-BRC RAST in paper). Qualitatively consistent (both confirm Shigella-typical high IS
  density); quantitatively differs.

## Step 7. Similar Genome Finder (BVBRC-96 workflow leg)

- **Comparator panel (6 genomes via NCBI Datasets):**
  Sf 2a 301, Sf 5b 8401, S. sonnei Ss046, S. dysenteriae Sd197, S. boydii Sb227, E. coli K12
  MG1655.
- **Tools:** mash 2.3 (sketch + dist); fastANI (query-vs-reference-list).
- **Result:** Sf 5b 8401 is nearest (fastANI 99.933%, mash 0.00113, aligned fraction 0.940);
  E. coli K12 MG1655 at 97.808% ANI reflects the Shigella-inside-Escherichia phylogeny.

## Step 8. LLM-judge verdict

- **Endpoint:** Argo proxy (`localhost:44497`), free CELS endpoint.
- **Model:** `argo:claude-opus-4.7`.
- **Input:** the assembled evidence bundle (all TSVs + PGAP-parse summary + fastANI table).
- **Output:** `report/evidence/judge_verdict.md` (verdict + reasoning).
- **Verdict:** PARTIAL REPLICATION (strong).

## Step 9. Reporting

- `report/REPORT.md` — canonical markdown (source of truth for this backfill).
- `report/REPORT.tex` — LaTeX rendering with dedicated Genuine Critique section.
- `report/open_questions.json` — 5 forward-looking scientific questions.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — listing + provenance of evidence files.
- `report/failure_analysis.md` — what was NOT tested and why, with recovery plan.

---

## Guardrails

- **Only FREE endpoints.** No Anthropic/OpenAI/OpenRouter direct calls. Argo proxy only.
- **Sibling not overwritten.** BVBRC-54 sibling left untouched.
- **Compute-lane discipline.** Heavy work on uicgpu (Ollie-owned LUCID/BVBRC lane); local
  workspace only for lightweight data pulls and report generation.
- **Do-not-fabricate rule.** All numbers in this workflow trace to a specific TSV, JSON, or
  GFF file under `report/evidence/`.
