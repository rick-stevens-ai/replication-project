# Artifacts Summary — BVBRC-78 (Pradal 2023, vB_EfaH_163)

Every artefact produced or fetched during this replication, grouped by category. Verdict: **PARTIAL**.

## 1. Input data (fetched from public repositories)

| Artefact | Source | Accession | Purpose | Notes |
|----------|--------|-----------|---------|-------|
| Paper metadata | NCBI eutils | PMID 36680219 | Bibliographic anchor | esummary JSON |
| Full-text XML | EuropePMC | PMC9860891 | Claim extraction | `work/paper_pmc.xml` |
| Phage genome | ENA | `CAJDKA010000002.1` | Primary subject of replication | 150,836 bp; contig 2 of the WGS record (contig 1 is a WGS-index artefact and is discarded) |
| Comparator: iF6 | NCBI nuccore | `NC_029009` | Herelleviridae reference | Paper's stated top hit |
| Comparator: EfV12-phi1 | NCBI nuccore | `MH880817` | Herelleviridae reference | Paper's stated top hit |
| Comparator: EFDG1 | NCBI nuccore | `NC_047796.1` | Herelleviridae reference; MCP donor | Paper's stated top hit; MCP `YP_009218324.2` |
| Comparator: EFP01 | NCBI nuccore | `MT909815.1` | Herelleviridae reference | Additional Schiekvirus |
| Comparator: MDA2 | NCBI nuccore | `MW633168.1` | Herelleviridae outgroup (Kochikohdavirus) | Paper places on separate branch |
| Outgroup 1 | NCBI nuccore | `NC_031260` | Siphoviridae control | Used to sanity-check lysogeny screen |
| Outgroup 2 | NCBI nuccore | `MK360024` | Siphoviridae control | Second outgroup for BLASTn null distribution |

**NOT fetched (blocked by authors):**
- Raw sequencing reads for vB_EfaH_163 — required for PhageTerm (C-9). Not deposited.
- Host isolate VR-13 genome — required to independently confirm van cluster (C-13). Not deposited.

## 2. Reference sets we built

| Artefact | Contents | Purpose |
|----------|----------|---------|
| Lysogeny marker DB | 7 proteins: λ int NP_040604.1, φ80 int NP_050146.1, P22 int NP_059583.1, P22 cI NP_059609.1, λ cI NP_040628.1, Sa3int int YP_009641394.1, L54a int YP_240215.1 | BLASTp target for C-6 lytic-lifestyle screen |
| Abricate DBs | card, ncbi, resfinder, argannot, megares, vfdb, victors (7 DBs) | C-5 AMR + virulence screen |
| MCP set | 6 major-capsid-protein sequences extracted from 6 Herelleviridae proteomes by best-hit BLASTp against EFDG1 MCP | UPGMA input for C-7 phylogeny |

## 3. Analysis intermediates

| Artefact | Producer | Size | Used for |
|----------|----------|------|----------|
| `work/proteins.faa` | Prodigal (meta) on phage genome | 183 records | ORF count C-3, lysogeny query C-6, MCP query base |
| `work/genes.gff` | Prodigal | GFF3 | ORF coordinates |
| `work/aragorn_output.txt` | ARAGORN default tRNA mode | 21 tRNAs | C-4 |
| `work/abricate/*.tab` | Abricate x7 DBs | 0 hits each | C-5 |
| `work/blastp_lysogeny.tsv` | BLASTp phage proteome vs 7-marker set | 0 hits at E<1e-5 | C-6 |
| `work/blastn_wgs.tsv` | Pairwise blastn phage vs each comparator | HSP tables | C-7, C-8 |
| `work/mcp_pid_matrix.tsv` | BioPython PairwiseAligner all-vs-all on 6 MCPs | 6×6 identity matrix | C-7 topology |
| `work/mcp_upgma.nwk` | Bio.Phylo UPGMA on 1-pid | Newick tree | C-7 topology (recovers paper Fig 4) |

## 4. Evidence files (report/evidence/)

| File | Contents |
|------|----------|
| `abricate_summary.tsv` | Consolidated 7-DB result: 0 AMR, 0 virulence |
| `blastn_summary.tsv` | Weighted-avg %identity per comparator: iF6 96.5, EFP01 95.7, EfV12-phi1 94.1, EFDG1 93.8, MDA2 ~85 |
| `mcp_tree.nwk` + `mcp_tree.png` | UPGMA tree matching paper Fig 4 topology |
| `aragorn.txt` | 21 tRNAs listed with anticodons and coordinates |
| `prodigal_summary.txt` | 183 ORFs; length distribution |
| `judge_input.md` | The claim-by-claim evidence packet sent to the LLM judges |
| `judge_verdicts.jsonl` | 4 responsive judges' raw responses + parsed verdict |

## 5. Reports (report/)

| File | Format | Role |
|------|--------|------|
| `REPORT.md` | Markdown | Canonical replication report |
| `REPORT.tex` | LaTeX | Detailed report with Genuine Critique section (this batch) |
| `brief.md` | Markdown | One-paragraph summary for wave-level aggregation |
| `attempt_log.md` | Markdown | Chronological execution log |
| `artifact_harvest.md` | Markdown | Enumeration of every public artefact fetched |
| `open_questions.json` | JSON | 5 forward-looking research questions (this batch) |
| `workflow.md` | Markdown | End-to-end pipeline documentation (this batch) |
| `artifacts_summary.md` | Markdown | This file (this batch) |
| `failure_analysis.md` | Markdown | Honest catalogue of failures, blocked claims, tool workarounds (this batch) |

## 6. Verdict artefacts

- Per-judge verdicts (Argo :44497 panel): 3× PARTIAL, 1× REPLICATED (of 4 responsive judges).
- Majority: **PARTIAL**.
- WAVE_RESULT line emitted in `REPORT.md` §9.

## 7. What is NOT in the artifact set (and why)

- **PhageTerm output** — requires raw reads, not deposited by authors (C-9 blocked).
- **VR-13 host genome + van cluster BLAST** — host isolate not deposited (C-13 blocked).
- **Wet-lab replicates** (host range, one-step growth, Galleria) — out of computational-replication scope (C-10, C-11, C-12).
- **MAFFT MSA** — Homebrew build segfaulted; fell back to BioPython PairwiseAligner + UPGMA. Topology reproduces paper Fig 4; branch lengths should not be over-interpreted.
- **VIRIDIC / pyani ANIm** — not run; would let us convert C-8's "directional agreement" into a proper numeric agreement metric.
- **Argo opus 4.7 and 4.8 judge responses** — both endpoints returned HTTP 502 during the run and were replaced with claude-sonnet-4.6 and gpt-5.4.
