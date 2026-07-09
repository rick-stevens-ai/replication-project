# Workflow — BVBRC-81 replication

Independent replication of the BV-BRC Genome Assembly (Nanopore) + downstream
annotation / comparative-genomics / functional-survey workflow applied by
Mollova et al. (2023) to *Lactiplantibacillus plantarum* PU3.

**Executed 2026-07-03.** Light steps on CherryRd, heavy compute on `uicgpu`
(8×A100), environment `/data/stevens/envs/bvbrc28`.

---

## Stage 0 — Paper + accession discovery

1. Retrieve paper full-text XML (MDPI PDF was Akamai-blocked from both hosts):
   ```
   curl -sL "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10609609/fullTextXML" -o paper.xml
   # -> 200,906 B
   ```
2. Parse XML for accessions and reported metrics.

## Stage 1 — Sequence retrieval + verification

3. Verify accessions CP120642–CP120651 via NCBI EUtils `esummary` (loop over
   all 10). All exist; all annotated to strain PU3; all sizes match paper
   Table 1.
4. Fetch FASTA:
   ```
   curl -sL ".../efetch.fcgi?db=nuccore&id=CP120642,...,CP120651&rettype=fasta&retmode=text" \
        -o genome/PU3_all.fasta
   # -> 3,423,478 B, 10 records
   ```
5. Fetch GenBank:
   ```
   curl -sL ".../efetch.fcgi?db=nuccore&id=CP120642,...,CP120651&rettype=gb&retmode=text" \
        -o genome/PU3_all.gb
   # -> 7,876,807 B
   ```

## Stage 2 — Independent assembly-metric recomputation

6. Python: per-record length + GC → `report/evidence/genome_metrics.tsv`.
7. Python: parse GenBank FEATURES tables per locus for
   `gene` / `CDS` / `tRNA` / `rRNA` / `ncRNA` / `tmRNA`
   → `report/evidence/genbank_feature_counts.txt`.

## Stage 3 — BV-BRC cross-check

8. Query BV-BRC:
   ```
   curl "https://www.bv-brc.org/api/genome/1590.5192"
   curl "https://www.bv-brc.org/api/sp_gene/?eq(genome_id,1590.5192)"
   ```

## Stage 4 — Independent annotation (uicgpu)

9. Prokka 1.14.6:
   ```
   prokka --outdir prokka_out --prefix PU3 --cpus 32 \
          --kingdom Bacteria --gcode 11 \
          --genus Lactiplantibacillus --species plantarum --strain PU3 \
          --locustag PU3 --force --fast PU3_all.fasta
   ```
10. Also collected the current NCBI PGAP re-annotation (2024-11-18) from the
    Assembly record for comparison.

## Stage 5 — Comparative genomics

11. Download reference genomes:
    ```
    wget https://ftp.ncbi.nlm.nih.gov/.../GCA_018588605.2_..._genomic.fna.gz   # M19
    wget https://ftp.ncbi.nlm.nih.gov/.../GCF_000203855.3_ASM20385v3_...       # WCFS1
    ```
12. Mash:
    ```
    mash sketch -o PU3.msh PU3_all.fasta
    mash dist -p 32 PU3.msh refs/M19.fna refs/WCFS1.fna
    ```
13. FastANI (identical tool to paper):
    ```
    fastANI -q PU3_all.fasta --rl refs_list.txt -o fastani_out.tsv -t 32
    ```

## Stage 6 — Functional surveys

14. Abricate 0.5 at defaults (`--mincov 80 --minid 80`) vs each DB:
    ```
    for db in card vfdb resfinder argannot; do
      abricate --db "$db" PU3_all.fasta > report/evidence/abricate_${db}.tsv
    done
    ```
15. Bacteriocin cluster window filter:
    ```
    awk -v s=1561101 -v e=1586810 \
        '$1=="CP120642.1" && $3=="CDS" && $4>=s && $5<=e' prokka_out/PU3.gff \
        > report/evidence/bacteriocin_window.gff
    ```

## Stage 7 — LLM-judge cross-verification

16. Submit the replication summary to three independent free Argo endpoints
    via `http://127.0.0.1:44497/v1/chat/completions`:
    - `argo:gpt-4o`
    - `argo:gpt-5`
    - `argo:gemini-2.5-pro`

    (Claude opus-4.7 / opus-4.8 both returned HTTP 502 that day — excluded.)
    Outputs in `report/evidence/judge_output_*.txt`.

## Stage 8 — Reporting

17. Aggregate into `report/REPORT.md` (canonical) + `report/REPORT.tex`
    (typeset). Verdict + honest limitations + genuine critique.

---

## Not attempted (out of scope for a sequence-only replication)

- BAGEL4 (web server, not installed locally) — bacteriocin core-peptide labels.
- CRISPRCasFinder (web server) — CRISPR array typing.
- dbCAN3 (web server) — CAZyme survey.
- Wet-lab phenotype panels (acid/bile/osmotic tolerance, BIOLOG PM,
  antibiotic disc diffusion) — require the actual PU3 strain and an
  anaerobic lab.
