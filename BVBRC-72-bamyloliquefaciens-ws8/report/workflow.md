# Workflow — BVBRC-72 *B. amyloliquefaciens* WS-8 Replication

End-to-end recipe used to produce the REPORT.md verdict. All steps executable on CherryRd (macOS) + uicgpu (Ubuntu, 8×A100). All endpoints FREE.

## Stage 0 — Paper retrieval

| Step | Endpoint | Command / call | Output |
|---|---|---|---|
| 0.1 | Europe PMC | GET `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9728402/fullTextXML` | `paper/PMC9728402_fulltext.xml` (107 KB) |
| 0.2 | NCBI PubMed | `efetch -db pubmed -id 31601062 -format abstract` | `paper/pubmed_31601062.txt` |
| 0.3 | Semantic Scholar v1 | `GET /graph/v1/paper/DOI:10.4014/jmb.1906.06055` (header `x-api-key: $S2_API_KEY`) | `paper/s2_metadata.json` (open-access flag + canonical PDF URL) |

## Stage 1 — Accession identification

- NCBI Assembly search: `Bacillus amyloliquefaciens WS-8` → single hit **GCF_001922005.1** (ASM192200v1).
- Cross-check: paper's stated genome length `3,929,787 bp` matches the assembly length exactly. High confidence this is the deposited sequence.
- Bookkeeping accessions:
  - BioProject: PRJNA354791
  - BioSample: SAMN06051297
  - GenBank: CP018200.1 (RefSeq NZ_CP018200.1)

## Stage 2 — Genome download (uicgpu)

```bash
# on uicgpu, working dir ~/replication/bvbrc-72/genomes/
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP018200.1&rettype=gbwithparts&retmode=text" \
  -o CP018200.gb        # 9.09 MB
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP018200.1&rettype=fasta&retmode=text" \
  -o CP018200.fasta     # 3.99 MB
```

## Stage 3 — Independent genome-statistics compute

- Script: `work/genome_stats.py` (Biopython 1.83).
- Reads `CP018200.gb`, computes GC directly from sequence composition (NOT PGAP-reported), tallies feature-type counts (gene, CDS, pseudo, tRNA, rRNA, ncRNA, tmRNA, regulatory).
- Outputs JSON to `report/evidence/genome_stats.json`.

Expected values (matched paper): 3,929,787 bp; 46.499 % GC; 3895 gene / 3777 CDS / 107 pseudo / 86 tRNA / 27 rRNA (9× each of 5S/16S/23S) / 4 ncRNA + 1 tmRNA / 25 regulatory.

## Stage 4 — Independent BGC marker-gene scan

