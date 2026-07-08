# Replication Report — arXiv:2310.12981

**Paper:** *Improved Pairwise Measurement-Based Surface Code*
Grans-Samuelsson, Mishmash, Aasen, Knapp, Bauer, Lackey, da Silva, Bonderson.
Quantum 8, 1429 (2024). DOI 10.22331/q-2024-08-02-1429. arXiv:2310.12981.

**Replicator:** Ollie (OpenClaw subagent), 2026-07-03.
**Set:** QC-100. **Verdict:** **SPOT-CHECK**.
**Directory:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2310.12981-improved-pair-meas-surface-code/`

---

## 1. Paper summary

The paper devises a new pair-measurement-based realization of the rotated
surface code on a rectangular qubit lattice, using single-qubit and
nearest-neighbor two-qubit Pauli measurements plus three auxiliary qubits per
plaquette. It is optimized for Majorana-based hardware. Headline performance
numbers on a standard circuit noise model:

* **Fault-tolerance threshold ≈ 0.66%** (their improved pair-measurement code).
* Compared to **1.3%** for the 4.8.8 Floquet code (Ref. [5] in paper).
* Pseudo-thresholds ~0.096% (surface code) vs ~0.143% (4.8.8) for `p_target = 10⁻¹²`.
* Achieves full code distance sub-threshold with appropriate boundaries.
* Modest threshold reduction when adding hook-error-preventing modifications.
* Presents an efficient dead-component (dead qubit / dead measurement) strategy.

## 2. Claims table

| ID | Claim | Type | Testable in-scope? | Tested here? |
|----|-------|------|--------------------|--------------|
| C1 | Improved pair-meas surface code has threshold ≈ 0.66% under standard circuit noise | Quantitative | Yes (full: needs their exact circuit) — Partial (sanity bound): Yes | Partial: bounded from above by standard-CNOT threshold |
| C2 | Their circuit period is 4 steps of syndrome extraction | Structural | Yes (in principle, requires circuit reconstruction) | No — out of scope |
| C3 | Syndrome extraction avoids bidirectional hook errors, achieving full distance with appropriate boundaries | Structural | Yes | No — out of scope |
| C4 | Hook-preventing variants: only modest threshold reduction | Quantitative | Yes | No — out of scope |
| C5 | Efficient dead-component strategy | Algorithmic | Yes | No — out of scope |
| C6 | 4.8.8 Floquet code threshold in comparable noise model: ~1.3% | Quantitative | Yes (external Ref. [5]) | No — only referenced |
| C7 | Standard rotated surface code with CNOT-based syndrome extraction: threshold ~1% (implicit baseline) | Quantitative | **Yes — directly** | **Yes** ✓ |

## 3. Method

We perform a real Stim + PyMatching threshold sweep on the *standard*
CNOT-based rotated surface code (Stim built-in circuit,
`surface_code:rotated_memory_z`) to (a) verify our simulation methodology
against a well-known literature threshold (~1%) and (b) establish an
upper-bound sanity check on the paper's 0.66% pair-measurement value (the
pair-measurement circuit is expected to have a lower threshold than the
CNOT circuit because it replaces unitary gates with noisier measurements).

We do **not** implement the paper's exact pair-measurement schedule
(three auxiliary qubits per plaquette, 4-step period, hook-preventing
variants) — that is a substantial engineering exercise beyond the scope of
this timeboxed replication.

### Exact commands

```
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install stim pymatching numpy
python code/threshold_sweep.py
```

### Tool versions

* stim `1.16.0`
* pymatching `2.4.0`
* numpy `2.5.0`
* Python 3 stdlib

### Sweep configuration

* Circuit: `stim.Circuit.generated("surface_code:rotated_memory_z", ...)`.
* Distances: d ∈ {3, 5, 7}; rounds = d.
* Noise: uniform `p` applied to `after_clifford_depolarization`,
  `after_reset_flip_probability`, `before_measure_flip_probability`,
  and `before_round_data_depolarization`.
* Physical error rates: p ∈ {0.002, 0.003, 0.004, 0.005, 0.006, **0.0066**,
  0.007, 0.008, 0.009, 0.010, 0.012, 0.014, 0.017, 0.020}.
* 20,000 shots per (d, p) point.
* Decoder: PyMatching from `circuit.detector_error_model(decompose_errors=True)`.
* Per-round LER conversion: `p_round = 0.5*(1 - (1 - 2*p_shot)^(1/rounds))`.
* Threshold estimated by linear interpolation of the (d=3 vs d=5),
  (d=5 vs d=7), and (d=3 vs d=7) per-round LER crossings.

## 4. Results

### 4a. Full sweep table

See `evidence/threshold_sweep_results.csv` and
`evidence/threshold_sweep_results.json` for the complete 42-point grid.

Selected rows near the paper's claimed threshold (p = 0.66%):

| distance | p_phys | shots | errors | p_shot | p_round |
|---------:|-------:|------:|-------:|-------:|--------:|
| 3 | 0.0066 | 20000 | 587 | 0.02935 | 9.98e-3 |
| 5 | 0.0066 | 20000 | 609 | 0.03045 | 6.24e-3 |
| 7 | 0.0066 | 20000 | 528 | 0.02640 | 3.86e-3 |

At p = 0.66% under standard CNOT surface code, per-round LER strictly
**decreases** with distance (9.98e-3 → 6.24e-3 → 3.86e-3), i.e. we are
**below** the CNOT-circuit threshold. This is consistent with the CNOT
threshold being ~1% and the paper's 0.66% figure being *below* both.

### 4b. Threshold crossings (per-round LER curves)

| pair | crossing p | bracket |
|------|-----------:|---------|
| d=3 vs d=5 | 0.0124 | [0.012, 0.014] |
| d=5 vs d=7 | 0.0111 | [0.010, 0.012] |
| d=3 vs d=7 | 0.0117 | [0.010, 0.012] |

**Measured standard CNOT surface code threshold: p_th ≈ 1.1–1.2%.**

This matches the well-known literature value of ~1% for the standard rotated
surface code under a symmetric depolarizing circuit noise model
(e.g. Fowler et al., Phys. Rev. A 86, 032324 (2012); Stim documentation).

### 4c. Results vs paper

| Quantity | Paper (pair-meas circuit) | This work (standard CNOT circuit) | Consistent? |
|----------|--------------------------|-----------------------------------|-------------|
| Fault-tolerance threshold | **~0.66%** | ~1.15% ± ~0.1% | ✓ Yes — CNOT threshold correctly exceeds pair-meas threshold; ordering as expected |
| Per-round LER trends with distance sub-threshold | Decreasing (full distance) | Decreasing (Table 4a) | ✓ Yes |
| Above-threshold LER trends | Increasing with distance | At p ≥ 0.014, d=7 > d=3 per-round LER (0.0429 > 0.0371) | ✓ Yes |

## 5. Verdict

### **SPOT-CHECK**

**Justification.**
* We ran a real Stim + PyMatching threshold sweep on the standard rotated
  surface code, obtaining a threshold estimate of ~1.15%, consistent with
  the well-known ~1% literature value.
* Because we did not implement the paper's exact pair-measurement circuit
  (3-ancilla-per-plaquette, 4-step period, hook-preventing variants), we
  cannot directly reproduce the 0.66% threshold headline.
* However, our measurement provides a **consistency bound**: the pair-meas
  threshold is expected to be *lower* than the CNOT threshold (pair-meas
  circuits replace unitary gates with noisier measurements), and 0.66% < 1.15%
  is consistent with that expectation.
* Our per-round LER numbers at p = 0.66% show correct sub-threshold scaling
  (decreasing with distance) under the CNOT circuit.
* The methodology (Stim generated circuit → detector error model → PyMatching
  minimum-weight-perfect-matching decoder → threshold from LER crossings) is
  the same standard pipeline the paper uses.

**Not REPLICATED because:** we did not simulate the paper's actual circuit.
**Not NO-GO because:** all tools (Stim, PyMatching) are open-source and the
paper's methodology is fully described; a full replication is achievable
with additional engineering time.
**Not CONTRADICTED because:** our measured CNOT threshold exceeds the
paper's pair-meas threshold in the direction expected by physics.

## 6. Evidence files

* `evidence/threshold_sweep_results.json` — full sweep grid + metadata.
* `evidence/threshold_sweep_results.csv` — same, tabular.
* `../code/threshold_sweep.py` — replication script (self-contained).
* `../logs/threshold_sweep.log` — full run transcript.
* `../paper/paper.pdf` — arXiv source PDF.
* `../paper/paper.txt` — pdftotext extraction.

## 7. What a full replication would require

1. Implement the paper's 4-step pair-measurement syndrome-extraction circuit
   as a Stim `.stim` file (rotated surface code, 3 auxiliary qubits per
   plaquette, Fig. 6 / 7 gates from the paper). ~1-2 days of work.
2. Implement the "hook-preventing" variant (Sec. 3.4) as a second circuit.
3. Re-run the threshold sweep on both circuits with the noise model in the
   paper's App. B (standard circuit noise + measurement noise for
   two-qubit Pauli measurements).
4. Cross-check threshold ≈ 0.66% (headline) and slightly-reduced threshold
   for hook-preventing variant.
5. (Optional) Reproduce Fig. 21 pseudo-thresholds at `p_target = 10⁻¹²`.

## 8. Runtime

Full sweep (3 distances × 14 p-values × 20,000 shots = 840,000 shots) ran in
**~10 seconds** on a single CherryRd CPU core. No HPC/GPU required.
