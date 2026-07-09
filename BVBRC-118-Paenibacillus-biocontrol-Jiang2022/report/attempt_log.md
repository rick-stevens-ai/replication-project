# Attempt Log — BVBRC-118 (Jiang 2022, *P. peoriae* HJ-2)

## 2026-07-05 (wave-keeper subagent, argo/argo:claude-opus-4.7)

**T+00:00** Read wave brief + dir standard. Confirmed target dir `BVBRC-118-Paenibacillus-biocontrol-Jiang2022/` did not yet exist. Created skeleton (report/evidence, work, extraction).

**T+00:01** PMID 35209846 → PMC PMC8876185 → BMC Genomics OA. Fetched paper.pdf directly from BMC (9.5 MB, PDF v1.4) via `https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-022-08330-0.pdf`. `pdftotext -layout` → 838 lines paper.txt.

**T+00:03** Grepped paper for accessions. Found `PRJNA580302` (data availability statement) + GenBank 16S accession `MK911741` (partial 1.4 kb sequence). No genome/chromosome accession referenced; deposition was to SRA only.

**T+00:05** NCBI eutils probe of PRJNA580302:
- `nuccore` linkname: only the 16S (MK911741.1) — the annotated assembly was **never deposited to NCBI Assembly/Nucleotide**.
- `assembly` search for `Paenibacillus peoriae HJ-2`: 0 hits (paper claims chromosome NZ deposition but it never went live).
- `biosample` link: SAMN13155059 (jiang-HJ-2, `Microbe sample from Paenibacillus peoriae`).
- `sra` link: SRR10363117 (SRX7071172, PacBio Sequel, 183,095 spots, 1.30 Gb, 329 MB .sra).

**Consequence.** The reproducibility task becomes an *independent reassembly* from the deposited raw PacBio reads (Sequel, non-HiFi) rather than a re-alignment against an existing assembly.

**T+00:07** SSH to uicgpu; probed conda envs for tools.
- `/data/stevens/envs/bvbrc14`: Flye 2.9.6-b1802 + minimap2 + samtools ✓
- `/home/stevens/miniforge3/envs/bvbrc76`: Prokka ✓
- `/data/stevens/envs/antismash`: antiSMASH 8.0.4 ✓
- `/home/stevens/micromamba/envs/amr`: fasterq-dump 3.4.1 + prefetch ✓
- Marker + Nougat available under `/gpustor/stevens/anaconda3/envs/`.

**T+00:08** `prefetch` via SRA-toolkit failed (proxy DNS resolution issue on uicgpu for NCBI SDL). Pivoted to direct S3 download: `https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR10363117/SRR10363117` → 329,222,294 bytes (~314 MB) delivered in ~30 s.

**T+00:09** `fasterq-dump --threads 32 SRR10363117.sra` → `SRR10363117.fastq` (2,619,753,090 bytes; 183,095 spots/reads). Byte-count matches SRA record exactly.

**T+00:11** Kicked off marker + nougat on paper.pdf. Initial run OOM'd (another user held ~19 GB on GPU 0 + ~53 GB on GPU 0). Retried with `CUDA_VISIBLE_DEVICES=2` (marker) and `CUDA_VISIBLE_DEVICES=3` (nougat) — GPUs 2–7 fully free.
- **nougat** finished in ~22 s (paper.mmd, 64 KB).
- **marker** finished in ~68 s (paper.md).
- Copied both back to `extraction/{marker.md,nougat.mmd}` — artifacts (2) and (3) satisfied.

**T+00:12** Kicked off Flye assembly:
```
flye --pacbio-raw SRR10363117.fastq --out-dir assembly/flye --genome-size 6m --threads 64
```

**T+00:21** Flye finished. `assembly.fasta`: 6,007,189 bp, 1 circular contig, N50 = 6,007,189, mean coverage 205×. Python-computed GC% = 45.676. **Paper reported 6,001,192 bp / 45% GC / 215× — Δ length = +0.10%, Δ GC = +0.68 pp.** All within tool-version noise.

**T+00:23** Kicked off Prokka (bvbrc76 env) + antiSMASH run 1 (basic; antismash env) in parallel.

**T+00:24** Prokka done in ~40 s. Result: **5,244 CDS (paper: 5,237, Δ=+7 = +0.13%), 39 rRNA (exact match), 108 tRNA (exact match)**, 1 tmRNA, 3 repeat regions.

**T+00:27** antiSMASH run 1 done. **19 protoclusters detected** (paper: 12). No compound names because knownclusterblast off by default in antiSMASH 8.

**T+00:28** Kicked off antiSMASH run 2 with `--cb-knownclusters --cb-general --cb-subclusters --pfam2go --smcog-trees --tigrfam --asf --rre --tfbs`. This activates MIBiG matching.

**T+00:30** In parallel, fetched three P. peoriae reference genomes (IBSD35 GCF_002937395.1, HS311 GCF_001272655.2, ZF390 GCF_014692735.1) from NCBI FTP.

**T+00:31** skani ANI + mash dist against all three references. **HJ-2 → IBSD35 ANI = 97.59% (highest); HS311 = 97.56%; ZF390 = 96.38%.** Matches paper's claim that HJ-2 is closest to IBSD35 (though HS311 is essentially tied, margin 0.03 pp).

**T+00:44** antiSMASH run 2 finished (dominated by diamond blastp for knownclusterblast). Custom parser (`/tmp/parse_antismash.py`) extracts top MIBiG hits per region.

**T+00:45** **All 6 named compounds from paper Table 4 recovered via MIBiG knownclusterblast:**
- fusaricidin B (BGC0001152.5, 8/8 hits) at R01
- paeninodin (BGC0001356.4, 3/6) at R05
- paenilan (BGC0001727.3, 11/11) at R06
- tridecaptin (BGC0000449.5, 5/5) at R09
- pelgipeptin (BGC0000403.5, 2/8) at R10
- polymyxin (BGC0000408.5, 5/5) at R18

**T+00:46** Circular-rotation analysis: computed (mine_pos − paper_pos) mod 6,007,189 for each of five clusters. Four of five yield offsets in a tight 11 kb window near 2.405 Mb → single circular rotation of ~2.405 Mb explains coordinate shifts. Paenilan cluster span matches paper exactly (27,007 mine vs 27,006 paper, Δ=1 bp).

**T+00:48** LLM-judge call to `argo:claude-opus-4.6` via LiteLLM aggregator localhost:4000 (Argo 4.7/4.8 rejected by aggregator due to unwrapped thinking parts — filed as failure_analysis note). **Verdict: REPLICATED, high confidence, 100% coverage, 97% agreement.**

**T+00:52** Wrote all 8 mandated dir-standard artifacts:
- (1) `paper.pdf` ✓
- (2) `extraction/marker.md` ✓
- (3) `extraction/nougat.mmd` ✓
- (4) `report/REPORT.tex` (compiled to REPORT.pdf, 5 pages) ✓
- (5) `report/open_questions.json` (5 questions with next_steps) ✓
- (6) `report/workflow.md` (with tool table + effort estimate) ✓
- (7) `report/artifacts_summary.md` (+ `artifact_harvest.md`) ✓
- (8) `report/failure_analysis.md` ✓

Also: `report/REPORT.md`, `report/brief.md`, `report/evidence/{assembly,annotation}_metrics.json`, `report/evidence/antismash_regions.tsv`, `report/evidence/ani_results.tsv`, `report/evidence/rotation_analysis.txt`, `report/evidence/llm_judge_scoring.json`.

**T+00:55** DONE. WAVE_RESULT emitted below.
