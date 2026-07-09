# Replication Workflow — BVBRC-44 pCl107 (Rafei et al. 2022)

**Target:** Rafei R, Koong J, Osman M, Al Atrouni A, Hamze M, Hamidian M. *Analysis of pCl107, a large plasmid carried by an ST25 A. baumannii strain...* FEMS Microbes 3:xtac027 (2022). DOI 10.1093/femsmc/xtac027.
**Compute host:** `uicgpu` (free; 8×A100), `ssh uicgpu; source ~/env.sh` for proxy internet.
**Workdir:** `/data/stevens/scratch/bvbrc44-pCl107` (remote) → mirrored to `~/Dropbox/REPLICATE-PROJECT/BVBRC-44-Abaumannii-pCl107-plasmid-2022/` (local).
**Wall-clock:** ~5 minutes end-to-end after environment is set up. Human/analyst time: ~2–3 hours for report writing + LLM-judge scoring.

---

## Stage 0 — Environment (one-time)

| Tool | Version | Env | Install |
|---|---|---|---|
| NCBI Datasets CLI | 18.32.0 | `bvbrc28` | `conda install -c conda-forge ncbi-datasets-cli` |
| NCBI eutils (efetch) | current | system | `conda install -c bioconda entrez-direct` |
| AMRFinderPlus | 3.12.8 | `amr` | `conda install -c bioconda ncbi-amrfinderplus` |
| abricate + ResFinder DB | 2026-Apr | `amr` | `conda install -c bioconda abricate` |
| mlst (T. Seemann) | current | `bvbrc28` | `conda install -c bioconda mlst` |
| BLAST+ | current | `bvbrc28` | `conda install -c bioconda blast` |
| Biopython | 1.83+ | `bvbrc14` | `conda install -c conda-forge biopython` |
| Argo proxy (LLM judge) | localhost:44497 | host | pre-existing, free ANL Argo |

All free. No paid endpoints, no cluster allocations.

---

## Stage 1 — Sequence retrieval (~30s)

```bash
cd /data/stevens/scratch/bvbrc44-pCl107
mkdir -p genomes refs
# Target genome + plasmid
efetch -db nuccore -id CP098521.1 -format fasta > genomes/CP098521.1.fna       # chromosome
efetch -db nuccore -id CP098522.1 -format fasta > genomes/CP098522.1.fna       # pCl107
efetch -db nuccore -id CP098522.1 -format gbwithparts > genomes/CP098522.1.gbff  # pCl107 GenBank flatfile
# Reference plasmids (C4, C11)
for acc in KU744946.1 CP012005.1 KT779035.1 MF399199.1 MK531536.1; do
  efetch -db nuccore -id $acc -format fasta > refs/${acc}.fna
done
```

**Artifacts:** `genomes/CP098521.1.fna`, `genomes/CP098522.1.fna`, `genomes/CP098522.1.gbff`, `refs/*.fna` (5 files).

---

## Stage 2 — Genome statistics (C1) (~5s)

```python
from Bio import SeqIO
for f in ["genomes/CP098521.1.fna", "genomes/CP098522.1.fna"]:
    rec = next(SeqIO.parse(f, "fasta"))
    print(rec.id, len(rec.seq))
```

**Expected:** `CP098521.1 4056235` / `CP098522.1 198716`.
**Artifact:** stored in `evidence/evidence_summary.json`.

---

## Stage 3 — Host MLST (C2) (~10s)

```bash
mlst --scheme abaumannii   genomes/CP098521.1.fna > evidence/mlst_oxford.tsv
mlst --scheme abaumannii_2 genomes/CP098521.1.fna > evidence/mlst_pasteur.tsv
```

**Expected:** ST229 (Oxford) / ST25 (Pasteur).
Capsule KL14/OCL6 typing would require **Kaptive** (not run — see failure_analysis.md).

---

## Stage 4 — AMR genotyping (C3, C10) (~60s)

Three independent callers per sequence:

```bash
# AMRFinderPlus on plasmid + chromosome
amrfinder -n genomes/CP098522.1.fna --organism Acinetobacter_baumannii --plus \
  > evidence/amrfinder_pCl107.tsv
amrfinder -n genomes/CP098521.1.fna --organism Acinetobacter_baumannii --plus \
  > evidence/amrfinder_chromosome.tsv

# abricate vs ResFinder DB
abricate --db resfinder genomes/CP098522.1.fna > evidence/abricate_resfinder_pCl107.tsv
abricate --db plasmidfinder genomes/CP098522.1.fna > evidence/abricate_plasmidfinder.tsv

# RefSeq annotation-mined AMR list (from gbff /gene qualifiers)
python scripts/mine_gbff_amr.py genomes/CP098522.1.gbff > evidence/refseq_amr_pCl107.txt
```

**Expected on pCl107:** aac(6′)-Ian, aac(3)-IIe, aph(3′′)-Ib, aph(6)-Id, sul2, tet(B)/tetR(B) — all at 100/100.
**Expected on chromosome:** blaOXA-64, blaADC-26, gyrA_S81L, parC_S84L.

---

## Stage 5 — Module coordinate verification (C5–C9) (~30s)

