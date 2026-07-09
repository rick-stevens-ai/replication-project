# Replication Workflow — BVBRC-107 (González-Escalona et al. 2019, STEC O26:H11)

Compute host: `ssh uicgpu` (micromamba env `amr`: blastn 2.16.0, AMRFinderPlus 3.12.8 + DB 2024-07-22.1, mlst 2.35.0).
Target paper: *PLoS ONE* 14(7):e0220494, DOI 10.1371/journal.pone.0220494.
Verdict: **PARTIAL** (downstream biology replicates; cross-platform assembly comparison not re-executed).

## Pipeline overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. FETCH PacBio closed assemblies from NCBI Nucleotide (efetch)    │
│     CP037941–CP037947  →  work/ncbi_fasta/                          │
├─────────────────────────────────────────────────────────────────────┤
│  2. CLONE reference DBs from CGE Bitbucket:                         │
│     plasmidfinder_db, virulencefinder_db, resfinder_db,             │
│     serotypefinder_db                                               │
│     Also: amrfinder_update  (NCBI AMRFinderPlus DB v2024-07-22.1)   │
├─────────────────────────────────────────────────────────────────────┤
│  3. PER-STRAIN CONCATENATE  chr + plasmid(s) → single FASTA         │
│     343 = CP037943 + CP037944                                       │
│     346 = CP037945 + CP037946 + CP037947                            │
│     350 = CP037941 + CP037942                                       │
├─────────────────────────────────────────────────────────────────────┤
│  4. SCREENS (per strain):                                           │
│     (a) SerotypeFinder BLAST      → O:H call                        │
│     (b) mlst --scheme ecoli_achtman_4  → ST assignment              │
│     (c) PlasmidFinder BLAST       → per-contig replicon type        │
│     (d) AMRFinderPlus --organism Escherichia --plus                 │
│         → acquired AMR genes + virulence genes                      │
│     (e) BLAST vs virulence_ecoli.fsa  → virulence cross-check       │
├─────────────────────────────────────────────────────────────────────┤
│  5. AGGREGATE → report/evidence/*.tsv + gene_summary.json           │
├─────────────────────────────────────────────────────────────────────┤
│  6. COMPARE against paper Tables 5/6/7 + AMR list                   │
├─────────────────────────────────────────────────────────────────────┤
│  7. LLM-JUDGE (Argo argo:gpt-5.2) → verdict JSON                    │
└─────────────────────────────────────────────────────────────────────┘
```

## Step-by-step commands (executed)

### 1. Fetch deposited PacBio assemblies
```bash
for acc in CP037941 CP037942 CP037943 CP037944 CP037945 CP037946 CP037947; do
  efetch -db nuccore -id "$acc" -format fasta > work/ncbi_fasta/${acc}.fasta
done
```
Result: 7 GenBank records, sizes matching paper Table 6 within 1–2 kb.

### 2. Reference databases
```bash
git clone https://bitbucket.org/genomicepidemiology/plasmidfinder_db.git
git clone https://bitbucket.org/genomicepidemiology/virulencefinder_db.git
git clone https://bitbucket.org/genomicepidemiology/resfinder_db.git
git clone https://bitbucket.org/genomicepidemiology/serotypefinder_db.git
amrfinder_update -d amrfinderdb
```

### 3. Per-strain concatenation
```bash
cat work/ncbi_fasta/CP037943.fasta work/ncbi_fasta/CP037944.fasta > work/strain_343.fasta
cat work/ncbi_fasta/CP037945.fasta work/ncbi_fasta/CP037946.fasta \
    work/ncbi_fasta/CP037947.fasta > work/strain_346.fasta
cat work/ncbi_fasta/CP037941.fasta work/ncbi_fasta/CP037942.fasta > work/strain_350.fasta
```

### 4. Screens (per strain)
```bash
BLASTFLAGS="-perc_identity 90 -qcov_hsp_perc 60 -evalue 1e-30 -outfmt 6"

# (a) Serotype
blastn -query work/strain_${S}.fasta -db serotypefinder_db/all $BLASTFLAGS \
  > report/evidence/serotype_${S}.tsv

# (b) MLST
mlst --scheme ecoli_achtman_4 work/strain_${S}.fasta > report/evidence/mlst_${S}.tsv

# (c) Plasmid replicons
blastn -query work/strain_${S}.fasta -db plasmidfinder_db/enterobacteriaceae \
  $BLASTFLAGS > report/evidence/plasmidfinder_${S}.tsv

# (d) AMRFinderPlus
amrfinder --nucleotide work/strain_${S}.fasta --organism Escherichia --plus \
  -d amrfinderdb/latest --threads 8 > report/evidence/amrfinder_${S}.tsv

# (e) Virulence cross-check
blastn -query work/strain_${S}.fasta -db virulencefinder_db/virulence_ecoli.fsa \
  $BLASTFLAGS > report/evidence/virulence_blast_${S}.tsv
```

### 5. Aggregate → gene_summary.json
Per-strain gene-presence matrix built by parsing all `report/evidence/*_${S}.tsv`
into a single JSON keyed by (strain, gene) → {present, %id, %cov, source_tool}.

### 6. Compare vs paper
Diff table (see REPORT.md §4): serotype 3/3, MLST 3/3, plasmid replicons match,
AMR 6/6 in 346 (others none), Table 7 virulence 6/6 across all 3 strains,
common virulence 17/18 (astA/gad below AMRFinderPlus panel).

### 7. LLM-judge
```bash
curl -sS $ARGO/chat/completions -H "Authorization: Bearer stevens" \
  -H "Content-Type: application/json" -d @judge_prompt.json \
  > report/verdict.json
# → verdict=PARTIAL, coverage_score=70, agreement_score=98
```

## What was NOT re-executed (why verdict is PARTIAL)

Claims C9 (MinION vs PacBio congruent) and C10 (MiSeq misses toxB/tccP/iha/astA)
require running Canu v1.6+ on SRR8335317–18 (MinION) and SPAdes on
SRR8333590–92 (MiSeq), ~30 GB total. Deferred to a future replication expansion.

## Reproducibility notes

* All input data (CP037941–CP037947) is public via NCBI eutils, no auth.
* All reference DBs are open (CGE Bitbucket + NCBI AMRFinderPlus).
* No proprietary tools were used (CLC Genomics 9.5.2 in paper → replaced with
  open-source equivalents; SPAdes would be the analogue for MiSeq assembly if
  C10 were re-executed).
* Free-endpoint policy respected: uicgpu A100 for compute; Argo `argo:gpt-5.2`
  for LLM judge.
