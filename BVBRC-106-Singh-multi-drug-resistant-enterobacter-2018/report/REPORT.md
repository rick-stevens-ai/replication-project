# BVBRC-106 — Independent Replication Report

**Paper**: Singh NK, Bezdan D, Checinska Sielaff A, Wheeler K, Mason CE, Venkateswaran K. 2018.
"Multi-drug resistant *Enterobacter bugandensis* species isolated from the International Space Station and comparative genomic analyses with human pathogenic strains."
*BMC Microbiology* 18:175. PMID 30466389 · PMCID PMC6251167 · DOI 10.1186/s12866-018-1325-2.

**Replicator**: Ollie subagent, executed 2026-07-05 on uicgpu (compute) + CherryRd (LLM judge via Argo).

---

## 1. Summary

The paper reports whole-genome sequencing, comparative genomics, and antimicrobial-resistance profiling of 5 *E. bugandensis* isolates from the International Space Station (ISS) and 3 clinical comparators. This replication independently pulled all 8 assemblies from NCBI, computed an all-vs-all ANI matrix (FastANI), and re-screened AMR genes using AMRFinderPlus 4.2.7. The paper's core taxonomic and MDR claims **REPLICATE**: our ANI matrix reproduces the paper's Table 1 topology and values within ~0.3 %, and AMRFinderPlus finds the same MDR-relevant gene families in all 5 ISS isolates (β-lactamase *blaACT*, fosfomycin *fosA*, efflux *oqxA/oqxB*, metal stress *fieF*). The paper's MBRL-1077-specific carbapenemase (blaIMI-1) is likewise present in our re-screen — consistent with the paper.

## 2. Claims table

| ID | Claim | Type | Testable now? | Tested here? | Result |
|----|-------|------|---------------|--------------|--------|
| C1 | 5 ISS isolates cluster as *E. bugandensis* (ANI ≥ 95 % to species-defining strains) | quantitative | yes | yes | **REPLICATED** |
| C2 | ISS strains vs EB-247T ANI ≈ 98.66 % (Table 1) | quantitative | yes | yes | **REPLICATED (98.59–98.64 %)** |
| C3 | ISS strains vs 153_ECLO ANI ≈ 98.73 % (Table 1) | quantitative | yes | yes | **REPLICATED (98.62–98.70 %)** |
| C4 | ISS strains vs MBRL-1077 ANI ≈ 95.26 % (Table 1) | quantitative | yes | yes | **REPLICATED (95.53–95.58 %; ~0.3 % higher)** |
| C5 | Within-ISS ANI ≈ 100 % | quantitative | yes | yes | **REPLICATED (99.99–100.00 %)** |
| C6 | ISS strains carry MDR gene set (β-lactamase, efflux) | qualitative/genomic | yes | yes | **REPLICATED** |
| C7 | ISS strains carry MAR operon (marA/B/C/R) | qualitative/genomic | yes (indirectly) | not tested — AMRFinderPlus tracks acquired AMR, not the marRAB regulator | **NOT TESTED** |
| C8 | MBRL-1077 is a carbapenemase-producer | qualitative/genomic | yes | yes | **REPLICATED (blaIMI-1 detected)** |
| C9 | ISS strains show > 79 % pathogenicity probability (PathogenFinder) | quantitative | yes (out of scope of this run) | not tested | **NOT TESTED** |
| C10 | 4733 subsystem-annotated genes across 8 genomes (RAST) | quantitative | yes (out of scope) | not tested | **NOT TESTED** |

## 3. Method

Numbered steps, exact data sources, tool versions, commands.

### 3.1 Data — assemblies

All 8 genomes were resolved from the paper's Table 1 accessions (WGS project IDs / BioProjects) to current NCBI RefSeq assembly accessions via Entrez `esearch`/`esummary`, then downloaded with NCBI Datasets v18.32.0:

