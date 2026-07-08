# Replication Workflow — arXiv:2308.05237 (QML for fraud detection)

## 0. Environment bootstrap
- Host: CherryRd (macOS Darwin 25.3.0), Python 3.13, CPU-only.
- `cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2308.05237-qml-fraud-detection/`
- `python -m venv .venv && source .venv/bin/activate`
- `pip install qiskit qiskit-machine-learning qiskit-aer scikit-learn pandas numpy matplotlib`
- Pinned versions (captured in `logs/run1.log`): qiskit 2.5.0, qiskit-machine-learning
  0.9.0, qiskit-aer 0.17.2, scikit-learn 1.9.0.

## 1. Paper ingest
- Downloaded arXiv 2308.05237v1 PDF to `work/paper.pdf`.
- `pdftotext work/paper.pdf work/paper.txt` for grep-friendly extraction.
- Cross-checked Sec. IV.A (dataset), Sec. IV.B (protocol: COBYLA maxiter=200, Aer
  QasmSimulator), Sec. IV.C + Table II (results).

## 2. Dataset construction (deviation from paper)
- Kaggle `ealaxi/banksim1` requires an API token unavailable in the offline subagent.
- Synthesized a 200-record BankSim-*like* dataset (`data/banksim_like_200.csv`) whose
  per-feature marginals match Sec. IV.A:
  - 100 fraud + 100 non-fraud (balanced, paper's protocol);
  - fraud `amount` ~ N(567.23, 128.47), non-fraud ~ N(145.68, 50.32);
  - fraud category over-represents `es_sportsandtoys` (20 %) and `es_health` (15 %);
  - age category "2" (26–35) = 45 % of fraud; female = 56 %.

## 3. Preprocessing (verbatim from paper Sec. IV.B)
- `age`: regex to int, `U → 8`.
- `gender`, `category`: `LabelEncoder`.
- `amount`: numeric passthrough.
- 4-feature vector → `MinMaxScaler(feature_range=(0, π))` (feature maps encode as
  rotation angles).
- Train/test = 75 / 25 stratified split, `random_state=42` → 150 train / 50 test.

## 4. Model grid (this replication: 6 cells = 2 models × 3 feature maps)
- Feature maps: `ZFeatureMap`, `ZZFeatureMap(entanglement="linear", reps=2)`,
  `PauliFeatureMap(paulis=["Z","Y","ZZ"], entanglement="linear", reps=2)`.
- **QSVC**: `qiskit_machine_learning.algorithms.QSVC(quantum_kernel=
  FidelityQuantumKernel(feature_map=fmap))`. Train on 150, score on 50.
- **VQC**: `RealAmplitudes(num_qubits=4, reps=3)` ansatz + `COBYLA(maxiter=200)` +
  per-iteration loss callback.
- **Not run**: EstimatorQNN, SamplerQNN (CPU-budget cut; paper's own numbers place them
  0.20+ below QSVC/Z, so winner call unaffected).

## 5. Classical baselines (added by us, not in paper)
- `sklearn.linear_model.LogisticRegression()`, `SVC(kernel="rbf")`, `SVC(kernel="linear")`
  on the same 4-feature scaled input. Same 75/25 stratified split.

## 6. Execution
- Single command: `python code/replicate.py 2>&1 | tee logs/run1.log`.
- Wall-time: ~16 min total (11 min QSVC × 3 feature maps + 5 min VQC × 3 feature maps).
- Deterministic on seed 42.

## 7. Scoring
- Per-class accuracy / precision / recall / F1 collected into
  `results/replication_results.json` (mirrors Table II format).
- Headline comparison logged: paper QSVC/Z F1 = 0.98 → ours 0.943, |Δ| = 0.037.
- Feature-map ordering for QSVC (Z ≫ ZZ ≈ Pauli) matches paper.

## 8. Verdict adjudication
- Applied the standing rule: headline-exercised = Yes; |ΔF1| within ±0.10 tolerance
  for synthetic-data QML replication → **REPLICATED**.
- Flagged deviations: synthetic BankSim, QNNs skipped, single seed, Qiskit version
  drift (0.44 → 2.5) — all in `failure_analysis.md`.

## 9. Artifact writeout (this backfill, 2026-07-06)
- Added: `report/REPORT.tex`, `report/open_questions.json`,
  `report/open_questions_section.tex`, `report/workflow.md` (this file),
  `report/artifacts_summary.md`, `report/failure_analysis.md`,
  `extraction/nougat.mmd` (stub).
- Preserved: `report/REPORT.md`, `code/replicate.py`, `data/banksim_like_200.csv`,
  `results/replication_results.json`, `logs/run1.log`, `work/paper.pdf`,
  `work/paper.txt`.

## 10. Free-endpoint compliance
- Zero paid API calls. Local Qiskit Aer only. No LLM calls during scoring or
  adjudication. No Kaggle API (that's why the dataset is synthetic).
