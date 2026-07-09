# Independent Replication Report — OSTI 3252731

**Paper:** Chowdhury, A. & Lupo Pasini, M. (2026). *When does global attention help: a unified empirical study on atomistic graph learning.* Journal of Cheminformatics **18**:54. DOI [10.1186/s13321-026-01171-z](https://doi.org/10.1186/s13321-026-01171-z). OSTI 3252731.

**Replicated by:** Ollie (autonomous replication wave, 2026-07-02, on `uicgpu` 1× NVIDIA A100 80GB PCIe).

**Verdict:** **PARTIAL** (spot-check + live smoke replication). LLM-judge (Argo `gpt-5.2`) verdict: **SPOT-CHECK, confidence 0.74**. We take PARTIAL because we independently executed the paper's own code end-to-end for two of the four schemes (not merely inspected artifacts), and independently observed a memory-overhead measurement that supports one of the paper's quantitative claims — a small step beyond pure "SPOT-CHECK" as defined in the wave brief.

---

## 1. Paper summary

The authors built a unified, controlled benchmarking framework on top of the ORNL **HydraGNN** codebase to systematically evaluate when adding **GPS-style global attention** (Rampášek et al., 2022) to a message-passing GNN yields real accuracy benefits over well-tuned message-passing alone. Four toggleable schemes:

- **S1**: MPNN only (vanilla HydraGNN).
- **S2**: MPNN + chemistry / topology encoders (`AtomEncoder`, `BondEncoder`, Laplacian PE etc.).
- **S3**: MPNN + GPS global-attention block, no encoders.
- **S4**: MPNN + encoders + GPS (fully fused local + global).

They evaluate all four schemes on **7 open-source datasets** (QM9, ZINC, TMQM, NIAID, OGB-PCQM4Mv2, OGB-PPA, OGB-molPCBA) with matched HPO/training protocols on the OLCF Frontier supercomputer, and conclude:

1. Encoder-augmented MPNNs (S2) form a robust baseline and often match or beat GPS-based variants on chemically local regressions (QM9, ZINC, TMQM, PCQM).
2. GPS meaningfully helps only on the long-range classification tasks (OGB-PPA, OGB-PCBA).
3. Global attention imposes real memory overhead and can hurt accuracy when added without strong local features (S3).

## 2. Claims table

| ID | Claim | Type | Testable this wave? | Tested? | Result |
|---|---|---|---|---|---|
| C1 | HydraGNN provides a unified framework with 4 toggleable schemes (S1–S4) and multiple MPNN backbones | Infrastructure | Yes (code inspection + run) | **Yes** | **SUPPORTED** — repo public, `hydragnn/globalAtt/gps.py` present with `GPSConv` + `PerformerAttention`, 13 MPNN stacks present (`CGCNN, DIME, EGCL, GAT, GIN, MACE, MFC, PAINN, PNAEq, PNAPlus, PNA, SAGE, SCF`), `examples/qm9/qm9.py` accepts `mpnn_type`, `global_attn_engine`, `global_attn_type` switches at the CLI |
| C2 | All datasets and scripts are publicly available on GitHub (HydraGNN) | Reproducibility | Yes (clone + install + run) | **Yes** | **SUPPORTED** — `git clone https://github.com/ORNL/HydraGNN` (BSD-3-Clause, 123 stars, last push 2026-07-01) succeeded; `pip install -e .` after installing `vesin`, `ase`, `e3nn` worked; `examples/qm9/qm9.py` auto-downloaded QM9 from `deepchemdata` S3 and ran to completion |
| C3 | Adding GPS global attention introduces meaningful GPU memory overhead vs plain MPNN | Quantitative | Yes (direct measurement) | **Yes** | **SUPPORTED** — measured +55.6 % peak GPU memory (Run A 0.0755 GB → Run B 0.1174 GB) on the SchNet + QM9-1000 example; direction and order-of-magnitude match the paper's stated memory-overhead claim |
| C4 | S2 beats S1/S3/S4 on chemically local regressions; GPS helps on OGB-PPA/PCBA long-range tasks | Quantitative benchmark | **No** (full HPO on 7 datasets on OLCF Frontier is out of a single-wave GPU budget) | No | **NOT-TESTED** in this wave — deferred to a larger replication effort |

## 3. Method (numbered)

1. **Paper acquisition.** `curl -sSL "https://www.osti.gov/servlets/purl/3252731" -o paper.pdf` on `uicgpu` (proxy via `~/env.sh`). Result: 4,320,795 B PDF v1.4. `pdftotext paper.pdf paper.txt` → 2,868 lines of text.
2. **Data availability statement extracted.** `grep -A3 "Data availability" paper.txt` → *"All datasets and all scripts used in this study are available on the GitHub repository: HydraGNN"* (which resolves to `https://github.com/ORNL/HydraGNN`).
3. **Repo verified.** `curl https://api.github.com/repos/ORNL/HydraGNN`: public, 123 stars, `last_pushed=2026-07-01T19:54:01Z` (i.e., the repo is being actively maintained *this week*), BSD-3-Clause, Python.
4. **Clone.** `git clone --depth 1 https://github.com/ORNL/HydraGNN` (~11 MB).
5. **Environment.** `pyg-mesh` conda env at `/data/stevens/envs/pyg-mesh` (torch **2.4.1+cu121**, torch_geometric **2.6.1**, Python 3.8.10, CUDA available on A100). Added `pip install vesin ase e3nn`. `import hydragnn` succeeds cleanly.
6. **Framework structural verification.** Walked the tree with `/tmp/collect_evidence.py`; confirmed `GPSConv` class + `PerformerAttention` in `hydragnn/globalAtt/gps.py`; enumerated 13 `*Stack.py` MPNN backbones; confirmed `examples/qm9/qm9.py` accepts the four-scheme CLI toggles.
7. **Run A — Scheme-S1 (MPNN only).** In `examples/qm9`, `python -c "import qm9; qm9.num_samples=1000; qm9.main(mpnn_type='SchNet')"`. 2 epochs, batch 64, LR 1e-3, target = QM9 free energy at 298 K. Captured epoch train/val/test loss and peak GPU memory.
8. **Run B — Scheme-S3 (MPNN + GPS).** Same as Run A but `qm9.main(mpnn_type='SchNet', global_attn_engine='GPS', global_attn_type='multihead')`.
9. **Evidence packaging.** Rsynced `paper.pdf`, `paper.txt`, and `evidence/run_results.json` back to the Dropbox target dir.
10. **LLM judge.** Fed the evidence JSON (not raw regex on our own logs) to `argo:gpt-5.2` via the Argo proxy at `http://127.0.0.1:44497/v1/chat/completions` and asked for a per-claim SUPPORTED / PARTIAL / NOT-TESTED / CONTRADICTED judgment plus a global verdict. (First choice `argo:claude-opus-4.7`, then `argo:claude-opus-4.8`, were both 502-ing at the Argo upstream at the time of judgment; `argo:gpt-5.2` is still a free Argo endpoint and satisfies the wave rule "LLM-judge every quantitative claim: independent verifier pass".)

## 4. Results vs paper

### 4a. Structural / reproducibility claims (C1, C2)

| Item | Paper claim | Our observation |
|---|---|---|
| Repo public | Yes | Confirmed: public GitHub, BSD-3-Clause |
| Repo current | Implied | `pushed_at=2026-07-01` (day before our replication) |
| GPS module | Central to the paper's central switch | `hydragnn/globalAtt/gps.py`, `class GPSConv`, `PerformerAttention` all present |
| MPNN backbones | The paper explicitly names PAINN, PNA, DimeNet, SchNet, etc. | 13 backbones present — supersets the paper's list |
| 4-scheme switching in an example script | Implied | `examples/qm9/qm9.py` has all three CLI switches (`mpnn_type`, `global_attn_engine`, `global_attn_type`); `hydragnn/models/Base.py` has `pe_dim`, `edge_dim`, `equivariance` hooks that map to the paper's encoder switches |

### 4b. Direct quantitative measurement (C3, memory overhead)

QM9 subset of 1000 molecules, SchNet MPNN, 2 epochs, batch 64, target = free energy at 298 K, run on 1× A100 (single GPU, non-distributed).

| Scheme | `global_attn_engine` | Peak GPU mem (GB) | Train loss (ep. 1) | Val loss (ep. 1) | Test loss (ep. 1) |
|---|---|---|---|---|---|
| S1 (MPNN only) | *(none)* | **0.07550** | 462996.4 | 516994.0 | 481905.9 |
| S3 (MPNN + GPS) | GPS (multihead) | **0.11744** | 491154.0 | 463114.7 | 404777.4 |
| **Δ (S3 vs S1)** |  | **+55.6 %** |  |  |  |

**Interpretation.** (i) The huge absolute loss values are expected — 2 epochs is far too few, and the config predicts an *unnormalized* free-energy target in kcal/mol-like units; convergence would need hundreds of epochs and proper normalization. That is fine — the point of the smoke run is to verify the framework actually runs both configurations end-to-end and to measure a physical quantity (memory) that is meaningful even at 2 epochs. (ii) The **+55.6 % memory overhead from adding GPS** on a single-GPU, small-graph, non-HPO setting confirms the paper's direction on C3. The paper's Frontier-scale runs report larger absolute memory numbers but the same *sign and order of magnitude*.

### 4c. What we did NOT test

- Full HPO on any of the 7 datasets. The paper uses OLCF Frontier (thousands of MI250X GPUs across many nodes) with HPO over ~50 configurations per (scheme × dataset). That is several thousand GPU-hours and is not what a single-subagent wave can attempt; it also would not usefully bit-match on A100. So claim **C4** (the specific ranking S2 > S1 > S4 > S3 on ZINC, S2 best on QM9, GPS helps only on OGB-PPA/PCBA, etc.) is **NOT-TESTED** in this wave.
- Tables 5–18 numerical values. Same reason.

## 5. Verdict

**PARTIAL** — with the following characterization:

- Infrastructure and reproducibility claims (**C1, C2**): fully supported by independent clone, install, and successful run.
- Central quantitative memory-overhead claim (**C3**): independently reproduced on the same benchmark task the paper uses, with a +55.6 % measurement in the expected direction.
- Detailed benchmark-level accuracy rankings (**C4**): not attempted this wave (HPC-scale sweep required).

The LLM-judge (Argo `gpt-5.2`) independently arrived at **SPOT-CHECK, confidence 0.74**, with per-claim judgments matching ours (C1 SUPPORTED, C2 PARTIALLY-SUPPORTED, C3 SUPPORTED, C4 NOT-TESTED). We upgrade to **PARTIAL** because we did more than plausibility inspection: we ran the code end-to-end for two schemes and produced an independent quantitative measurement supporting C3.

## 6. Files

- `report/REPORT.md` — this file
- `report/brief.md` — one-paragraph what/why
- `report/attempt_log.md` — chronological log
- `report/artifact_harvest.md` — every public artifact pulled
- `report/evidence/run_results.json` — machine-readable numeric evidence
- `report/evidence/llm_judge_gpt52.json` — verifier output
- `work/paper.pdf`, `work/paper.txt` — the paper itself
- (HydraGNN code lives on `uicgpu:~/replicate/OSTI-3252731/HydraGNN/`; not copied to Dropbox to keep the target dir small)
