# BVBRC-109 — Replication Workflow

**Paper**: Delgado-Suárez et al., *PLoS ONE* 16(5):e0243681 (2021), PMID 33951039
**Compute host**: `uicgpu` (Ubuntu, 255 cores, 2 TB RAM, CPU-only pipeline)
**Scratch**: `/data/stevens/bvbrc109/`
**Conda env**: `/data/stevens/envs/bvbrc14` (AMRFinderPlus 4.2.7, mlst 2.33.1, blast+, datasets 18.32.0, entrez-direct, python 3.11.15 + scipy)

---

## Stage 0 — Paper & metadata acquisition

1. `curl` PLOS Open-Access printable PDF → `work/paper.pdf`.
2. `pdftotext -layout paper.pdf paper.txt` (on CherryRd, poppler).
3. `grep -A2 -B2 -iE '(accession|prja|samn|srr|amrfinder|mlst|sgi)' paper.txt` to extract methods + accessions.
4. Fetch supplementary files S1–S7 (`.xlsx` + `.pdf`) from PLOS supporting-info URLs.
5. Semantic Scholar record via `x-api-key` header (Keychain lookup: `security find-generic-password -a rick-stevens-ai -s semantic-scholar-api-key -w`).

## Stage 1 — Metadata normalization

6. `openpyxl` → CSV conversion:
   - `S1_File.xlsx` → `work/study_isolates.csv` (77 study isolates + SRR/SAMN accessions + QC).
   - `S2_File.xlsx` → `work/public_isolates.csv` (2400 public NCBI Mexico Salmonella by source).
   - `S3_File.xlsx` → `work/typh_public.csv` (40 Mexican Typhimurium with pre-computed AMR).

## Stage 2 — Assembly retrieval

7. Enumerate BioProject assemblies:
   ```
   datasets summary genome accession PRJNA480281 \
     --assembly-source GenBank --as-json-lines \
     | dataformat tsv genome --fields accession,assminfo-biosample-accession \
     > work/all_prja_assemblies.tsv
   ```
8. Join `study_isolates.csv` (SAMN column) against `all_prja_assemblies.tsv` → 68 matches; 9 SAMNs never assembled → `work/missing_samns.txt`.
9. Bulk download:
   ```
   datasets download genome accession --inputfile work/study_gca.txt \
     --include genome --filename work/study_genomes.zip
   unzip -j work/study_genomes.zip 'ncbi_dataset/data/GCA_*/GCA_*.fna' \
     -d work/assemblies_flat/
   ```
   → 68 `.fna` files (~315 MB total on uicgpu).

## Stage 3 — AMR calling (AMRFinderPlus 4.2.7, DB 2026-03-24.1)

10. Per-genome AMRFinderPlus in parallel:
    ```
    ls work/assemblies_flat/*.fna | xargs -I {} -P 32 bash -c '
      base=$(basename {} .fna)
      amrfinder -n {} --organism Salmonella --plus --threads 2 \
        -o work/amr_out/${base}.tsv \
        --mutation_all work/amr_out/${base}.mut.tsv
    '
    ```
    Wall time ≈ 1 min for 68 genomes.
11. Concatenate:
    ```
    awk 'FNR==1 && NR!=1 {next} {print}' work/amr_out/*.tsv > work/all_amr_calls.tsv
    awk 'FNR==1 && NR!=1 {next} {print}' work/amr_out/*.mut.tsv > work/all_mut_calls.tsv
    ```

## Stage 4 — MLST (senterica_achtman_2 scheme, mlst 2.33.1)

12. Single batched call:
    ```
    mlst --scheme senterica_achtman_2 --nopath \
      work/assemblies_flat/*.fna > work/mlst_results.tsv
    ```

## Stage 5 — SGI-1 detection (blastn against AF261825.2)

13. Fetch reference:
    ```
    efetch -db nuccore -id AF261825.2 -format fasta > work/sgi1_ref.fna
    ```
14. Per Typhimurium+monophasic isolate (n=8 in re-analysed set):
    ```
    for f in $(grep -E 'Typhimurium|monophasic' work/study_isolates.csv | cut -f<gca_col>); do
      makeblastdb -in work/assemblies_flat/${f}.fna -dbtype nucl -out /tmp/db_${f}
      blastn -query work/sgi1_ref.fna -db /tmp/db_${f} \
        -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore' \
        -evalue 1e-30 -perc_identity 95 > work/sgi1_out/${f}.blast.tsv
      # sum aligned bp across HSPs
    done
    ```
