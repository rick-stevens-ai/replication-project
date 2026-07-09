# Workflow — QC-200 replication of PANSATZ (Meirom & Frankel 2023)

## Tools used (with versions)

| Tool | Version | Purpose |
|---|---|---|
| macOS zsh | (Darwin 25.3.0) | shell |
| curl | system | fetch PDF from Frontiers, hit Argo LLM endpoint |
| pdftotext (poppler) | system | Marker/Nougat fallback extractions and `paper.txt` skim |
| shasum | system | verify paper SHA256 against manifest |
| Python | 3.14.6 (Homebrew) | reproduction runtime |
| pip / venv | stdlib | isolated environment at `work/venv/` |
| Qiskit | 2.5.0 | quantum circuit + Statevector + EfficientSU2 ansatz |
| qiskit-nature | 0.8.0 | PySCFDriver + ParityMapper + two-qubit reduction |
| PySCF | 2.13.1 | independent FCI reference energies |
| NumPy | system | linear algebra + eigen-decomposition of Hamiltonian |
| SciPy | system | `scipy.optimize.minimize(method="COBYLA")` VQE optimizer |
| Argo LLM proxy | localhost:44497 + litellm :4000 | free LLM inference for judge scoring |
| argo:gpt-5.2 | (Argonne Argo) | LLM judge #1 |
| argo:gpt-5.4 | (Argonne Argo) | LLM judge #2 |
| pdflatex | not run (LaTeX not available on host in this session; REPORT.tex written but not compiled) | LaTeX -> PDF |

## Workflow steps

```
1. Paper identification & fetch
   1a. Try https://arxiv.org/abs/2023.12735  -> HTTP 404. Not arXiv.
   1b. Interpret slug "type-original-research-published-09-october" as
       Frontiers-style hint (article type + publication date).
   1c. Query Crossref: publisher-name=Frontiers,
       filter=from-pub-date:2023-10-09,until-pub-date:2023-10-09,
       query=quantum. Single hit -> DOI 10.3389/frqst.2023.1273581.
   1d. Fetch PDF from
       https://www.frontiersin.org/journals/quantum-science-and-technology/articles/10.3389/frqst.2023.1273581/pdf
       (HTTP 200, 1,891,804 bytes).
   1e. shasum -a 256 paper.pdf ->
       e4360ed9d9b62ea0df0035253b8d6dfff4c184bd92dc48a7b4b6527fbbca3fdd
       (MATCHES manifest byte-for-byte).
   1f. Copy paper.pdf to target-dir root; record all above in
       work/paper_provenance.md.

2. Paper reading
   2a. pdftotext -layout paper.pdf work/paper.txt
   2b. Read title, abstract, Sec. 2 (setup), Sec. 3 (Results), Sec. 4
       (Summary). Extract:
         - Ansatz mechanism: pulse-duration parameters, DRAG + CR pulses
         - Molecules: H2, HeH+, LiH (STO-3G)
         - Chemical accuracy threshold: 0.0016 Ha
         - Hardware run: ibm_lagos, readout-only mitigation
         - Baseline: 1-layer Real-Amplitudes HEA (GANSATZ)

3. Pick the ONE most-checkable number
   -> H2 STO-3G, 2-qubit parity-reduced, ideal-simulator VQE reaching
      chemical accuracy across all bond distances (Fig. 3A/3D).

4. Environment
   4a. python3 -m venv work/venv --system-site-packages
   4b. source work/venv/bin/activate
   4c. pip install 'qiskit>=1.0' qiskit-nature pyscf numpy scipy

5. H2 reproduction
   5a. Write report/evidence/h2_vqe_reproduce.py:
       - PySCFDriver(H 0 0 0; H 0 0 d, sto3g).run()
       - ParityMapper(num_particles).map(second_q_op)  [gives 2-qubit op]
       - qubit_H.to_matrix() -> np.linalg.eigvalsh  [eigen-FCI]
       - pyscf.fci.FCI(RHF(mol)).kernel()  [independent FCI]
       - EfficientSU2(2, reps=2, "linear") ansatz + COBYLA seed=42
       - Loop over d in {0.5, 0.7, 0.9, 1.1, 1.5, 2.0, 2.5} Angstrom
       - Dump JSON to report/evidence/h2_vqe_results.json
   5b. python3 report/evidence/h2_vqe_reproduce.py  [runs in ~90s]
       -> 7/7 distances chemical-accurate; err at 0.7 A ~ 3e-9 Ha.

6. HeH+ reproduction (bonus)
   6a. Write report/evidence/heh_plus_vqe.py (same pattern, He + H, charge=1).
   6b. Run.  -> 5/5 distances chemical-accurate.
   6c. Fix a numpy-bool -> JSON TypeError (wrap in bool()).

7. Marker/Nougat fallback extraction
   (Marker and Nougat not installed on host; no cached corpus copies.)
   7a. Prepend provenance banner; append `pdftotext -layout paper.pdf` to
       extraction/marker.md.
   7b. Same for extraction/nougat.mmd (without -layout, closer to Nougat's
       flat text output).

8. LLM-judge scoring (Argo, free)
   8a. First tried argo:claude-opus-4.7 via :44497 -> HTTP 502.
   8b. Switched to litellm aggregator :4000. Same Anthropic 502 pattern.
   8c. Called argo:gpt-5.2 and argo:gpt-5.4 - both returned JSON PARTIAL.
   8d. Dumped responses to report/evidence/llm_judge_argo_*.json.

9. Report authoring
   9a. report/REPORT.md
   9b. report/REPORT.tex
   9c. report/open_questions.json (5 non-generic Qs grounded in observed
       reproduction behavior)
   9d. report/workflow.md (this file)
   9e. report/artifacts_summary.md
   9f. report/failure_analysis.md
```

## Effort estimate

- Wall clock: ~25-30 min (see failure_analysis.md for line-item breakdown).
- Computational cost: a few CPU-seconds of PySCF FCI + ~90 s of statevector VQE (all on CherryRd CPU).
- Argo calls: 2 successful (gpt-5.2, gpt-5.4), 2-4 failed 502 (opus-4.7, opus-4.8 x2 attempts). No paid API touched.

## Data flow

```
Frontiers HTTPS -> work/paper.pdf (sha verified) -> paper.pdf (root artifact)
                                                 -> work/paper.txt (pdftotext skim)
                                                 -> extraction/marker.md, nougat.mmd
qiskit-nature + PySCF -> report/evidence/*.py -> report/evidence/*.json
report/evidence/*.json -> LLM judge prompt -> Argo -> report/evidence/llm_judge_*.json
all above -> report/REPORT.md, REPORT.tex, open_questions.json, artifacts_summary.md,
             workflow.md, failure_analysis.md
```
