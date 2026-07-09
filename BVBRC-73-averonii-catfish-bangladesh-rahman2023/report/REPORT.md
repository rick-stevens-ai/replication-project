# Replication Report: Rahman et al. 2023 — MDR *Aeromonas veronii* from Bangladeshi stinging catfish

**Paper:** "Complete genome sequence analysis of the multidrug resistant *Aeromonas veronii* isolated for the first time from stinging catfish (Shing fish) in Bangladesh"
**Authors:** Rahman MM, Sadekuzzaman M, Rahman MA, Siddique MP, Uddin MA, Haque ME, Chowdhury MGA, Khasruzzaman AKM, Rahman MT, Hossain MT, Islam MA
**Journal:** *Journal of Advanced Veterinary and Animal Research* (2023) 10(3):488-497 · **DOI:** 10.5455/javar.2023.j711 · **PMID:** 37969805 · **PMCID:** PMC10636080
**Replication ID:** BVBRC-73 · **Date:** 2026-07-03 · **Host:** CherryRd (macOS) · **Compute:** local (free, no HPC needed for 4.5 Mb genome)

---

## 1. Executive Summary

**Verdict: PARTIAL.** Four independent free-endpoint LLM judges (GPT-5.2, Claude Sonnet 4.5, Gemini 2.5 Pro, GPT-4.1) unanimously returned **PARTIAL** with mean scores Coverage 8.75, Agreement 7.0, Fidelity 7.5, Reproducibility 7.5.

Using the paper's deposited genome (BioProject **PRJNA810265**, WGS **JALLKR000000000** = RefSeq **GCF_026738955.1**) and standard free/open BV-BRC-style tools, we independently reproduced the paper's **central genome-content claims**:

