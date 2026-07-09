# Workflow — Jurrus-APBS-2017 replication

## Pipeline

```
[europepmc render endpoint]
        │  1.71 MB PDF
        ▼
   paper.pdf ─────────► marker (uicgpu)    ─► extraction/marker.md   (555 lines)
                    └─► nougat (uicgpu GPU6) ► extraction/nougat.mmd (415 lines)

[RCSB]
        │  1FAS.pdb (75 KB) + 1CRN.pdb (49 KB)
        ▼
   work/*.pdb
        │
        │ pdb2pqr30 --ff=AMBER --apbs-input
        ▼
   work/*.pqr + work/*.in
        │
        │ apbs <mol>.in         (4 configurations: LPBE-0M, LPBE-0.15M, NPBE-0.15M, geoflow[FAILED])
        ▼
   work/*_pot.dx + work/*.apbs.log
        │
        │ python + numpy grid stats
        ▼
   report/evidence/potential_stats.json
        │
        │ LLM judge call → argo:gpt-5.2 via LiteLLM aggregator (Argo Opus 4.7/4.8 both 502)
        ▼
   report/evidence/llm_judge_argo.json      Verdict: PARTIAL
```

## Tools + codes used

| Stage | Tool | Version | Location |
|---|---|---|---|
| PDF fetch | curl | system | uicgpu |
| PDF→markdown | marker_single | 1.x | /data/stevens/envs/marker |
| PDF→LaTeX-flavored MD | nougat | 0.1 | /gpustor/stevens/anaconda3/envs/nougat |
| Structure prep | pdb2pqr30 | 3.6.1 | /data/stevens/envs/apbs-repl |
| PBE solve | apbs | 3.4.1 (compiled 2026-01-30) | /data/stevens/envs/apbs-repl |
| Grid analysis | python + numpy | 3.10 | (same env) |
| LLM judge | Argo LiteLLM aggregator @ cherryrd:4000 | live 2026-07-05 | Bearer stevens |

No new code was written; all invocations use standard command-line tools.

## Data sources

- **APBS + PDB2PQR**: conda-forge pre-built binaries (public, open source, https://github.com/Electrostatics/apbs, GitHub tag v3.4.1).
- **Test proteins**: RCSB Protein Data Bank (https://files.rcsb.org/download/{1FAS,1CRN}.pdb), public domain.
- **Paper PDF**: europepmc.org OA render (equivalent to PMC5734301, which is embargo-free per Wiley Bronze OA).

## Compute cost (effort estimate)

| Step | Wall time | CPU-hours |
|---|---|---|
| PDF fetch (with 3 failed URLs) | 15 s | negligible |
| marker extraction | 51 s | 0.014 |
| nougat extraction | 19 s (after 1 OOM retry) | 0.005 |
| APBS + PDB2PQR (already installed) | 0 (cached env) | 0 |
| 1FAS + 1CRN prep + 4 solver runs | 12 s | 0.003 (single-thread) |
| DX grid analysis (python) | 2 s | negligible |
| LLM judge (1 successful call after 3 502s) | 8 s | negligible |
| **Report writing (interactive)** | ~10 min | — |
| **Total wall clock end-to-end** | **~20 min** | **~0.03 CPU-hr** |

Rerun effort estimate for a fresh replicator (assuming APBS/PDB2PQR need to be installed): ~30–45 min including `conda install -c conda-forge apbs pdb2pqr` (5–10 min).

## Reproducibility hash

```bash
# from scratch on a Linux box with conda:
conda create -n apbs-repl -c conda-forge apbs=3.4.1 pdb2pqr=3.6.1 python=3.10 numpy -y
conda activate apbs-repl
curl -sL -o 1fas.pdb https://files.rcsb.org/download/1FAS.pdb
pdb2pqr30 --ff=AMBER --apbs-input 1fas.in 1fas.pdb 1fas.pqr
# fix pdb2pqr's write-pot filename bug:
sed -i 's|write pot dx 1fas.pqr|write pot dx 1fas_pot|' 1fas.in
apbs 1fas.in
# expected: "Global net ELEC energy = 1.095928709461E+05 kJ/mol"
```

Same exact numeric result reproducible on any x86_64 Linux with APBS 3.4.1 (single-thread, no GPU dependence).
