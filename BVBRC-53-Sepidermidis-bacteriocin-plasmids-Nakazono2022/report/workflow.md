# Workflow — BVBRC-53 (Nakazono 2022, S. epidermidis bacteriocin plasmids)

Compact, reproducible pipeline used for this replication. All free endpoints
only; heavy compute on `uicgpu` per the standing heavy-compute rule.

## 0. Inputs

- Paper: Nakazono et al., *PLOS ONE* 17(1):e0258283 (2022).
  DOI 10.1371/journal.pone.0258283 · PMID 35041663 · PMC PMC8765612.
- Full text: Europe PMC OA XML (free; not the paid `pdf` tool).
- NCBI accessions: `OK031036` (pEpi56), `OK031035` (pNuk650),
  `KP702950` (pIVK45 reference).

## 1. Sequence retrieval (local)

- `eutils efetch` against NCBI `nuccore` for each accession, both FASTA and
  `gbwithparts` GenBank output. No auth required.
- Raw FASTA-body byte-length verified against the deposited lengths in the
  paper (64,386 / 26,160 / 21,840 bp) as a first sanity check.
- Files land under `work/seqs/`.

## 2. Genome statistics (local Python)

- Parse GenBank feature tables → length, GC%, CDS count.
- For each `CDS` feature carrying an `epi*` or `nuk*` `/gene` qualifier,
  extract `/gene`, `/product`, `/translation` and record the coordinates.
- Output: `report/evidence/genome_stats.txt` (per-plasmid summary + gene
  cluster inventory).

## 3. Peptide comparisons (local Python)

- **Epidermin (epiA):** translate the deposited epiA CDS from pEpi56;
  align to canonical Tü3298 prepeptide
  `MEAVKEKNDLFNLDVKVNAKESNDSGAEPRIASKFICTPGCAKTGSFNSYCC`.
  Score amino-acid mismatches. Result: 0 aa mismatches → 100% aa identity.
- **Nukacin (nukA):** translate nukA from pNuk650 and pIVK45; align
  position-by-position. Localize the single mismatch relative to
  leader vs mature C-terminal peptide.
  Result: exactly 1 leader mismatch (pos 4, L↔F); mature
  `KKKSGAVPTVSHDCHMNSWQFIFTCCG` identical.

## 4. Comparative alignment (local blastn)

- `makeblastdb -in pIVK45.fasta -dbtype nucl`
- `blastn -query pNuk650.fasta -db pIVK45 -perc_identity 80 -outfmt 6`
- Compute a per-base query-coverage vector across pNuk650 to identify
  unaligned (insertion) blocks.
- Result: 99.6% backbone identity; 70.3% of pNuk650 aligns to pIVK45;
  7,781 bp of pNuk650 is unaligned, dominated by a single 5,926 bp block
  at positions 17040–22965 plus a 1,821 bp block.
- Note: local MUMmer was broken (`TIGR::Foundation` @INC error + mbedtls
  version mismatch), so blastn was used as the comparative tool. See
  `attempt_log`.
- Output: `report/evidence/blastn_pNuk650_vs_pIVK45.tsv`.

## 5. BV-BRC specialty-gene screen (uicgpu, `bvbrc14` env)

- `ssh uicgpu` → activate `/data/stevens/envs/bvbrc14`.
- **abricate 1.4.0** against DBs (all dated 2026-Apr-03):
  plasmidfinder, card, resfinder, vfdb, megares, bacmet2.
- **AMRFinderPlus 4.2.7** on all three plasmids.
- Rationale: PlasmidFinder is the paper's declared BV-BRC workflow
  (“PlasmidFinder via Similar Genome Finder”).
- Outputs: `report/evidence/abricate_*.tsv`,
  `report/evidence/amrfinder_*.tsv`.

## 6. LLM-judge scoring

- Argo proxy `localhost:44497`, model `argo:gpt-5.2` (free per standing
  Argo rule).
- Structured JSON verdict over the full claim set C1–C8.
- Output: `report/evidence/llm_judge_prompt.txt`,
  `report/evidence/llm_judge_result.json`.

## 7. Report assembly

- Markdown master: `report/REPORT.md` (this replication's canonical text).
- Derived artifacts: `REPORT.tex`, `open_questions.json`, `workflow.md`,
  `artifacts_summary.md`, `failure_analysis.md` (this file family).
- Verdict: **PARTIAL REPLICATION (strong)** — every sequence-testable
  claim matched; wet-lab claim (C8) out of reach.

## Environment notes

- **Local host:** light Python + eutils + local blastn.
- **uicgpu:** conda env `bvbrc14` (`/data/stevens/envs/bvbrc14`) for
  abricate + AMRFinderPlus DBs.
- **Argo:** `localhost:44497` proxy, free endpoint, model `argo:gpt-5.2`
  for the LLM judge.
- **No paid endpoints used.** No hardcoded HPC login node.
