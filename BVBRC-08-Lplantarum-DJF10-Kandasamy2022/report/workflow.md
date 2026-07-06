# Workflow — Kandasamy 2022 *L. plantarum* DJF10 Replication (Pass 1 + Pass 2)

**Paper:** Int. J. Mol. Sci. 2022, 23, 14494 · DOI 10.3390/ijms232214494 · PMID 36430971
**Reads:** SRR14598288 (Illumina NovaSeq 6000, 14.8M paired-end)
**BioProject / BioSample:** PRJNA731289 / SAMN19277818

**Verdict:** PARTIAL (Coverage 8 / Agreement 8; 17/28 VERIFIED, 11/28 PARTIAL, 0/28 CONTRADICTED, 0/28 NOT_TESTED)

---

## Overall Two-Pass Structure

| Pass | Date | Scope | Result |
|---|---|---|---|
| Pass 1 | 2026-05-10 | 22 of 28 claims (core genome features, safety screens, probiotic gene inventory) | 16 VERIFIED, 6 PARTIAL, 6 NOT_TESTED |
| Pass 2 | 2026-06-23 | Attack all 6 NOT_TESTED (all web-only tools) + rescue 1 PARTIAL | 17 VERIFIED, 11 PARTIAL, 0 CONTRADICTED, 0 NOT_TESTED |

Pass 1 report preserved verbatim at `report/REPORT.pass1.md`. Pass 2 report at `report/REPORT.md` supersedes.

---

## Pass 1 Pipeline (baseline, carried forward)

1. **Read retrieval.** `prefetch` + `fasterq-dump` on SRR14598288 → paired FASTQ.
2. **QC + trim.** `fastp` (default probiotic-grade trim, adapter auto-detect).
3. **Assembly.** SPAdes v3.15.x with `--only-assembler --careful` → 33-contig / 27-contig-filtered draft assembly, 3,382,068 bp (paper: 3,385,113 bp, −0.09%).
4. **Annotation.** Prokka v1.14.6 → 3,169 CDS (paper: 3,168).
5. **Species/ANI.** `pyani` or `fastANI` vs *L. plantarum* type-strain set → 98.3–99.1% (paper: ~99%).
6. **Safety screens.**
   - AMR: RGI/CARD + AMRFinderPlus + ResFinder → 0 hits across all three DBs (paper: absent) ✅
   - VFDB / PATRIC-VF / Victors virulence → 0 hits (paper: absent) ✅
   - Plasmids: PlasmidFinder + Platon + MOB-suite → 0 replicons (paper: no plasmids) ✅
7. **Probiotic gene inventory** (BLAST-driven, per-gene targeted):
   - Hemolysin tlyA (41.8% identity, low → non-pathogenic) ✅
   - Cold-shock cspA × 5 ✅
   - Chaperones/stress: groES/EL, clpB/C/E/L/P, hslO/V, dnaK/J — all confirmed ✅
   - Bile-salt hydrolase cbh (99.7% identity) ✅
   - Na+/H+ antiporters (NhaC + 9 additional) ✅
   - Sortase A (strA) ✅