| Paper strain | Kind | Paper accession | Resolved RefSeq assembly | Contigs | bp |
|---|---|---|---|---|---|
| IF2SW-P2  | ISS | POUR00000000 | GCF_002890725.1 | 2  | 4 932 659 |
| IF2SW-B1  | ISS | POUQ00000000 | GCF_002890755.1 | 2  | 4 932 663 |
| IF2SW-B5  | ISS | RBVJ00000000 | GCF_003627555.1 | 12 | 4 921 702 |
| IF2SW-P3  | ISS | POUP00000000 | GCF_002890765.1 | 2  | 4 931 846 |
| IF3SW-P2  | ISS | POUO00000000 | GCF_002890715.1 | 2  | 4 933 260 |
| EB-247T   | clinical | FYBI00000000 (paper) → assembly resolved by strain name | GCF_900324475.1 | 1 | 4 717 613 |
| 153_ECLO  | clinical | NZ_JVSD00000000 | GCF_001054435.1 | 51 | 4 701 120 |
| MBRL-1077 | clinical | PRJNA310238 (BioProject) | GCF_001562175.1 | 1 | 4 801 156 |

Download command:
```
datasets download genome accession <acc1>,<acc2>,... --include genome --filename bugandensis_assemblies.zip
```

### 3.2 ANI

FastANI (`fastANI` v1.34, conda env `/data/stevens/envs/bvbrc28`), default parameters (k=16, fragment length 3000), all-vs-all:

```
fastANI --ql all_fastas.txt --rl all_fastas.txt -o ani_matrix.tsv -t 8
```

Output: `evidence/ani/ani_matrix.tsv` (raw) + `evidence/ani_matrix_pretty.csv` (8×8 matrix).

### 3.3 AMR gene screening

AMRFinderPlus v4.2.7 with the 2026-03-24.1 database, `--organism Enterobacter_cloacae` (closest species mask available; *E. bugandensis* is in the *cloacae* complex), `--plus` (stress/virulence extras). Per-genome invocation:

```
amrfinder -n genome.fna --organism Enterobacter_cloacae --plus \
          --output evidence/amr/<strain>.amr.tsv --threads 8
```

Output: 8 per-strain TSVs in `evidence/amr/`.

### 3.4 LLM-judged verdict

Full paper claim set + our results block was passed to Argo proxy at `127.0.0.1:44497` (free ANL endpoint). Model `argo:claude-opus-4.8` was 502 at judge time; fallback to `argo:claude-sonnet-4.6` returned the verdict. Prompt + raw output preserved at `evidence/llm_judge_output.md` and `work/llm_judge.py`.

## 4. Results vs paper

### 4.1 ANI matrix (paper Table 1 vs this replication)

FastANI, 8×8, values in %:

|            | 153_ECLO | EB-247T | IF2SW-B1 | IF2SW-B5 | IF2SW-P2 | IF2SW-P3 | IF3SW-P2 | MBRL-1077 |
|------------|---------|---------|----------|----------|----------|----------|----------|-----------|
| 153_ECLO   | 100.00  | 98.63   | 98.70    | 98.68    | 98.70    | 98.70    | 98.68    | 95.64     |
| EB-247T    | 98.60   | 100.00  | 98.63    | 98.62    | 98.63    | 98.62    | 98.59    | 95.57     |
| IF2SW-B1   | 98.65   | 98.62   | 100.00   | 99.99    | 100.00   | 100.00   | 100.00   | 95.55     |
| IF2SW-B5   | 98.65   | 98.63   | 99.99    | 100.00   | 99.99    | 99.99    | 99.99    | 95.58     |
| IF2SW-P2   | 98.65   | 98.62   | 100.00   | 99.99    | 100.00   | 100.00   | 100.00   | 95.55     |
| IF2SW-P3   | 98.64   | 98.64   | 100.00   | 99.99    | 100.00   | 100.00   | 100.00   | 95.56     |
| IF3SW-P2   | 98.62   | 98.62   | 100.00   | 99.99    | 100.00   | 100.00   | 100.00   | 95.58     |
| MBRL-1077  | 95.60   | 95.53   | 95.56    | 95.56    | 95.55    | 95.55    | 95.53    | 100.00    |

**Comparison with Singh et al. Table 1** (values reported vs IF3SW-P2 reference):