- `work/bgc_gene_scan.py`: scans CDS `product/gene/note` qualifiers for canonical BGC marker gene names (dfnJ, mlnH, mlnI, bacA, srfA*, ppsA-D, baeJ, dhbA-F, LanC/LanM, etc.).
- `work/nrps_pks_scan.py`: scans for NRPS/PKS domain descriptors (A-domain, C-domain, PCP, KS, AT, KR, DH, ER, TE).
- Proximity clustering: ≥2 strong biosynthetic CDS within 20 kb → BGC-like region.
- Result: 9 BGC-like regions found (fewer than antiSMASH's 13 because PGAP annotation is product-string-heavy / gene-name-sparse; consistent with antiSMASH v8 topology).

## Stage 5 — antiSMASH v7.1.0 (web)

```bash
# submit via public antiSMASH web API
curl -F "seq=@genomes/CP018200.gb" \
     -F "genefinding=none" \
     -F "minimal=true" \
     https://antismash.secondarymetabolites.org/api/v1.0/submit
# poll for jobid completion; download regions.js + index.html
```

- Runtime ≈ 2 min.
- Result: **12 regions** (transAT-PKS ×4, T3PKS, terpene ×2, NRPS, NRPS+betalactone+transAT-PKS hybrid, PKS-like, `other` with bacilysin rule, RiPP-like+NRP-metallophore+NRPS, `lanthipeptide-class-ii`).

## Stage 6 — antiSMASH v8.0.4 (local, uicgpu)

Discovered pre-installed conda env `/data/stevens/envs/antismash` with antiSMASH v8.0.4 + Pfam-A 35.0 + full clusterblast/knownclusterblast/MIBiG/subclusterblast databases.

```bash
conda activate /data/stevens/envs/antismash
antismash --taxon bacteria \
  --output-dir antismash8_out \
  --cb-knownclusters --cb-subclusters --cb-general \
  --cc-mibig \
  --clusterhmmer \
  --genefinding-tool none \
  --cpus 8 \
  genomes/CP018200.gb
```

- Runtime ≈ 6 min.
- Result: **13 regions**; per-region MIBiG matches saved to `knownclusterblast/CP018200.1_c{1..13}.txt`.
- v8 finds one additional region vs v7 (`terpene-precursor` at 56–77 kb).

## Stage 7 — LLM-judge verdict

- Script: `work/judge.py`.
- Endpoint: Argo proxy at `localhost:44497` (tunneled from studio-ts).
- Model: `argo:gpt-5.2` (FREE via Argo).
- Params: `temperature=0.1`, `max_tokens=2500`.
- Input: 21-claim table + curated paper-fact summary.
- Output: per-claim `agrees_bool` + agreement pct + one-line reasoning; aggregate `coverage`, `agreement`, `verdict`, `concerns`, `justification` as JSON.
- Result stored at `report/evidence/llm_judge_result.json`.
- Verdict: **PARTIAL**, coverage 90 %, agreement 83.6 %.

## Stage 8 — Report assembly

- `report/REPORT.md` — canonical human-readable narrative (this replication's master output).
- `report/REPORT.tex` — LaTeX rendition with dedicated GENUINE CRITIQUE section.
- `report/open_questions.json` — 5 grounded scientific open questions.
- `report/artifacts_summary.md` — file inventory.
- `report/failure_analysis.md` — what failed / what couldn't be tested / why.
- `report/artifact_harvest.md` — accessions.
- `report/attempt_log.md` — chronological execution log.

## Compute topology summary

| Host | Role | Tools used |
|---|---|---|
| CherryRd | orchestration, LLM judge, paper retrieval, report assembly | curl (NCBI, EPMC, S2), Python 3.12, Argo proxy tunnel |
| uicgpu (8×A100) | genome parsing, antiSMASH v8 local run | Biopython 1.83, conda env `/data/stevens/envs/antismash`, antiSMASH v8.0.4 |
| studio-ts | Argo proxy host (upstream tunnel target for CherryRd LLM calls) | — |

## Endpoint & credential summary (all FREE)

- NCBI E-utils: no auth
- Europe PMC: no auth
- Semantic Scholar Graph v1: header `x-api-key: $S2_API_KEY` (Keychain: service `semantic-scholar-api-key`, account `rick-stevens-ai`)
- antiSMASH web api v1.0: no auth
- antiSMASH v8.0.4 local: no external calls (bundled MIBiG/Pfam databases)
- Argo proxy (localhost:44497 on CherryRd, tunneled from studio-ts): `Authorization: Bearer stevens`

No paid LLM APIs, no OpenAI / Anthropic / OpenRouter direct calls.

## Reproducibility notes

- To re-run end-to-end from scratch, minimum wall-clock is ~15 minutes on uicgpu (genome download ~30 s, genome_stats ~5 s, antiSMASH v8 ~6 min, LLM judge ~30 s), plus network round-trips for NCBI/EPMC.
- The single non-idempotent step is antiSMASH v7 (web) — antiSMASH server assigns a fresh jobid each submission. Local antiSMASH v8 is fully deterministic given the same input GBK and database versions.
- All raw command lines and outputs are preserved under `work/` and `report/evidence/`.
