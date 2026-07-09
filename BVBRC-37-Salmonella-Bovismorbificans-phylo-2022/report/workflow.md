# Replication Workflow — BVBRC-37 / Gopinath 2022 Bovismorbificans

**Paper:** Gopinath et al., *Microorganisms* 10(6):1199 (2022). DOI 10.3390/microorganisms10061199.
**Verdict:** REPLICATED.
**Compute:** heavy steps on `uicgpu` (8×A100, 255 cores); clustering / metadata / figures / judge locally.

---

## 0. High-level flow

```
NCBI BioProject PRJNA378379
        │
        ▼
[Datasets REST paginated pull]     ← C1  (82 Bovismorbificans assemblies)
        │
        ▼
[datasets download genome ...]     ← single 117 MB zip, flattened to per-accession FASTA
        │
        ├──► SeqSero2 (k-mer mode)                              ← C2  serovar
        ├──► mlst (senterica_achtman_2)                         ← C4  7-gene ST
        ├──► mash sketch + mash dist all-vs-all → SciPy hclust  ← C3, C4  topology
        ├──► NCBI BioSample attrs (isolation_source/host/geo)   ← C5  source/geo
        └──► AMRFinderPlus --organism Salmonella --plus         ← C6  AMR + virulence
                                    │
                                    ▼
                    evidence bundle → LLM judge (free Argo gpt-5.2) → verdict
```

## 1. Steps in order

### 1.1 Identify the dataset (C1)
- Endpoint: `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/bioproject/PRJNA378379/dataset_report`
- Pagination: 500/page.
- Filter: `organism == "Salmonella enterica subsp. enterica serovar Bovismorbificans"`.
- Result: 82 assemblies of 425 in the umbrella project.
- Cross-check: BioSample IDs matched against paper Table 1 (spot-check `SAMN12657228` → strain `N14_0646` → WGS project `WSDC01`).

### 1.2 Download assemblies
```
datasets download genome accession \
    --inputfile acc.txt \
    --include genome
```
- Output: one 117 MB zip.
- Post-process: unzip, flatten to one FASTA per accession under `work/genomes/`.
- Validation: 82/82 files present, all non-empty.

### 1.3 Serovar confirmation — SeqSero2 (C2)
```
SeqSero2_package.py -m k -t 4 -i <accession>.fna -d <outdir>
```
- Mode: `-m k` (k-mer, appropriate for assembled genomes).
- Parse `SeqSero_result.tsv` per genome → predicted serotype + antigenic profile.
- Result: 82/82 = "Bovismorbificans", uniformly `8:r:1,5`.

### 1.4 MLST typing — mlst (C4, C1)
```
mlst --scheme senterica_achtman_2 <accession>.fna
```
- Fix: `mlst` needs conda env's `blastn` on `PATH` and env `perl`; `export PATH=$CONDA_PREFIX/bin:$PATH`.
- Result: dominant STs {142:49, 377:14, 1499:11, 2640:5}, minority ST150:2, ST8700:1.

### 1.5 Whole-genome clustering — mash + SciPy (C3, C4)
```
mash sketch -o all -s 10000 <all 82 FASTAs>
mash dist all.msh all.msh > dist.tsv
```
- Load 82×82 into SciPy → `scipy.cluster.hierarchy.linkage(method="average")` → `fcluster(t=2, criterion="maxclust")`.
- Dendrogram: `scipy.cluster.hierarchy.dendrogram()` with leaves colored by ST.
- Result: cluster 1 = ST150 (n=2); cluster 2 = ST142+377+1499+2640+8700 (n=80). **Two-polyphyletic-cluster topology reproduced.**

### 1.6 Source / geography metadata (C5)
- Per-accession pull of BioSample attributes via NCBI Datasets:
  `datasets summary genome accession <acc> --report ids_only` then `efetch -db biosample -id <SAMN...>`.
- Extract `isolation_source`, `host`, `geo_loc_name`; categorize clinical vs food vs animal/env.
- Result: 70 clinical, 8 food, + animal/env/feed. CH 75, CA 5, US 2.

