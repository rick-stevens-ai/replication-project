# Artifacts Summary — BVBRC-106

Every artifact produced, pulled, or referenced during this replication. Files with `report/`
prefix are local to this Dropbox dir; files with `~/replicate/bvbrc-106/` prefix live on uicgpu.

## 1. Paper / literature artifacts

| Artifact | Source | Local path | Size |
|---|---|---|---|
| PubMed abstract | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=30466389 | `work/pubmed_30466389.txt` | 4.0 KB (70 lines) |
| PMC full-text XML | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC6251167&rettype=xml | `work/pmc6251167.xml` | 140 KB (44 lines wrapped) |
| Paper PDF | https://bmcmicrobiol.biomedcentral.com/counter/pdf/10.1186/s12866-018-1325-2.pdf | `paper.pdf` | (see PDF-fetch note in `failure_analysis.md`) |
| Marker .md extraction | central Eagle SCOUT corpus (fallback: local `pdftotext`) | `extraction/marker.md` | see extraction/ |
| Nougat .mmd extraction | central Eagle Nougat manifest (fallback: pending-stub) | `extraction/nougat.mmd` | see extraction/ |

**Paper metadata**
- Title: *Multi-drug resistant Enterobacter bugandensis species isolated from the ISS and comparative genomic analyses with human pathogenic strains*
- Authors: Singh NK, Bezdan D, Checinska Sielaff A, Wheeler K, Mason CE, Venkateswaran K.
- Journal: *BMC Microbiology* 18:175, 2018.
- DOI: **10.1186/s12866-018-1325-2**
- PMID: **30466389**  ·  PMCID: **PMC6251167**
- License: CC-BY 4.0 (open access).

## 2. Genome assemblies (NCBI Datasets 18.32.0, downloaded 2026-07-05)

BioProject in paper (ISS strains): **PRJNA319366**. Bulk zip:
`~/replicate/bvbrc-106/genomes/bugandensis_assemblies.zip` (11.5 MB, 8 GCFs).

| Paper strain | Kind | Assembly acc. | Name | Contigs | bp | NCBI URL |
|---|---|---|---|---|---|---|
| IF2SW-P2  | ISS | GCF_002890725.1 | ASM289072v1 | 2  | 4 932 659 | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_002890725.1/ |
| IF2SW-B1  | ISS | GCF_002890755.1 | ASM289075v1 | 2  | 4 932 663 | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_002890755.1/ |
| IF2SW-B5  | ISS | GCF_003627555.1 | ASM362755v1 | 12 | 4 921 702 | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_003627555.1/ |
| IF2SW-P3  | ISS | GCF_002890765.1 | ASM289076v1 | 2  | 4 931 846 | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_002890765.1/ |
| IF3SW-P2  | ISS | GCF_002890715.1 | ASM289071v1 | 2  | 4 933 260 | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_002890715.1/ |
| EB-247T   | clinical | GCF_900324475.1 | EB-247 | 1  | 4 717 613 | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_900324475.1/ |
| 153_ECLO  | clinical | GCF_001054435.1 | ASM105443v1 | 51 | 4 701 120 | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_001054435.1/ |
| MBRL-1077 | clinical | GCF_001562175.1 | ASM156217v1 | 1  | 4 801 156 | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_001562175.1/ |

Per-strain FASTAs symlinked at `~/replicate/bvbrc-106/genomes/fastas/`.
Local snapshot of the resolution mapping: `report/evidence/resolved_accessions.json`
and `report/evidence/assembly_map.tsv`.

## 3. Analysis outputs

| Artifact | Path (this dir) | Path (uicgpu remote) | Format |
|---|---|---|---|
| All-vs-all ANI matrix (raw) | `report/evidence/ani/ani_matrix.tsv` | `~/replicate/bvbrc-106/work/ani_matrix.tsv` | 3-col TSV |
| 8×8 pretty ANI matrix | `report/evidence/ani_matrix_pretty.csv` | (derived) | CSV |
| Per-strain AMR TSVs (×8) | `report/evidence/amr/<strain>.amr.tsv` | `~/replicate/bvbrc-106/work/amr/*.tsv` | AMRFinderPlus 4.2.7 TSV |
| Resolved accessions | `report/evidence/resolved_accessions.json` | (mirror) | JSON |
| Assembly map | `report/evidence/assembly_map.tsv` | (mirror) | TSV |
| LLM judge output | `report/evidence/llm_judge_output.md` | (n/a) | Markdown |

## 4. Code / scripts

| Script | Path | Language | Purpose |
|---|---|---|---|
| Accession resolver | `work/resolve_accessions.py` | Python 3.11 | Entrez esearch/esummary → GCF |
| Assembly fetcher | `work/fetch_assemblies.sh` | bash | NCBI `datasets` wrapper |
| Legacy fetcher | `work/download_genomes.sh` | bash | (superseded) |
| LLM judge client | `work/llm_judge.py` | Python 3.11 | Argo proxy POST |

## 5. Report artifacts (this backfill)

| Artifact | Path | Status |
|---|---|---|
| Markdown report (original) | `report/REPORT.md` | present |
| LaTeX report (backfill) | `report/REPORT.tex` | present (+ `open_questions_body.tex`) |
| Open questions JSON | `report/open_questions.json` | present, 5 grounded Qs |
| Workflow | `report/workflow.md` | present (this pass) |
| Artifacts summary | `report/artifacts_summary.md` | present (this doc) |
| Failure analysis | `report/failure_analysis.md` | present (this pass) |
| Brief | `report/brief.md` | present |
| Attempt log | `report/attempt_log.md` | present |
| Original artifact harvest | `report/artifact_harvest.md` | present |

## 6. Traces / logs

- Original session narrative: `report/attempt_log.md` (chronological).
- LLM judge full response: `report/evidence/llm_judge_output.md`.
- Compute host: `uicgpu` (8× A100, 255 cores).
- LLM host: CherryRd → Argo proxy `127.0.0.1:44497` (free ANL endpoint).
- Conda envs used: `/data/stevens/envs/bvbrc28`, `/data/stevens/envs/bvbrc14`.

## 7. Verdict trace

Verdict: **REPLICATED** (preserved from original 2026-07-05 00:26 CDT run).
Judge model: `argo:claude-sonnet-4.6` (Opus 4.8 502'd on first attempt).
One-line: *ANI values and AMR gene profiles closely match paper's core claims within tool/database variation; no meaningful contradictions found.*
