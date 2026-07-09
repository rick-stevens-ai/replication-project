# Workflow — OSTI 3366861 Replication

## End-to-end pipeline

```
┌────────────────────────┐   ┌────────────────────┐   ┌─────────────────────────┐
│ 1. Fetch paper PDF     │──▶│ 2. Clone SCULPT    │──▶│ 3. Download D2O Zenodo  │
│  (osti.gov/purl/...)   │   │  AMOS-experiment/  │   │  (56.5 MB, 8 files,     │
│                        │   │  CoInML on GitHub  │   │  953 120 events)        │
└────────────────────────┘   └────────────────────┘   └────────────┬────────────┘
                                                                    │
                                                                    ▼
┌────────────────────────┐   ┌───────────────────────┐   ┌────────────────────────┐
│ 6. Adaptive-confidence │◀──│ 5. Compute quality    │◀──│ 4. Physics features    │
│  score (paper Eq. 1)   │   │  metrics: silhouette, │   │  (KER, EESum, TotalE,  │
│  + tier weights + caps │   │  Hopkins, stability,  │   │  alpha_12) + 1 % sub-  │
│  + asymptotic bonus    │   │  CH, DB, phys-consis  │   │  sample + UMAP + DBSCAN│
└────────────┬───────────┘   └───────────────────────┘   └────────────────────────┘
             │
             ▼
┌────────────────────────┐   ┌────────────────────┐
│ 7. Compare to Fig. 3   │──▶│ 8. LLM-judge       │
│  numerics + ARI vs     │   │  verdict via Argo  │
│  ground-truth states   │   │  (argo:gpt-5.2)    │
└────────────────────────┘   └────────────────────┘
```

## Tools & codes

| Step | Tool | Version | Location |
|---|---|---|---|
| 1 | curl | system | uicgpu |
| 2 | git | system | uicgpu |
| 3 | zip/unzip | system | uicgpu |
| 4 | Python 3.8 venv | stdlib | uicgpu:~/sculpt-work/sculpt_env |
| 4 | numpy | 1.24.4 | pip in venv |
| 4 | pandas | 2.0.3 | pip in venv |
| 4 | umap-learn | 0.5.7 | pip in venv |
| 4 | scipy | 1.10.1 | pip in venv |
| 5 | scikit-learn | 1.3.2 | pip in venv (silhouette, CH, DB, ARI, DBSCAN) |
| 6 | pure numpy | — | `work/replicate_v2.py` implements the paper's Sec. II.C formula directly |
| 8 | Argo proxy (free) | cherryrd :44497 | model = `argo:gpt-5.2` |

## Machines & host layout

| Role | Host | Path |
|---|---|---|
| Heavy compute (UMAP, DBSCAN, metrics) | **uicgpu** (8×A100) | `~/sculpt-work/` |
| Report writing + LLM-judge | **cherryrd** (main gateway host) | `~/Dropbox/REPLICATE-PROJECT/OSTI-3366861-...` |

All heavy work was CPU (UMAP + DBSCAN + metrics are not GPU-accelerated in this pipeline). uicgpu was chosen for RAM + reliability; execution was well under 5 minutes wall-clock for the 9531-event UMAP + full metric suite.

## Effort estimate

| Stage | Wall-clock | Human effort |
|---|---|---|
| Paper reading + planning | — | 15 min |
| PDF fetch + extract + text scan | — | 5 min |
| Clone SCULPT + inspect source | 1 min | 10 min |
| Zenodo download (56.5 MB) | 30 s | — |
| Venv install (umap-learn, sklearn) | 4 min | 1 min |
| First replicate run (v1) + debug ε grid | 2 min compute | 15 min |
| Refined replicate_v2 with ε sweep + coarse-5 config | 3 min compute | 20 min |
| Confidence-score formula re-implementation + sanity check vs SCULPT source | — | 15 min |
| ARI-vs-truth cross-check (independent of paper) | 5 s | 5 min |
| LLM-judge prompt + call | 1 min | 5 min |
| REPORT.md + brief + open_questions + workflow + artifacts_summary + failure_analysis | — | 30 min |
| **Total** | **~11 min compute** | **~2 hours human/agent** |

## Reproduction command (single shot on uicgpu)

```bash
cd ~/sculpt-work
source sculpt_env/bin/activate
python replicate_v2.py    # writes out/replicate_v2.json
```

Prereqs already staged on uicgpu:~/sculpt-work/: `D2O_data/D2O_dataset/*.dat`, `CoInML/`, `sculpt_env/`.