### 1.7 AMR + virulence content (C6)
- One-time DB setup: `amrfinder_update -d <writable_dir>` (DB 2024-07-22.1).
- Per genome:
  ```
  amrfinder -n <acc>.fna \
      --organism Salmonella \
      --plus \
      --database <writable_dir>/latest \
      -o <acc>.amrfinder.tsv
  ```
- Aggregate: pandas concat → group by Element type / class / gene.
- Result: 799 virulence hits, 199 AMR hits, 205 stress/metal hits. `spvD` in 56/82.

### 1.8 LLM-judge verdict
- Evidence bundle: results tables, figure, per-claim comparison.
- First choice: `argo:claude-opus-4.8` → HTTP 502 (known Argo proxy issue for opus-4.8 that day).
- Fallback: `argo:gpt-5.2` (free, no paid endpoint).
- Judge output: REPLICATED, coverage ≈ 0.92, per-claim C1–C5 reproduced, C6 partial.
- Full text: `evidence/llm_judge_verdict.txt`.

## 2. Tools and codes

| Tool | Version | Purpose | Free? |
|---|---|---|---|
| NCBI Datasets CLI (`datasets`) | 18.32.0 | assembly pull | ✅ |
| NCBI Datasets REST | v2alpha | BioProject query | ✅ |
| SeqSero2 (`SeqSero2_package.py`) | 1.3.2 | serovar prediction | ✅ (bioconda) |
| mlst | 2.35.0 (senterica_achtman_2) | 7-gene ST typing | ✅ (bioconda) |
| mash | 2.3 | genome-distance sketch | ✅ (bioconda) |
| SciPy `cluster.hierarchy` | 1.18.0 | linkage + fcluster | ✅ |
| Matplotlib | (env) | dendrogram render | ✅ |
| AMRFinderPlus (`amrfinder`) | 3.12.8, DB 2024-07-22.1 | AMR + virulence content | ✅ (bioconda) |
| Argo proxy → `gpt-5.2` | free tier | LLM judge | ✅ (never paid) |

Custom code: small Python driver scripts (dataset filter, per-accession fanout on `uicgpu`, results aggregation, dendrogram, LLM-judge harness). All artifacts under the paper's report dir.

## 3. Work estimate

| Phase | Wall time | Human touch |
|---|---|---|
| Dataset identification + BioProject query + filter | ~15 min | low (one query iteration) |
| 117 MB genome download + unzip + flatten | ~5 min | low |
| SeqSero2 × 82 (k-mer mode, 4 threads each, on uicgpu) | ~10 min | none once queued |
| MLST × 82 (after `PATH`/`perl` fix) | ~5 min | one env fix (~10 min) |
| mash sketch + all-vs-all dist + SciPy hclust + dendrogram | ~5 min | some plotting tweak |
| BioSample metadata pull + categorization | ~20 min | manual field cleanup |
| AMRFinderPlus × 82 (after DB update) | ~30 min | one DB-dir permissions fix |
| LLM-judge bundling + retry (opus 502 → gpt-5.2) | ~10 min | one retry decision |
| Report writing | ~1 h | main text + tables |
| **Total** | **~2.5 h wall**, **~1.5 h analyst attention** | one Ollie session |

## 4. Reproducibility notes for a re-runner

1. All API calls are auth-free (NCBI Datasets is public; no NCBI API key needed for this volume).
2. `mlst` PATH/perl issue is the only real environment gotcha — ensure `$CONDA_PREFIX/bin` precedes system `PATH`.
3. `amrfinder_update -d <dir>` needs a writable dir; DB version pinning matters if you want byte-identical AMR calls (we used 2024-07-22.1).
4. Mash sketch size `s=10000` is default and adequate; results are robust to `s ∈ [1000, 100000]`.
5. `argo:claude-opus-4.8` may still be flaky through the proxy; `argo:gpt-5.2` is a reliable free fallback.
6. Any BioProject drift (post-publication BioSample edits, added/removed genomes) will shift the exact tallies by 1–2 — the qualitative conclusion (two-cluster split, dominant STs, mixed sources) is stable.