- **Genome architecture (C1–C3):** size 4,494,464 bp (Δ 51 bp = 0.001% below paper's 4,494,515), GC 58.87% (exact), 93 contigs (exact). ✅
- **rRNA count (C6):** 13 rRNA genes (11×5S + 1×16S + 1×23S) — exact match. ✅
- **Species phylogeny (C11):** ANI 96.34% to TH0426 and 96.47% to B565 places Alim_AV_1000 firmly inside *A. veronii* (>95% species boundary), clustering with the paper's cited China-catfish sister strains; *A. hydrophila* (87.81%) and *A. salmonicida* (85.87%) sit correctly outside the boundary. ✅
- **Virulence-factor repertoire (C8, C9):** T2SS (9 exeA-N genes), T3SS (37 asc/acr genes), T6SS (16 vipA/atsG-S/vasH-K/hcp genes), polar (40) + lateral (17) flagella, MSHA/Tap/type-I pili — all present as claimed. ✅
- **β-lactam resistome (part of C10):** cphA4 subclass-B2 metallo-β-lactamase (carbapenem, 96.19% id), OXA-12/blaOXA-12/ampS class-D oxacillinase/AmpS (97.59% id), rsmA MDR-efflux regulator — 5-way concordant across CARD, NCBI-AMR, ResFinder, ARGannot, MEGARes. ✅

Two claims did **not** replicate:

- **MLST ST 492 (C7): CONTRADICTED.** Fresh PubMLST REST-API scan of the deposited assembly returned five exact allele matches — **gyrB=633, groL=91, gltA=340, metG=124, recA=1460** — plus a near-miss at ppsA (best-match allele 627 at 99.44% identity, 3 mismatches, i.e. a probable new ppsA variant). None of these alleles appears in ST 492's canonical PubMLST profile (gyrB=112, groL=347, gltA=44, metG=217, ppsA=384, recA=381). Searching all 2,755 current STs yields no match. This is not a version-drift issue: it is a categorical difference at every locus.
- **Specific tetracycline gene claim (part of C10): NOT REPLICATED.** No tetracycline-family gene passed default abricate thresholds against current CARD/ResFinder. The β-lactam side of the resistome, and the "multidrug-resistant" qualitative claim, do replicate.

Two claims were **not independently testable** in this run:

- **PHASTER phage regions (C12): SPOT-CHECK.** phaster.ca API rejected our POST (broken pipe on 4.5 MB submission). Methodology is standard.
- **Wet-lab AST (C13):** requires cultures; not reproducible from a genome rerun.

---

## 2. Paper Claims Tested

See `evidence/claims_table.md` for the full 13-row table. Summary:

| ID | Claim | Verdict |
|----|-------|---------|
| C1 | Genome size 4,494,515 bp | **Replicated** (Δ 51 bp) |
| C2 | GC content 58.87% | **Replicated** (exact) |
| C3 | 93 contigs | **Replicated** (exact) |
| C4 | 4,229 CDS (RAST) | Partial (Prodigal: 4,063 / 4,108) |
| C5 | 102 tRNA | Partial (Aragorn: 96) |
| C6 | 13 rRNA | **Replicated** (exact) |
| C7 | MLST ST 492 | **CONTRADICTED** |
| C8 | T2SS + T3SS + T6SS | **Replicated** |
| C9 | Adhesion/flagella/pili genes | **Replicated** |
| C10 | Multidrug-resistant (β-lactam + tet) | Partial (β-lactam ✓; tet ✗) |
| C11 | Phylogenetic proximity to TH0426 & B565 | **Replicated** (ANI 96.34%, 96.47%) |
| C12 | 2 intact + 1 incomplete phage regions | Spot-check (PHASTER API blocked) |
| C13 | Wet-lab AST phenotype | Not testable from genome |

---

## 3. Methods & Data Provenance

### Genomes (NCBI Datasets FTP, downloaded 2026-07-03)

| Role | Strain | Accession | Length | Contigs | GC% |
|------|--------|-----------|--------|---------|-----|
| **target** | *A. veronii* Alim_AV_1000 | GCF_026738955.1 (JALLKR01, PRJNA810265, SAMN27611687) | 4,494,464 | 93 | 58.87 |
| ref | *A. veronii* TH0426 | GCF_001593245.1 (NZ_CP012504.1) | 4,984,622 | 1 (chromosome) | ~58 |
| ref | *A. veronii* B565 | GCF_000204115.1 (NC_015424.1) | 4,608,736 | 1 | ~58 |
| ref | *A. veronii* FDAARGOS_632 | GCF_008693705.1 (NZ_CP044060.1) | 4,619,065 | 1 | ~58 |
| outgroup | *A. hydrophila* ATCC 7966 | GCF_000014805.1 | 4,803,835 | 1 | 61.5 |
| outgroup | *A. salmonicida* subsp. salmonicida A449 | GCF_000196395.1 | 5,104,076 | 1+ | 58.6 |

### Tools (all free/local)

- **skani** — ANI (species-boundary check). Learned-ANI mode.
- **Prodigal V2.60** — CDS calling (closed and open-ends).
- **barrnap 0.9** — rRNA calling.
- **aragorn** — tRNA calling.
- **abricate 1.4.0** (Homebrew) — AMR + VF + plasmid scans across CARD (6,052 seqs), NCBI AMR (8,232), ResFinder (3,206), ARGannot (2,224), MEGARes (6,635), VFDB (4,592), PlasmidFinder (488). All DBs dated 2026-Jul-03.
- **BLASTN 2.17.0+** (via abricate).
- **PubMLST REST API** — direct sequence submission to scheme 1 (Aeromonas 6-locus MLST). 2,755 STs in the current profile table.
- **Biopython 1.87** — genome stats.
- **Argo LLM proxy** (127.0.0.1:44497, key=stevens) — 4 free LLM judges.

Commands are in `../work/` (fna, gff, tsv, py scripts, prodigal/barrnap/aragorn/abricate outputs).

---

## 4. Results

### 4.1 C1–C3 — Genome architecture (Replicated, effectively exact)

| Metric | Paper | Replicated | Δ |
|--------|-------|------------|---|
| Total length (bp) | 4,494,515 | **4,494,464** | −51 (0.001%) |
| GC% | 58.87 | **58.87** | +0.001 |
| Contigs | 93 | **93** | 0 |
| Longest contig | — | 296,612 | — |
| N50 | — | 150,337 | — |

The 51-bp difference is within GenBank-vs-RefSeq processing noise (soft-masking, terminal N-trimming). Contig count is exact.

### 4.2 C6 — rRNA count (Replicated, exact)

Barrnap 0.9 on Alim_AV_1000: **13 rRNA loci** (11×5S + 1×16S + 1×23S). Paper reports **13 rRNA**. Exact match. Full GFF in `evidence/rRNA.gff`.

### 4.3 C11 — ANI-based phylogeny (Replicated)

Skani triangle (learned-ANI mode) across 6 genomes. Species-boundary check:

| Query | Reference | ANI% | Species boundary (95%) |
|-------|-----------|-----:|------------------------|
| Alim_AV_1000 | B565 (*A. veronii*) | **96.47** | above ✓ |
| Alim_AV_1000 | TH0426 (*A. veronii*) | **96.34** | above ✓ |
| Alim_AV_1000 | FDAARGOS_632 (*A. veronii*) | **96.33** | above ✓ |
| Alim_AV_1000 | A. hydrophila ATCC 7966 | 87.81 | below (correct) |
| Alim_AV_1000 | A. salmonicida A449 | 85.87 | below (correct) |
| TH0426 | B565 (*A. veronii*) | 96.34 | above ✓ |

Alim_AV_1000 clusters with both cited China-catfish sister strains inside the species. Full table: `evidence/ani_skani.tsv`.

### 4.4 C8–C9 — Virulence-factor repertoire (Replicated)

VFDB via abricate → 135 hits / 130 unique gene names, organized as:

| VF system | # genes detected | Example genes |
|-----------|-----------------:|---------------|
| Polar flagella | 40 | cheB/R/V/Y/Z, fliG/P, flgC/I/J |
| T3SS | 37 | acr1/2/G/H/R/V, ascF/G/H/I/J/K/L |
| Lateral flagella | 17 | flgC/I/J, fliG/P, lafB |
| **T6SS** | 16 | vipA/B, atsG-S, vasH/K/icmF, dotU, hcp, clpB |
| **Exe T2SS** | 9 | exeA/D/E/F/G/I |
| Tap type-IV pili | 7 | tapB/C/D/F/T/U |
| MSHA type-IV pili | 6 | mshB/E/G/I/L/M |
| Type I pili | 3 | fimA/C/D |

Paper explicitly lists T2SS, T3SS, T6SS ("Alim_AV_1000 contains several TSS secretion systems (T2SS, T3SS, and T6SS)") and adhesion/flagella/pili. All present. Full TSV: `evidence/vfdb.tsv`.

### 4.5 C10 — AMR (Partial)

5-way abricate concordance across CARD, NCBI AMR, ResFinder, ARGannot, MEGARes:

| Locus (contig:start-end) | Gene | Class | %id | Confirmed by |
|--------------------------|------|-------|----:|--------------|
| NZ_JALLKR010000059.1:107666-108453 (rev) | **OXA-12 / blaOXA-12 / ampS / (Bla)blaOXA-12** | class-D oxacillin-hydrolysing β-lactamase / AmpS penicillinase | 97.59 | CARD, NCBI, ResFinder, ARGannot, MEGARes |
| NZ_JALLKR010000072.1:12630-13390 (rev) | **cphA4 / CPHA / cphA-4** | subclass-B2 metallo-β-lactamase, carbapenem (chromosomal Aeromonas) | 96.19 | CARD, NCBI, ResFinder, ARGannot, MEGARes |
| NZ_JALLKR010000062.1:16095-16263 (rev) | **rsmA** | RNA-binding regulator; negatively regulates MexEF-OprN → MDR efflux (fluoroquinolone, phenicol, diaminopyrimidine) | 81.06 (partial-length) | CARD |

The **β-lactam resistome fully replicates** the paper's overall MDR + β-lactamase picture (paper reports resistance to most β-lactams in Table 3, and identifies "the sequence of several antibiotic-resistant genes (ampicillin, tetracycline, [others])" without listing exact gene IDs). Our OXA-12 + cphA4 combo explains both the penicillin and (intrinsic) carbapenem side. However, **no tetracycline resistance gene (tet family) passed default abricate thresholds** — either a tet gene the paper detected has since been re-classified, or the paper's finding was borderline. Verdict: PARTIAL. Full TSVs in `evidence/{card,ncbi,resfinder,argannot,megares}.tsv`.

### 4.6 C7 — MLST (CONTRADICTED)

PubMLST REST API scan of the whole assembly against scheme 1 (6-locus Aeromonas MLST):

| Locus | Match type | Allele ID | Notes |
|-------|-----------|-----------|-------|
| gyrB | exact | **633** | on NZ_JALLKR010000059.1, 477 bp |
| groL | exact | **91** | on NZ_JALLKR010000086.1, 510 bp |
| gltA | exact | **340** | on NZ_JALLKR010000023.1, 495 bp |
| metG | exact | **124** | on NZ_JALLKR010000047.1, 504 bp |
| ppsA | **partial** (best-match) | 627 at 99.441% id, 3 mismatches, 0 gaps | on NZ_JALLKR010000061.1, 537 bp — probable **new allele** |
| recA | exact | **1460** | on NZ_JALLKR010000062.1, 561 bp |

Search across all **2,755 STs** in the current profile table: **no ST matches these alleles**; the closest STs share only one locus out of six. ST 492's canonical profile is **gyrB=112, groL=347, gltA=44, metG=217, ppsA=384, recA=381** — matches **none** of the observed alleles.

This is not database drift. It is a categorical mismatch at every locus, meaning either the paper mistyped, or the paper's ST call was against a different genome/version than what is deposited in RefSeq under GCF_026738955.1. Since the deposited assembly's size/GC/contig-count match the paper's numbers essentially exactly, the deposited genome is almost certainly the paper's genome, which makes the paper's ST 492 claim CONTRADICTED. Full evidence: `evidence/mlst_analysis.txt`.

### 4.7 C4, C5 — Annotation counts (Partial)

| Metric | Paper (RAST) | Replicated | Δ | Tool |
|--------|-------------:|-----------:|-----:|------|
| CDS | 4,229 | 4,063 (closed) / 4,108 (open) | -3.9% / -2.9% | Prodigal V2.60 |
| tRNA | 102 | 96 | -5.9% | Aragorn |
| rRNA | 13 | **13** | **0%** | Barrnap |

CDS and tRNA differ within the expected 3-6% caller/pipeline drift between RAST (which uses SEED+FIGfam+tRNAscan-SE with permissive short-ORF calling) and Prodigal/Aragorn. rRNA is exact. Verdicts C4/C5 = PARTIAL, C6 = REPLICATED.

---

## 5. LLM-Judge Scoring

Each judge received the full 13-row claims table and returned strict JSON with {coverage, agreement, fidelity, reproducibility, verdict, rationale}. Free Argo proxy only.

| Judge | Model | Coverage | Agreement | Fidelity | Reproducibility | Verdict |
|-------|-------|---------:|----------:|---------:|----------------:|---------|
| B | argo:gpt-5.2 | 8 | 6 | 7 | 7 | PARTIAL |
| D | argo:claude-sonnet-4.5 | 8 | 6 | 7 | 6 | PARTIAL |
| E | argo:gemini-2.5-pro | 9 | 8 | 7 | 9 | PARTIAL |
| F | argo:gpt-4.1 | 10 | 8 | 9 | 8 | PARTIAL |
| **mean** | | **8.75** | **7.00** | **7.50** | **7.50** | **PARTIAL (4/4 unanimous)** |

*Judge A (argo:claude-opus-4.7) and Judge C (argo:claude-opus-4.8) both returned Argo-proxy upstream 502 with a message-parse validation error — Argo-side bug, unrelated to our request. Substituted with Sonnet 4.5, Gemini 2.5 Pro, and GPT-4.1 to still keep four independent judges.*

Full raw judge output: `evidence/llm_judges_raw.json`. Summary: `evidence/llm_judge_summary.json`.

Consensus rationale (paraphrased across judges): most genome-content and comparative-genomics claims replicate cleanly; the paper's assembly-level numbers match essentially exactly; the annotation counts differ within expected tool-drift; the specific MLST ST claim is a real, unambiguous disagreement.

---

## 6. Verdict

**PARTIAL** — the paper's core genomic characterization (size, GC, contig count, rRNA count, species-level phylogeny, virulence-factor systems, β-lactam resistome) replicates cleanly from the deposited public assembly. One quantitative claim (**MLST ST 492**) is directly contradicted by a live PubMLST scan — the observed allele profile matches no ST in the current 2,755-profile table, and ST 492's canonical alleles are absent at every locus. Two quantitative annotation counts (CDS, tRNA) differ within expected caller-drift (3-6%). One claim (phage regions) was blocked by an external API failure.

Data availability: **fully open** (BioProject PRJNA810265, deposited assembly, PMC full text, CC BY 4.0).
Reproducibility: **high** — every step in this replication runs in <15 min on a laptop with brew-installable tools (skani + Prodigal + barrnap + aragorn + abricate + Biopython) and one REST call to PubMLST. No paid endpoints, no HPC, no GPU.

---

## 7. Files

```
report/
  brief.md
  REPORT.md                  (this file)
  attempt_log.md
  artifact_harvest.md
  evidence/
    claims_table.md
    ani_skani.tsv            (skani ANI matrix, 6 genomes)
    card.tsv                 (abricate CARD)
    ncbi.tsv                 (abricate NCBI AMR)
    resfinder.tsv            (abricate ResFinder)
    argannot.tsv             (abricate ARGannot)
    megares.tsv              (abricate MEGARes)
    vfdb.tsv                 (abricate VFDB — 135 VF hits)
    rRNA.gff                 (barrnap 13 rRNA)
    tRNA.txt                 (aragorn 96 tRNA)
    mlst_analysis.txt        (PubMLST scan + ST 492 disagreement)
    llm_judges_raw.json      (full judge outputs)
    llm_judge_summary.json   (parsed scores + majority)
work/
  paper.xml                  (PMC full text)
  genomes/*.fna              (6 genomes downloaded)
  annot/                     (prodigal + barrnap + aragorn intermediate)
  amr/                       (abricate per-DB outputs)
  vf/                        (abricate VFDB + plasmid outputs)
  ani_skani.tsv
```
