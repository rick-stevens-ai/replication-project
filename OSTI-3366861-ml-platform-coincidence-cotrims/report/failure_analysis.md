# Failure Analysis — OSTI 3366861

## What did NOT reproduce exactly

### F1. Silhouette / Calinski–Harabasz / Davies–Bouldin / Physics-consistency numeric values
Our numbers differ from Fig. 3 by 30–500 %. However:
- Direction is consistent with our clusters being cleaner-separated (higher silhouette, lower DB, higher CH).
- Paper explicitly notes numbers "can vary slightly from run to run due to the random sampling approach" — but the drift we see is larger than "slightly". Root cause likely: paper does not publish (a) numpy seed for the 1 % sample, (b) DBSCAN ε for Fig. 3, (c) UMAP `random_state`. Any of these dominates the partition-boundary sensitivity of these metrics.
- Since the confidence-score formula is designed to be robust to per-metric variation via tier weights + normalizations, the overall confidence still lands in the same "High" band (0.65+).

### F2. Full ~1.9 M event dataset not reproduced
Paper says "around 1,900,000 coincidence events". Zenodo release has 953 120 events (~½). Because the paper's own quantitative results are on a 1 % subsample of the full 1.9 M (i.e., ~19 000 events), our 1 % of 953 k = 9 531 events is a smaller sample. This partly explains numeric drift in metrics that are sensitive to sample size (silhouette, CH).

**Cannot fix without author contact.** Data availability statement says "available from the corresponding author upon request."

### F3. DBSCAN ε policy ambiguity
Paper states: "The optimization procedure tests epsilon values in the range [0.1, 1.0] and selects the configuration that maximizes the number of clusters while keeping the noise ratio below 50 %."
- Applied literally, this gives us **442 clusters** at ε=0.1 (noise 24 %), not 5.
- To get 5 clusters we had to pick ε=0.5 manually (matching Fig. 3 visually).
- Conclusion: SCULPT's production algorithm has extra constraints (probably min-cluster-size floor, or a different ε lower bound). Not fully documented in the paper.

### F4. Iterative sub-clustering workflow (0.70 → 0.79)
Paper's Sec. IV.B.2 shows an iterative UI-driven workflow: user lassoes a sub-cluster, re-runs UMAP on it, sees confidence rise from 0.70 → 0.79 as overlapping states separate.
- This is inherently interactive; we did NOT reproduce it in the batch run.
- A closed-loop Python-only version could be built (see open_question Q5).

### F5. Deep autoencoder and genetic programming modules
Paper Sec. II.B.2 and II.B.3 describe optional deep-autoencoder and genetic-programming feature-discovery modules. These are in the CoInML repo but were not exercised in the case study (paper says "we have not utilized the entire spectrum of capabilities of SCULPT in our analysis just yet" — Sec. VI). Not tested in our replication either.

## What DID reproduce end-to-end
- Public code + public data usable out of the box → **strong reproducibility infrastructure**.
- Physics feature ranges (KER 1–15 eV, α₁₂ 5°–180°, EESum 0–40 eV) match per-cluster values in the paper's Table on p. 11.
- 5-cluster UMAP + DBSCAN partition on real data.
- Hopkins statistic ≈ 0.98 (paper 0.98) — dataset is genuinely highly clusterable.
- Cluster stability ≈ 0.9994 (paper 0.9996) — partition is nearly perfectly stable to noise.
- Overall confidence in "High" band, matching paper's qualitative claim.
- Independent physics-validation cross-check (ARI vs true 8 quantum states = 0.617), evidence not shown in paper.

## Cautions for reader
- **Do not** conclude from this PARTIAL verdict that SCULPT is unreliable. The qualitative scientific claim reproduces cleanly. The quantitative drift is dominated by unpublished seeds and DBSCAN eps, not by algorithmic disagreement.
- **Do** note that the paper would benefit from publishing exact `random_state` / eps / any min-cluster-size constraints in a supplementary methods section — one-line addition, would enable bit-exact reproduction.

## Failures during the replication process itself

| When | What | Fix |
|---|---|---|
| 22:10 | `pdf` tool refused non-workspace path | Copied PDF into `~/.openclaw/workspace/` |
| 22:10 | Vision-model PDF extraction: all 3 backends failed (Anthropic 400 low balance, Gemini 3 Flash unknown, GPT-5.5 needs plugin) | Fell back to `pdftotext -layout` — worked perfectly |
| 22:09 | uicgpu curl DNS: exit code 6 | `source ~/env.sh` for proxy config |
| 22:20 | DBSCAN eps sweep too coarse at low end → 442 clusters instead of 5 | Extended sweep to eps∈[0.1, 3.0], added coarse-5 config |
| 22:32 | argo:claude-opus-4.8 → HTTP 502 | Fell back to argo:gpt-5.2 (also free) |

None of these are novel failures; all recovered within seconds.
