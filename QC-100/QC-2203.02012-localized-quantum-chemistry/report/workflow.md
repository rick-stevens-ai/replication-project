# Workflow — arXiv:2203.02012 replication

Exact reproduction workflow. All commands were run on CherryRd (macOS, Python 3.11.15) on 2026-07-03. Statevector simulation, laptop CPU, total wall time ~2 minutes.

## 0. Prereqs

- macOS or Linux, Python 3.11.
- ~500 MB free disk for the venv (PySCF + Qiskit + numpy/scipy).
- No GPU, no quantum-hardware account required.

## 1. Get the source tree

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2203.02012-localized-quantum-chemistry
ls
# expect: code/ report/ logs/ work/ (paper PDF + txt) extraction/
```

## 2. Build the virtualenv

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pyscf "qiskit==1.4.*" "qiskit-nature==0.7.*" "qiskit-algorithms==0.3.*"
```

Confirmed pinned versions: `pyscf==2.13.1`, `qiskit==1.4.6`, `qiskit-nature==0.7.2`, `qiskit-algorithms==0.3.1`.

## 3. Run the three scripts

```bash
# (a) STO-3G VQE-UCCSD on (H2)2 in canonical + Boys-localized MO bases, 3 geometries
python code/replicate_las_vqe.py        # -> report/evidence/results.json,  logs/run2.log

# (b) 6-31G CASCI + fragment-product surrogate on (H2)2, 5 geometries (the paper's basis)
python code/las_631g.py                 # -> report/evidence/las_6-31g.json, logs/las_631g.log

# (c) STO-3G fragment-product cross-check
python code/las_fragment_product.py     # -> report/evidence/las_fragment_product.json, logs/las_frag.log
```

Each script prints per-geometry energies and error vs the reference.

## 4. Sanity-check the results

Open `report/evidence/las_6-31g.json` and verify:

- `E_CASCI` at `r_inter = 1.5 A` ≈ `-2.257368 Ha`.
- `E_LAS_prod` at `r_inter = 0.6 A` differs from `E_CASCI` by > 4 mHa (breaks chemical accuracy — reproduces Fig.~3 breakdown).
- `E_LAS_prod` at `r_inter = 5.0 A` matches `E_CASCI` to < 0.01 mHa (fragments truly non-interacting).

Open `report/evidence/results.json` and verify:

- For all 3 geometries and both MO bases, `abs(E_VQE - E_FCI) < 0.05` mHa. (Actual worst-case: 0.031 mHa.)

## 5. Regenerate the report

The Markdown report `report/REPORT.md` is the primary source. The LaTeX report `report/REPORT.tex` is a companion with the critique and verdict.

```bash
# Optional: compile the LaTeX
pdflatex -output-directory=report report/REPORT.tex
```

## 6. Extend (optional next steps)

See `report/open_questions.json` for five concrete extension experiments, each CPU-feasible with the same venv (plus `qiskit-aer` for the noise study and `block2` for the DMRG baseline).

## 7. What is deliberately NOT in this workflow

- The paper's **LAS-QPE** fragmented-state-preparation circuit (requires the authors' `mrh` package + a custom fragmented-QPE circuit builder). We substituted VQE-UCCSD on the joint active space, which reaches the same CASCI limit from below but does not exercise the fragmented-QPE prep.
- The paper's **trans-butadiene / CAS(8,8)** benchmark (16 qubits, deep UCCSD, not attempted in this replication).
- The paper's **resource-count scaling** figure (Fig.~5) — this is an analytical/counting exercise, not a runnable simulation.

## 8. Bill of materials

| Artifact | Path | Size / role |
|---|---|---|
| Paper PDF | `work/paper.pdf` | source paper |
| Paper text | `work/paper.txt` | pdftotext extract |
| Nougat MMD stub | `extraction/nougat.mmd` | placeholder — not run on this paper |
| Replication scripts | `code/*.py` | reproducible pipeline |
| Result JSONs | `report/evidence/*.json` | machine-readable numbers |
| Logs | `logs/*.log` | full stdout of every run |
| Reports | `report/REPORT.md`, `report/REPORT.tex` | human-readable |
| Critique + failure analysis | `report/failure_analysis.md` | limits + risks |
| Open questions | `report/open_questions.json`, `report/open_questions_section.tex` | 5 concrete follow-ups |
| Artifact inventory | `report/artifacts_summary.md` | file-by-file summary |
| This workflow | `report/workflow.md` | how to rerun end to end |
