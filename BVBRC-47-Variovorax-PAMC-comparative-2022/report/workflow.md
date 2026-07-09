# Workflow: Replication of Shrestha et al. 2022 (BVBRC-47)

**Paper:** Shrestha P, et al. *International Journal of Microbiology* 2022, Art. 5067074. DOI 10.1155/2022/5067074. PMC10232917.
**Set:** BVBRC-47 (TOPUP85 rank-27).
**Host:** uicgpu01 (conda env `bvbrc28`; NCBI HTTP proxy via `source ~/env.sh`).
**Endpoints:** all free (Europe PMC + NCBI Datasets + local tools + Argo `gpt-5.2`).
**Verdict:** REPLICATED. Coverage 8/10, Agreement 9/10.

---

## Stage 0 — Deduplication and scoping

- **Risk:** a sibling directory `BVBRC-04-Variovorax-trehalose-Shrestha2022` (same lab, same year, similar topic) exists for a *different* paper (Shrestha 2022 *BMC Genomic Data* 23:4, DOI 10.1186/s12863-021-01020-y, single-strain PAMC28711 trehalose methods).
- **Action:** confirmed BVBRC-47 = Shrestha 2022 *Int J Microbiology* three-strain comparative-genomics paper (different journal, DOI, PMC, scope). Recorded dedup note at top of `REPORT.md`.

## Stage 1 — Paper acquisition (free)

1. Attempted Hindawi PDF endpoint → Cloudflare HTML block. Abandoned.
2. Fetched Europe PMC full-text XML:
   - URL: `https://europepmc.org/article/PMC/PMC10232917/fullTextXML`
   - Size: 162 KB, SHA-256 `63620a15…d3c0`.
3. Tag-stripped XML to extract: abstract, Materials & Methods, and all 5 tables. This is the canonical text source for the replication (Hindawi PDF is not machine-accessible).

## Stage 2 — Accession resolution

Mapped nucleotide accessions in the paper to current RefSeq assemblies via NCBI `esearch` → `esummary`:

| Strain | Paper accession | RefSeq assembly | Assembly name |
|---|---|---|---|
| PAMC28711 | CP014517 | GCF_001577265.1 | ASM157726v1 |
| PAMC26660 | CP060295 / NZ_CP060295 | GCF_014302995.1 | ASM1430299v1 |
| PAMC28562 | CP060296 / NZ_CP060296 | GCF_014303735.1 | ASM1430373v1 |
| *V. paradoxus* NBRC 15149ᵀ | (comparator) | GCF_050627025.1 | — |

## Stage 3 — Data download

```bash
# on uicgpu, conda env bvbrc28
source ~/env.sh   # NCBI HTTP proxy
for acc in GCF_001577265.1 GCF_014302995.1 GCF_014303735.1 GCF_050627025.1 ; do
  datasets download genome accession "$acc" --include genome,protein,gff3 \
    --filename "${acc}.zip"
  unzip -q "${acc}.zip" -d "${acc}/"
done
```

All 4 packages validated (`.fna` + `.faa` + `genomic.gff` present, non-empty).

## Stage 4 — Genome statistics (`genome_stats.py`)

- **Input:** per-strain `*_genomic.fna`, `genomic.gff`, `protein.faa`.
- **Compute:**
  - sequence length + GC% from `.fna`;
  - CDS / gene / tRNA counts from GFF feature-type tallies;
  - protein count from `.faa` record count.
- **Compare** against paper Table 1 (size, GC%, tRNA, gene/CDS).
- **Result:** sizes, GC%, tRNA counts match essentially exactly across all three PAMC strains. Gene/CDS within <2% (annotation-version drift).

## Stage 5 — Trehalose pathway scan (`treh2.py`) — headline C5