8. **Prophages / islands / CRISPR / IS / CAZymes / SEED / KEGG.** Deferred to pass 2 (all web-tool dependent in the paper's methodology).

Pass-1 outputs live in `results/pass1/` (assembly, Prokka GBK, blast tables, safety-screen JSONs, ANI matrices).

---

## Pass 2 Pipeline (attacks the 6 NOT_TESTED claims)

For each claim, the strategy is: (i) find a free, offline surrogate for the web tool the paper used; (ii) run at the standard field cutoff; (iii) if it undershoots, add one falsifiable custom scorer; (iv) name the honest blocker if it still comes up PARTIAL.

### 1. Prophages (claim 23) — PHASTER surrogate

```
Prokka v1.14.6 (--fast) → 3,169 CDS
  ↓
phispy v5.0.10 (Lactococcus training set, --include_annotations, --phmms)
  + 25 phage Pfam HMMs (PF00589 integrase, PF02899/PF13495 integrase-SAM,
    6× Terminase, Holin, Phage_lysozyme, CHAP, baseplate, capsid, portal, tail)
  ↓
phispy RF classifier → 0 regions (needs pVOG-level coverage)
  ↓
Custom PHASTER-style scorer (code/repass/find_prophages.py):
  for each integrase: inspect ±30 ORFs for additional phage HMM hits
  ↓
6 candidate regions → 2 INTACT-LIKE
  ↓
Coordinate cross-check vs paper Table:
  R1 integrase — 34 bp offset ✅
  R2 integrase — 98 bp offset ✅
  R3 — assembly-contig ambiguous ⚠
```

Outputs: `results/repass/prophage/SUMMARY.md`, `integrase_neighborhoods.json`, `custom_prophages.json`, `phispy_v4/`, `/tmp/phage_hits.tbl`.

### 2. SEED subsystems (claim 24) — RAST surrogate

```
Prokka v1.14.6 full-annotation GBK
  ↓
code/repass/seed_subsystem_count.py:
  25-bucket regex mimicking SEED top-level subsystems
  one-CDS-in-at-most-one-bucket (first match wins, RAST-ordered)
  ↓
481 / 3,169 CDS (15.2%) classified vs paper ~35% (1,119/3,168)
18 / 25 categories within ±4% absolute
All 25 categories represented
```

Blocker: FIGfam HMMs are closed-source (BV-BRC / RASTtk web-only).
Outputs: `results/repass/subsystems/SUMMARY.md`, `seed_subsystem_counts.json`, `SUBSYSTEM_OUTPUT.txt`.

### 3. KEGG BRITE (claim 25) — BlastKOALA surrogate

```
Pass-1 SwissProt blastp → 961 EC-annotated CDS
  ↓
code/repass/kegg_brite_map.py:
  KEGG REST /link/pathway/ec → pathway IDs
  KEGG REST /get/br:ko00001 → BRITE hierarchy
  walk to top-level + second-level category
  ↓
Per-category counts vs paper Table 3 (22 categories)
  ↓
Carbohydrate metabolism: 240 vs 226 ✅ (within 6%)
Other metabolism categories over-call 2–10× (EC fan-out)
Non-EC categories un-callable
```

Blocker: KofamScan profile DB (1.5 GB) did not finish downloading; tractable retry.
Outputs: `results/repass/kegg/SUMMARY.md`, `kegg_brite_counts.json`.

### 4. CAZymes (claim 26) — dbCAN surrogate

```
Download dbCAN-HMMdb V13 (826 HMMs, 120 MB) from pro.unl.edu/dbCAN2/download/Databases/V13/
  ↓
hmmscan against Prokka proteins (3,169 CDS)
  ↓
Filter at standard dbCAN cutoff:
  independent E < 1e-15, HMM coverage ≥ 0.35
  ↓
Class tally: GH 58, GT 35, CE 5, AA 3, CBM 0/14 (strict/relaxed)
Total: 101 (paper: 98) → +3%
```

Outputs: `results/repass/cazy/SUMMARY.md`, `DJF10_cazy.tbl`, `DJF10_cazy.domtbl`.

### 5. Genomic islands (claim 27) — IslandViewer surrogate

```
Install IslandPath-DIMOB v1.0.6 (bioconda)
  patch missing Bio/Perl.pm shim (bioconda BioPerl omission)
  ↓
DIMOB on annotated GBK → 0 islands
  (33-contig draft defeats dinucleotide-bias sliding window)
  ↓
Custom hypothetical-rich window (code/repass/find_islands*.py):
  20 CDSs, ≥60% hypothetical, ≥1 mobility marker, len ≥4 kb
  overlapping windows merged
  ↓
10 candidate islands, 28–100 kb (paper: 18 islands, 4–70 kb)
```

Blocker: IslandViewer 4 fuses DIMOB + SIGI-HMM + IslandPick over a curated reference genome pool.
Outputs: `results/repass/islands/SUMMARY.md`, `custom_islands_v2.json`, `DJF10_GIs_v3.gff`, `islandpath_v3.log`.

### 6. Bacteriocin clusters (claim 28) — BAGEL4 surrogate

```
UniProt L. plantarum C11 plantaricin cluster fetch:
  plnA, plnE, plnF, plnJ, plnK, plnN, plnI, plnP, plnL, plnM,
  plnD, plnC, plnG, plnQ, plnR (+ sactipeptide BmbF placeholder)
  → 16-protein reference FASTA
  ↓
tblastn vs SPAdes assembly, E < 1e-5
  ↓
NODE_10 hits at 51.5–58.7 kb:
  plnF 100% identity, plnN 100%, plnJ 100% (52–56 aa, E ≤ 4e-30)
  plnA 85% identity, plnG ABC transporter 56.6–58.7 kb
  → full 4-peptide cluster + transporter ✅
  ↓
hmmscan vs Pfam PF04055 (Radical_SAM), E < 1e-10
  → 3 hits, all in metabolic context (PFL activase, GTP cyclase)
  → sactipeptide cluster NOT_DETECTED ⚠ (BAGEL4 RiPP HMMs proprietary)
```

Outputs: `results/repass/bacteriocin/bagel_summary.md`, `bagel_tblastn.tsv`.

---

## Code Layout

```
code/
├── pass1/                       # (implicit) pass-1 blast + annotation drivers
└── repass/
    ├── seed_subsystem_count.py  # SEED regex bucketing
    ├── kegg_brite_map.py        # KEGG REST → BRITE
    ├── find_prophages.py        # integrase-neighborhood scorer
    └── (find_islands*.py moved here from /tmp)
```

## Results Layout

```
results/
├── pass1/                       # assembly, Prokka, ANI, blast, safety, probiotic-gene tables
└── repass/
    ├── prophage/                # SUMMARY.md, JSONs, phispy_v4/, phage_hits.tbl
    ├── subsystems/              # SUMMARY.md, seed_subsystem_counts.json, SUBSYSTEM_OUTPUT.txt
    ├── kegg/                    # SUMMARY.md, kegg_brite_counts.json
    ├── cazy/                    # SUMMARY.md, DJF10_cazy.tbl, DJF10_cazy.domtbl
    ├── islands/                 # SUMMARY.md, custom_islands_v2.json, DJF10_GIs_v3.gff, log
    ├── bacteriocin/             # bagel_summary.md, bagel_tblastn.tsv
    └── databases/               # dbCAN-HMMdb V13, phage Pfam HMMs
```

## Report Layout

```
report/
├── REPORT.md                    # pass-2 canonical
├── REPORT.pass1.md              # pass-1 verbatim
├── REPORT.tex                   # LaTeX rendering (this backfill)
├── open_questions.json          # 5 truly open scientific questions
├── workflow.md                  # this file
├── artifacts_summary.md
└── failure_analysis.md
```

Root: `PARSER_PROVENANCE.md` (pdftotext -layout audit of every claim).

## Compliance Rails
- Free / Argo-only — no paid services, no PHASTEST API, no BV-BRC submissions.
- No fabricated numbers — every count crossed against a Prokka/hmmscan/blast/JSON artifact.
- Every PARTIAL carries a named blocker.
- Pass-1 preserved unchanged; pass-2 report explicit about what it supersedes.
