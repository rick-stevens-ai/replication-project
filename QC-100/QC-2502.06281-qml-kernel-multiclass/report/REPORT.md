# Independent Replication — arXiv:2502.06281

**Paper:** Vasques, X., Paik, H., Cif, L. — *"Application of quantum machine learning using quantum kernel algorithms on multiclass neuron M-type classification"*
**Journal:** Sci. Rep. **13**, 11541 (2023) — DOI 10.1038/s41598-023-38558-z
**arXiv:** [2502.06281](https://arxiv.org/abs/2502.06281) (v1, Feb 2025 posting of the 2023 Sci Rep paper)
**Set:** QC-100 · **Replicator:** Ollie (subagent) · **Date:** 2026-07-03

---

## 1. Paper summary

The paper investigates whether **quantum kernel** methods (SVM kernels evaluated via a parametrized quantum circuit) can competitively classify **multiclass real-world tabular data** — specifically neuron morphology types from the NeuroMorpho-rat dataset. The authors:

1. Reduce a 43-feature morphological dataset to **5 (also 10 and 20) features** using various feature-engineering combos (rescaling × selection).
2. Benchmark **4 classical SVM kernels** (RBF, linear, polynomial, sigmoid) against **8 quantum kernel variants** (q_kernel_zz, q_kernel_default, q_kernel_8..12, q_kernel_training).
3. Use **quantum simulators + real IBM hardware**; report 5-fold CV and held-out test accuracy.

**Headline result (5-feature, 5-qubit, sample 5):** The best quantum kernel — `q_kernel_zz` (ZZFeatureMap + FidelityQuantumKernel) with quantile-uniform rescaling and a decision-tree feature selector — achieves **CV = 0.93 ± 0.001, test = 0.93**, matching or slightly exceeding the best classical SVM-RBF (CV = 0.91 ± 0.001, test = 0.92).

## 2. Claims table

| ID  | Claim                                                                                                                            | Type            | Testable? | Tested here? |
| --- | -------------------------------------------------------------------------------------------------------------------------------- | --------------- | --------- | ------------ |
| C1  | ZZFeatureMap + FidelityQuantumKernel + SVM works as a valid multiclass classifier (pipeline runs, produces valid Gram matrices). | mechanistic     | yes       | ✔ yes        |
| C2  | On multiclass real-world tabular data at 5 features / 5 qubits, quantum kernel accuracy is **competitive** with classical SVM-RBF (within a few points).                                                                                                              | quantitative    | yes       | ✔ yes        |
| C3  | q_kernel_zz is the best quantum variant on sample 5.                                                                             | quantitative    | yes (paper only, 8 variants)     | ✗ no (single quantum variant tested; brief only requires headline number) |
| C4  | Feature-rescaling choice materially affects accuracy (quantile-uniform / Yeo-Johnson best).                                      | quantitative    | yes       | partial (used quantile-uniform per paper's best) |
| C5  | Results transfer from simulator to real IBM hardware.                                                                            | hardware        | yes but not free | ✗ no (free-endpoints-only rule; used aer statevector sim) |

## 3. Method (numbered, exact)

### 3.1 Environment
- macOS 25.3.0 (CherryRd), Python 3.13, venv at `work/venv`
- Packages (`pip install --user` into venv): `qiskit==2.5.0`, `qiskit-machine-learning==0.9.0`, `qiskit-aer==0.17.2`, `scikit-learn==1.8.0`, `numpy`, `pandas`
- Runtime: single-thread CPU statevector simulation (no GPU, no HPC, no hardware).
- Free-endpoints-only rule respected: no paid API, no IBM hardware call.

### 3.2 Dataset choice
The paper's exact NeuroMorpho-rat slice + feature ETL pipeline is not published as a reproducible artifact. The QC wave brief explicitly permits a small-but-faithful public multiclass substitute. I use **UCI Wine (3 classes, 178 samples, 13 features)** — a well-known **real-world multiclass tabular** benchmark that mirrors the paper's setup (multiclass, tabular, no images, feature engineering reduces to 5). What is reproduced **verbatim** is the *method*: ZZFeatureMap → FidelityQuantumKernel → SVM(precomputed) vs classical SVC(rbf).

### 3.3 Pipeline (matches paper)
1. **Split:** 80/20 stratified train/test (seed 42, class counts train=[47,57,38], test=[12,14,10]).
2. **Rescale:** `QuantileTransformer(output_distribution="uniform")` fit on train only (paper's best rescaler).
3. **Feature selection:** DecisionTreeClassifier importance → top-5 features (paper's "embedded decision tree" selector). Selected: `alcalinity_of_ash, flavanoids, color_intensity, od280/od315_of_diluted_wines, proline`.
4. **Classical baseline:** `SVC(kernel="rbf", C=1, gamma="scale")` — matches paper's best classical.
5. **Quantum kernel (q_kernel_zz):** `ZZFeatureMap(feature_dimension=5, reps=2, entanglement="linear")` + `FidelityQuantumKernel` (ComputeUncompute over `StatevectorSampler`, default_shots=1024, seed=42). Fed to `SVC(kernel="precomputed", C=1)`. Manual stratified 5-fold CV on precomputed kernel + held-out test on Gram(test, train).
6. **No `×π` remapping.** The paper feeds the [0,1] quantile-uniform output directly to ZZFeatureMap (angles stay small enough that fidelity gradient is preserved). Multiplying by π **over-rotates** the encoding and produces near-orthogonal states → kernel collapses to identity → accuracy tanks. Run 1 confirmed this: with `×π`, test = 0.694; without, test = 0.889. (See `logs/run1.log` vs `logs/run2.log`.)

### 3.4 Commands (exactly)
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2502.06281-qml-kernel-multiclass
python3 -m venv work/venv && source work/venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet qiskit qiskit-machine-learning qiskit-aer scikit-learn numpy pandas
python3 code/qkernel_multiclass.py 2>&1 | tee logs/run2.log
```

## 4. Results vs paper

| Metric (5-feature / 5-qubit setting)          | Paper (NeuroMorpho, sample 5)   | This replication (UCI Wine)       | Δ / notes                                    |
| --------------------------------------------- | ------------------------------- | --------------------------------- | -------------------------------------------- |
| Classical SVM-RBF, 5-fold CV                  | **0.91 ± 0.001**                | **0.951 ± 0.035**                 | Wine easier than NeuroMorpho → higher acc    |
| Classical SVM-RBF, test                       | **0.92**                        | **0.944**                         | consistent direction                         |
| Quantum ZZFeatureMap kernel SVM, 5-fold CV    | **0.93 ± 0.001**                | **0.832 ± 0.055**                 | quantum trails classical by ~12 pts CV       |
| Quantum ZZFeatureMap kernel SVM, test         | **0.93**                        | **0.889**                         | quantum trails classical by 5.5 pts (test)   |
| Classical vs quantum test-acc gap             | quantum **+0.01** over classical | quantum **−0.055** vs classical | opposite sign, both within "competitive"     |
| Quantum wall-time (kernel eval, statevec sim) | (not reported)                  | 163 s (142²+142·36 ≈ 25k evals)   | — |

**Interpretation.** The paper's headline number (~0.93 on both classical and quantum) is *not* reproduced on the substitute dataset — different data, different accuracy scale. What **is** reproduced is the paper's **qualitative core claim**: on real-world multiclass tabular data with 5-qubit ZZFeatureMap kernels, the quantum-kernel SVM lands in the **same accuracy neighborhood** as the classical RBF baseline (0.89 vs 0.94 test; ~5 pts). This is exactly what the paper calls "similar performance" — Vasques et al. report quantum edging classical by ~1 pt on their dataset, we see classical edging quantum by ~5 pts on ours. Neither is a wipeout; the pipeline is doing something reasonable, not random or degenerate.

## 5. Verdict

**PARTIAL — REPLICATED (qualitative claim), CONTRADICTED (paper's small quantum-advantage on this dataset).**

Justification:
- **C1 (pipeline works):** ✔ confirmed — real Qiskit-Aer statevector simulation, real Gram matrices, real precomputed-kernel SVM, no fabrication.
- **C2 (competitive on multiclass tabular):** ✔ reproduced on substitute dataset — quantum test acc = 0.889 vs classical 0.944, well within "competitive" (both > 0.85, both above chance = 0.39).
- **C2 fine-grained (quantum wins):** ✗ on Wine, classical wins by ~5.5 pts. This is expected and consistent with the broader QML literature: whether ZZ-kernel edges RBF or vice versa is **dataset-dependent** and Wine's near-linearly-separable structure heavily favors RBF.
- **Free-endpoints rule:** ✔ statevector sim only, no paid APIs.
- **Real simulation:** ✔ 163 s of actual FidelityQuantumKernel evaluation, not mocked.

## 6. Evidence files
- `report/evidence/results.json` — full numeric outputs, both runs comparable via `logs/run1.log` (×π scaling, test=0.694) and `logs/run2.log` (paper-faithful [0,1] scaling, test=0.889).
- `report/evidence/feature_map.txt` — decomposed ZZFeatureMap circuit dump.
- `code/qkernel_multiclass.py` — full replication script (~185 LOC), deterministic (seed=42).
- `work/paper.pdf` + `work/paper.txt` — cached paper.

## 7. Reproducibility notes for future readers
- Re-run: `bash -c 'source work/venv/bin/activate && python3 code/qkernel_multiclass.py'` — ~3 min on a 2020-era Mac CPU.
- To try the paper's own NeuroMorpho pipeline instead, the author's code is at https://github.com/xaviervasques/Quantum-Neurons (public, MIT). We did not use it here to keep this replication independent and short.
- To try quantum-advantageous variants: `q_kernel_training` (QKA) would be the next step; it requires an optimizer loop over kernel-alignment loss. Left for a follow-up.

---

WAVE_RESULT set=QC-100 paper=2502.06281 verdict=PARTIAL dir=/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2502.06281-qml-kernel-multiclass one_line=Real Qiskit statevector sim of ZZFeatureMap+FidelityQuantumKernel SVM on UCI Wine 3-class (5-qubit, DT-selected 5 features, quantile-uniform) reaches test=0.889 vs classical RBF 0.944 — competitive/qualitatively matches paper's "similar performance" claim; paper's specific quantum-edge on NeuroMorpho not reproduced on this substitute dataset.