- **Input:** RefSeq `genomic.gff` `product=` fields (URL-decoded) per CDS.
- **Regex classifier:** OtsA, OtsB, TreY, TreZ, TreS, trehalase.
- **Pathway rollup:** OtsA/OtsB complete iff both otsA + otsB present; TreY/TreZ complete iff both treY + treZ; TreS complete iff treS present.
- **Result:**
  - PAMC28711 = 3 complete pathways ✅
  - PAMC28562 = 3 complete pathways ✅
  - PAMC26660 = 1 (OtsA/OtsB only) ✅
- Direct reproduction of the paper's headline biological claim. Evidence in `report/evidence/trehalose_scan.json`.

## Stage 6 — ANI (fastANI) — C6

```bash
fastANI --ql query_list.txt --rl ref_list.txt -o fastani.out
```

query/ref = the 4 assemblies. Cross-compared each PAMC strain vs *V. paradoxus* NBRC 15149ᵀ.

**Note:** fastANI ≠ paper's OAT/ANIb (BLAST) and ANIm (MUMmer). Absolute values differ 1–3%; the <95% species-boundary conclusion is preserved.

## Stage 7 — Proteome comparison (BV-BRC analogue) — supplementary

```bash
makeblastdb -in <subject>.faa -dbtype prot -out <subj>_db
blastp -query <query>.faa -db <subj>_db \
       -outfmt '6 qseqid sseqid pident qcovs evalue' \
       -evalue 1e-5 -max_target_seqs 1 -num_threads 8 > pw.tsv
# best-hit filter: pident ≥ 30 AND qcovs ≥ 70 AND evalue ≤ 1e-5
```

Reported shared-ortholog % across the 3 PAMC pairs → 79–81%. Consistent with sub-species relatedness. Evidence in `report/evidence/proteome_comparison.json`.

## Stage 8 — CAZyme content (Table 3) — C7

- **Status:** **PARTIAL.** `run_dbcan` not installed in the env; per-family CAZyme totals (paper Table 3) not recomputed at dbCAN2 resolution.
- Product-name trehalase scan (from Stage 5) confirms the coarse degradation-side pattern but cannot subtype GH37 vs GH15.
- **Closable step:** add `run_dbcan` v4+ + dbCAN's HMMER/DIAMOND/eCAMI DBs; re-run on the three PAMC proteomes.

## Stage 9 — Wet-lab AZCL (Table 5) — C8

Not reproducible in silico. Out of scope by design.

## Stage 10 — Independent LLM-judge (free)

- Model: Argo `argo:gpt-5.2` (free per standing rule).
- Input: compact evidence bundle (paper claim table + this replication's measured numbers).
- Output: verdict = **REPLICATED**, Coverage 8/10, Agreement 9/10.
- No regex scoring — full-text judgment.

## Stage 11 — Report assembly

- `REPORT.md` — human-readable markdown, all tables and verdict.
- `REPORT.tex` — detailed LaTeX version with an explicit Genuine Critique section.
- `open_questions.json` — machine-readable list of 5 open questions with concrete next steps.
- `artifacts_summary.md` — inventory of intermediate files (this workflow's evidence).
- `failure_analysis.md` — what did *not* work / partial gaps and how to close them.

## Rerun / reproduce

```bash
ssh uicgpu01
conda activate bvbrc28
source ~/env.sh
cd ~/Dropbox/REPLICATE-PROJECT/BVBRC-47-Variovorax-PAMC-comparative-2022/work
# 1. re-download assemblies (idempotent)
bash scripts/00_download.sh
# 2. stats
python scripts/genome_stats.py > report/evidence/genome_stats.json
# 3. trehalose (headline)
python scripts/treh2.py       > report/evidence/trehalose_scan.json
# 4. fastANI
bash scripts/40_fastani.sh    > report/evidence/fastani.tsv
# 5. proteome comparison
bash scripts/50_proteome_pw.sh > report/evidence/proteome_comparison.json
# 6. LLM-judge
python scripts/90_llm_judge.py  # uses Argo gpt-5.2 free endpoint
```

Expected time end-to-end on uicgpu: ~15–20 minutes (dominated by BLAST all-vs-all).
