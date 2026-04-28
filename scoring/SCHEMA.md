# Replication Scoring Schema

Each paper evaluation is a JSON object with this schema, written to `evaluations.jsonl` (one JSON per line):

```json
{
  "osti_id": "2396968",
  "paper_title": "Latent Stochastic Differential Equations for Modeling Quasar Variability",
  "paper_authors": "Fagin et al.",
  "paper_year": 2024,
  "domain": "Astrophysics/ML",
  "replication_dir": "~/Dropbox/REPLICATE-PROJECT/2396968-Latent-.../replication/",
  "our_score": "5-6/10 (v1 simplified)",
  "coverage_score": 4,
  "coverage_rationale": "Replicated 1-band DRW + latent-SDE architecture + basic training loop. Did NOT replicate 6-band LSST multivariate structure, Sim5 GR ray-tracing, 9-param Cholesky head (the paper's core contributions).",
  "agreement_score": 6,
  "agreement_rationale": "Our single-band RMSE 0.198 vs paper's 6-band RMSE 0.096 - direct comparison not apt given simplification. Our GPR beats latent-SDE as expected in 1-band limit (Matern-1/2 IS DRW covariance). Methodology reproduces correctly where we did it.",
  "what_reproduced": [
    "Latent SDE architecture (GRU encoder -> Ito SDE -> MLP decoder)",
    "Girsanov KL loss via torchsde.sdeint(logqp=True)",
    "Adam training with linear KL annealing",
    "DRW driving signal simulation"
  ],
  "what_missing": [
    "6-band LSST multivariate architecture",
    "Sim5 GR ray-tracing transfer functions",
    "9-param Cholesky-Gaussian head for physical parameter inference",
    "100K curves/epoch regenerated training volume",
    "Full opsim LSST cadence"
  ],
  "followon_questions": [
    "Q1: How does the latent SDE's parameter recovery degrade as photometric noise scales to 10x LSST requirement?",
    "Q2: Can replacing the GRU encoder with a Transformer (time-series foundation model like TimesFM) improve parameter recovery for the weak-signal parameters (a, lambda_Edd)?",
    "Q3: What is the minimum survey duration (vs LSST 10yr) needed to recover log(M_BH) with 0.1 dex precision?",
    "Q4: Does adding broad-line region emission (reverberation mapping light curves) as an auxiliary input tighten black hole mass constraints?",
    "Q5: How robust is the latent SDE posterior calibration under model mismatch (e.g., the accretion disk is not a simple thin-disk lamppost)?"
  ]
}
```

## Scoring rubrics

### Coverage (1-10) — what fraction of paper's contributions we reproduced
- 10: Every major methodological element reproduced at or near paper's scale
- 8: Core method + main results reproduced, minor scale/data simplification
- 6: Core method reproduced, significant scale/feature simplification
- 4: Partial methodology (comparator arm only, or simplified formulation)
- 2: Only tangentially related demonstration
- 1: Method fundamentally not replicated

### Agreement (1-10) — how well our quantitative/qualitative results match paper
- 10: All reported metrics within 5-10% of paper values
- 8: Most metrics within 20%, all trends correct
- 6: Qualitative agreement; metric-by-metric differ 20-50%
- 4: Qualitative agreement at mechanism level only
- 2: Weak agreement, some trends opposite
- 1: Results contradict paper

### Follow-on questions (exactly 5)
Each should be:
- Concrete and testable
- Extends paper's method or probes robustness
- Appropriate for an AI-assisted research agent (not requiring months of wet lab)
- Specific enough to have a well-defined deliverable