Parse `/gene` + `/product` + coordinate qualifiers from the pCl107 gbff:

```python
from Bio import SeqIO
modules = {
    "BREX": ["brxA","brxB","brxC","brxL","pglX","pglZ"],
    "ptx":  ["ptxD","ptxA","ptxB","ptxC","ptxE","phnC","phnD","phnE"],
    "uric": ["uraH","uraD","puuE","uacT","hiuH","uao","hpxO"],
    "P450": ["cyp"],
    "MPF":  ["dotA","dotD","traY","traH","virB"],
}
rec = next(SeqIO.parse("genomes/CP098522.1.gbff", "genbank"))
hits = {m: [] for m in modules}
for feat in rec.features:
    if feat.type != "CDS": continue
    name = (feat.qualifiers.get("gene",[""])[0] + " " +
            feat.qualifiers.get("product",[""])[0]).lower()
    for m, keys in modules.items():
        if any(k.lower() in name for k in keys):
            hits[m].append((feat.location.start.position+1,
                            feat.location.end.position, name.strip()))
import json; print(json.dumps(hits, indent=2))
```

**Artifact:** `evidence/pCl107_modules.json`.
**Expected:** BREX start at 125,913 (brxL); ptxD ~148,876; uraH/uraD/puuE at 106,464–108,390; **urate oxidase absent** (empty hpxO/uao intact-uricase slot); MPF T4SS genes present.

---

## Stage 6 — Comparative genomics (C4, C11) (~2 min)

### C4: AbGRI1 "missing-link" region

```bash
# Extract pCl107 resistance region (bases 75000–90000)
python -c "
from Bio import SeqIO
rec = next(SeqIO.parse('genomes/CP098522.1.fna','fasta'))
print('>pCl107_75k_90k\n' + str(rec.seq[75000:90000]))
" > work/pCl107_resregion.fna

# Build BLAST DBs and query
for acc in KU744946.1 CP012005.1; do
  makeblastdb -in refs/${acc}.fna -dbtype nucl -out refs/${acc}
  blastn -query work/pCl107_resregion.fna -db refs/${acc} -perc_identity 90 \
         -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore' \
         >> evidence/resistance_region_blast.txt
done
```

**Expected:** ~12 kb 100%-identity blocks vs pA297-3 (KU744946); slightly fragmented but ~11 kb near-100% vs pAB3 (CP012005).

### C11: Whole-plasmid family relatedness

```bash
for acc in KU744946.1 CP012005.1 KT779035.1 MF399199.1 MK531536.1; do
  makeblastdb -in refs/${acc}.fna -dbtype nucl -out refs/${acc}
  aligned=$(blastn -query genomes/CP098522.1.fna -db refs/${acc} -perc_identity 95 \
             -outfmt '6 length' | awk '{s+=$1} END {print s}')
  pct=$(python -c "print(100*${aligned}/198716)")
  echo -e "${acc}\t${aligned}\t${pct}%" >> evidence/plasmid_relatedness.txt
done
sort -k3 -nr evidence/plasmid_relatedness.txt
```

**Expected ranking:** pMC1.1 (MK531536) > pD46-4 (MF399199) > pA297-3 (KU744946) > pD4 (KT779035).

---

## Stage 7 — LLM-judge scoring (~30s)

```bash
# Build judge_input.txt: 11 claims + measured results, plain-text
cat scripts/build_judge_input.sh
bash scripts/build_judge_input.sh > work/judge_input.txt

# Call free-Argo gpt-5.2
curl -s http://localhost:44497/v1/chat/completions \
     -H 'Authorization: Bearer stevens' \
     -H 'Content-Type: application/json' \
     -d @<(python scripts/wrap_judge_payload.py work/judge_input.txt) \
  > evidence/llm_judge_argo_gpt5.2.json
```

**Expected:** coverage 9/10, agreement 10/10, verdict REPLICATED.

---

## Stage 8 — Report + artifact packaging (~2h analyst time)

- `report/REPORT.md` — human-readable narrative
- `report/REPORT.tex` — LaTeX version for archival
- `report/artifact_harvest.md`, `report/attempt_log.md`, `report/brief.md` — process trail
- `report/evidence/*` — all machine-readable outputs (see Stage 2–7)
- `report/open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md` — back-fill artifacts

---

## Work Estimate

| Stage | Task | Time |
|---|---|---|
| 0 | Environment (one-time; already set up on uicgpu) | 15 min |
| 1 | Sequence retrieval | 30 s |
| 2 | Genome stats | 5 s |
| 3 | MLST | 10 s |
| 4 | AMR (3 callers × 2 sequences) | 60 s |
| 5 | Module coordinate parsing | 30 s |
| 6 | Comparative BLAST (C4 + C11) | 2 min |
| 7 | LLM-judge call | 30 s |
| — | **Compute total** | **~5 min** |
| 8 | Report writing + artifact packaging | 2–3 h |
| — | **Human total** | **~3 h** |

Reproducibility: full pipeline is a single shell script over `efetch → mlst → amrfinder → abricate → biopython-parse → blastn → curl`. Any bioinformatics-familiar analyst can rerun end-to-end on `uicgpu` (or any Linux box with the listed tools) in under 10 minutes. Cost: $0.
