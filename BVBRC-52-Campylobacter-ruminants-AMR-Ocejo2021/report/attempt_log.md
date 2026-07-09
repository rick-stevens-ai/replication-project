# Attempt Log — BVBRC-52 (Ocejo et al. 2021, Campylobacter ruminant AMR)

Chronological, 2026-07-02 (all times CDT).

## Candidate selection
- Read `WAVE_BRIEF_2026-07-01.md` + exemplar BVBRC-17 REPORT.md.
- Scanned ranks 33+ of `BVBRC_TOPUP85_2026-06-26.tsv`; deduped against existing BVBRC-01..51.
- Rank 33 = environmental metagenomes (hybrid assembly) — harder to map to isolate genomes; skipped.
- **Picked rank 34: Ocejo 2021** (PMID 33903652) — Campylobacter jejuni/coli ruminant AMR. Distinct from BVBRC-20 (C. jejuni Peru phylogeography). Clear CARD/AMRFinder + SPAdes workflow, 41+ cites, OA.
- Target dir created: `BVBRC-52-Campylobacter-ruminants-AMR-Ocejo2021/` (BVBRC-50/51 existed; 52 free).

## Paper + data retrieval
- Europe PMC core query confirmed OA CC-BY, PMC8076188, hasData=Y, hasSuppl=Y.
- Full-text JATS XML pulled → Data availability: **BioProject PRJNA689687**, runs SRR13362733–802, 70 genomes.
- No pre-made assemblies under the BioProject (raw SRA reads only) → assembly required.
- Supplementary MOESM1 PDF pulled via EPMC `supplementaryFiles`; `pdftotext -layout` extracted **Table S1** (metadata/ST/CC/phenotype/MICs) and **Table S2** (per-isolate raw-read + assembly stats). Parsed both to JSON. (Deliberately did NOT use the paid `pdf` tool.)
- ENA `filereport` run table mapped SRR→strain(C0xxx)→species→FASTQ FTP. Confirmed 40 jejuni / 30 coli.

## Panel selection (16/70)
- Built `panel.json` covering every AMR mechanism + controls: ERY-R coli (23S), GEN-R coli (aph), blaOXA-489 ST-827 coli, TET-R jejuni + mosaic, several gyrA CIP/NAL, susceptible control C0444, STR-only C0430, and C0268 (paper's CIP-R/no-gyrA exception).

## Compute setup (uicgpu)
- Tools spread across path-envs: `bvbrc14` (abricate+mlst+blast+spades+fastp), `bvbrc38` (spades+fastp+Biopython), `amr` (fasterq-dump+spades), `bvbrc28` (NCBI datasets). No seqtk/pointfinder.
- abricate dbs present: resfinder, ncbi, card, argannot, megares, plasmidfinder, vfdb (2026-Apr). mlst `campylobacter` scheme present.

## Pipeline debugging
- **FAIL 1:** `nohup ... &` over non-interactive ssh died immediately; pipeline.out empty.
- **FAIL 2:** `setsid` relaunch still died silently. Root cause found: `set -u` at top + `source ~/env.sh` → env.sh line 9 `mkdir -p "$HF_HOME"` references HF_HOME before it's exported → unbound-variable abort under nounset, killing the whole script before any output.
- **FIX:** removed `set -u`. Pipeline then ran cleanly. (Logged to failure-log rationale: never `set -u` a script that sources ~/env.sh.)
- Also switched read downloads to ENA HTTPS FTP via uicgpu proxy (direct/no-proxy times out; proxy = HTTP 200).
- Downsampling: no seqtk → used `fastp --reads_to_process 1700000` (~150× cap) since raw data is ~1125×.

## Execution
- Ran 16-isolate loop: ENA download (~45–110s each) → fastp QC+cap → SPAdes `--isolate` (~2–4 min each) → 200 bp contig filter → assembly stats → abricate (6 dbs) → mlst. Total ~70 min. All 16 assembled; "PIPELINE COMPLETE".
- SSH note: long-lived ssh connections during heavy SPAdes load stalled output; used fresh short connections with ConnectTimeout/ServerAliveInterval to poll.

## Point mutations
- Downloaded C. jejuni NCTC 11168 reference (GCF_000009085.1) via NCBI datasets; extracted WT gyrA (Thr86), rpsL (Lys43), 23S rRNA with Biopython.
- `pointmut2.py`: tblastn WT gyrA/rpsL → residue at pos 86/43. gyrA T86I detected in all CIP/NAL-R; WT in CIP-S AND in C0268 (paper's exception) ✓.
- 23S: first generic "A→G count" approach too noisy (natural NCTC11168 divergence). Rewrote `find23s.py` to compare ERY-R vs ERY-S isolates column-by-column → **position 2075 is the single ERY-R-specific A→G**, matching the paper's A2075G exactly. Verified across all 16 in `finalize.py`.

## Concordance + tet(O) investigation
- Built genotype↔phenotype table (112 calls): raw 91.1%.
- 3 TET false-negatives (C0140/C0541/C0680, multidrug ST-825/2097 coli) had NO tet gene in any assembly/db. Investigated at **raw-read level**: BLAST tet(O) ref vs first 100k reads → 148/155/161 hits in the TET-R isolates, **0** in TET-S control C0444. Conclusion: tet(O) present, assembly dropout at downsampled coverage. Corrected concordance = 93.8%.
- AMP FPs = blaOXA present but paper states AMP-R needs an extra promoter mutation → gene-presence over-calls (paper's own caveat).

## Judging
- LLM judge Argo gpt-5.2 (free): initial verdict SPOT-CHECK, but on the explicit SPOT-CHECK-vs-PARTIAL distinction (a real de-novo rerun WAS done), verdict = **PARTIAL**. opus-4.8 fallback hit a transient 502; gpt-5.2 confirmed PARTIAL.

## Outputs
- Report + brief + logs + artifact_harvest + evidence/ (JSON/CSV/tabs/judge transcripts) written under `report/`.
- Raw reads + assemblies retained on uicgpu `/data/stevens/bvbrc52-campy/`.