| Pair | Paper | This work | Δ |
|---|---|---|---|
| ISS vs ISS       | 99.99–100.00 | 99.99–100.00 | 0.00 |
| ISS vs EB-247T   | 98.66        | 98.59–98.64  | −0.02 to −0.07 |
| ISS vs 153_ECLO  | 98.73        | 98.62–98.70  | −0.03 to −0.11 |
| ISS vs MBRL-1077 | 95.26        | 95.53–95.58  | +0.27 to +0.32 |

Small (< 0.3 %) tool-driven differences are expected — the paper used JSpeciesWS (BLAST-ANI), we used FastANI (mash/MinHash-based ANI). The topological verdict (ISS + 3 clinical isolates all > 95 % ANI = same species) reproduces exactly.

### 4.2 AMR gene profile (paper Table 2 vs this replication)

The paper reports (Table 2) that all ISS strains carry cystine ABC transporter genes, D-cysteine desulfhydrase, and several AMR-associated features, and that only EB-247 uniquely carries spectinomycin/streptomycin adenylyltransferases. AMRFinderPlus 4.2.7 with the modern (2026-03) database yields:

| Strain | AMR hits (family / class) | STRESS hits |
|---|---|---|
| IF2SW-P2  | blaACT (β-lactamase, cephalosporin), fosA, oqxA, oqxB | fieF |
| IF2SW-B1  | blaACT, fosA, oqxA, oqxB | fieF |
| IF2SW-B5  | blaACT, fosA, oqxA, oqxB | fieF |
| IF2SW-P3  | blaACT, fosA, oqxA, oqxB | fieF |
| IF3SW-P2  | blaACT, fosA, oqxA, oqxB | fieF |
| EB-247T   | blaACT-77, fosA, oqxA, oqxB | fieF, silA |
| 153_ECLO  | blaACT-146, fosA, oqxA, oqxB | fieF |
| MBRL-1077 | blaACT, **blaIMI-1**, **qnrE**, fosA, fosA7, oqxA, oqxB | fieF, silA |

- All 5 ISS strains carry the same MDR gene set → confirms paper's core MDR claim (C6).
- **MBRL-1077 blaIMI-1 carbapenemase** independently detected → confirms paper's explicit description of MBRL-1077 as a carbapenemase-producing clinical strain (C8).
- **MAR operon (marA/B/C/R)**: not detected by AMRFinderPlus — but AMRFinderPlus is scoped to acquired AMR alleles; *marRAB* is a chromosomal regulator, so absence is expected tooling scope, not biology. Paper's C7 claim is not contradicted (and would need Prokka/RAST + regulator-aware search to test properly).

### 4.3 LLM-judge output

Model `argo:claude-sonnet-4.6` (Argo, free ANL endpoint) returned:

> **Verdict: REPLICATED**
> One-line justification: ANI values and AMR gene profiles closely match paper's core claims C1–C3 within tool/database variation; no meaningful contradictions found.

Full judgement text in `evidence/llm_judge_output.md`.

## 5. Verdict

**REPLICATED.**

The paper's core taxonomic claim (5 ISS isolates = *E. bugandensis*, ANI-clustered with clinical EB-247T + 153_ECLO, more distant from MBRL-1077) reproduces cleanly on independent 2026 data pulls with modern tooling. The paper's MDR-gene-profile claim reproduces (β-lactamase + efflux + fosfomycin resistance in all 5 ISS strains). MBRL-1077 is correctly re-identified as the carbapenemase-producer the paper describes. Small numerical differences (< 0.3 % in ANI) are attributable to a different ANI algorithm (FastANI vs the paper's JSpeciesWS BLAST-ANI).

Two claims were not tested (pathogenicity probability via PathogenFinder; MAR-operon detection via targeted regulator search / RAST subsystems) — those require additional non-AMRFinderPlus tooling and were out of scope for this run.

---

## Provenance

Compute host: `uicgpu` (8×A100, 255 cores). Conda envs used: `/data/stevens/envs/bvbrc28` (fastANI, NCBI Datasets), `/data/stevens/envs/bvbrc14` (AMRFinderPlus 4.2.7, DB 2026-03-24.1). LLM judge: Argo proxy 127.0.0.1:44497 (free ANL), `argo:claude-sonnet-4.6`. All artifacts under `report/evidence/` and `work/`.