15. Cross-check with AMRFinderPlus 5-gene marker set (`aadA2 blaCARB-2 floR sul1 tetG`) per isolate. Agreement threshold: both signals must call the same isolate positive. Agreement is 100% (6/6 concordant SGI-1+, 2/2 concordant SGI-1−).

## Stage 6 — Statistical analysis

16. Run `work/analyze_v2.py`:
    - Parse `all_amr_calls.tsv` → per-isolate AMR class set (β-lactam, aminoglycoside, tetracycline, sulfonamide, phenicol, fluoroquinolone, macrolide, fosfomycin, etc.).
    - MDR = ≥3 distinct classes.
    - Build 2×2 contingency tables:
      - LN vs GB → MDR/non-MDR.
      - Typhimurium (+monophasic) vs Other → MDR/non-MDR.
      - `ramR_M83T` positive vs negative → MDR/non-MDR.
    - `scipy.stats.chi2_contingency` (correction=False) and `scipy.stats.fisher_exact`.
    - Emit JSON summary → `report/evidence/replication_summary_v2.json`.

## Stage 7 — LLM-judge scoring

17. Assemble `work/judge_prompt.md`:
    - Paper abstract + our 9-claim table + all key numbers + honest divergence notes.
18. Submit to Argo `gpt-5.2` via `hcodex` / direct `curl` with strict-JSON rubric (0–100 scale, per-claim reasoning).
19. Persist verdict → `report/evidence/judge_verdict.json`.
20. Human review; write `report/REPORT.md` (long-form) and `report/REPORT.tex` (LaTeX + critique section).

## Stage 8 — Report finalization

21. Author `report/brief.md`, `attempt_log.md`, `artifact_harvest.md`.
22. Author `report/artifacts_summary.md`, `failure_analysis.md`, `workflow.md`, `open_questions.json`, `REPORT.tex` (this backfill).
23. Verify all files listed in REPORT.md §7 (Data availability) exist and are non-empty.

---

## Data-flow diagram (ASCII)

```
  PLOS OA PDF ──► pdftotext ──► paper.txt ──► grep methods
       │
       └► S1..S7 xlsx ──► openpyxl ──► study/public/typh CSVs
                                              │
  BioProject PRJNA480281 ──► datasets ──► 68 GCA .fna
                                              │
                                              ├─► amrfinder --organism Salmonella --plus
                                              │       │
                                              │       └─► all_amr_calls.tsv + all_mut_calls.tsv
                                              │
                                              ├─► mlst senterica_achtman_2
                                              │       │
                                              │       └─► mlst_results.tsv
                                              │
                                              └─► blastn AF261825.2 (Typh only)
                                                      │
                                                      └─► sgi1_out/*.blast.tsv
                                                              │
      study_isolates.csv + all_amr_calls.tsv + mlst_results.tsv + sgi1_out/
                                              │
                                              ▼
                                       analyze_v2.py
                                              │
                                              ▼
                          replication_summary_v2.json  ──► judge_prompt.md
                                                                │
                                                                ▼
                                                    Argo gpt-5.2 LLM-judge
                                                                │
                                                                ▼
                                                    judge_verdict.json (78/100 PARTIAL)
                                                                │
                                                                ▼
                                        REPORT.md + REPORT.tex + open_questions.json
```

## Reproducibility notes

- **Idempotency**: Every stage writes to a distinct output file; re-runs overwrite deterministically. `datasets download` skips already-present accessions.
- **Parallelism**: Only stage 3 (AMRFinderPlus) is parallelised (`xargs -P 32`); everything else is single-threaded and negligible.
- **Failure recovery**: If AMRFinderPlus fails on an assembly, re-run only that assembly and re-concatenate. Blast failures are per-isolate and self-contained.
- **Compute cost**: Whole pipeline runs in <10 min wall-clock on uicgpu (dominated by `datasets download` network I/O).
- **Missing 9 assemblies**: Documented in `work/missing_samns.txt`. To close, run `sra-toolkit prefetch + fasterq-dump + spades` on the 9 SRR accessions (~30 CPU-hours, not executed in this replication).
