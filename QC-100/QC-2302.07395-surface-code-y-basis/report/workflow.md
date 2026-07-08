# Workflow — QC-2302.07395 (Inplace Surface-Code Y Basis)

## Provenance chain

1. **Paper acquisition** — `arxiv.org/pdf/2302.07395` (v2, 1 Apr 2024) fetched
   2026-07-03 into `work/paper.pdf` (SHA-256 pinned in run log).
2. **Zenodo artifact fetch** — record 7487893 (paper's own release):
   - `circuits.zip` (5.0 MB, ~500 `.stim` circuits at `d ∈ {3,5,7,9,11,13,15,17}`,
     bases `X, Z, Y, Y_folded, Y_braid`, padding rounds `rb ∈ {0..10}`).
   - `stats.csv` — paper's own logical-error-rate table for cross-check.
3. **Independent tool install** in isolated venv:
   `stim 1.16.0`, `sinter 1.16.0`, `pymatching 2.4.0`, `numpy 2.3.4`,
   Python 3.13.14 — every version **newer** than the paper's, no shared
   binaries.
4. **Circuit verification** (Experiment D) — parse REPEAT-block structure,
   count qubits, confirm `⌊d/2⌋+2` round envelope and `d×d` bounding box
   independently, without decoding.
5. **Cross-check LER sampling** (Experiment A) — sample each of X/Z/Y/Y_folded
   at `d∈{3,5,7}`, `p=0.001`; compare to `stats.csv`.
6. **Head-to-head inplace vs braid** (Experiment B) — sample Y and Y_braid at
   `d=9, rb=4, p=0.001`.
7. **Padding saturation sweep** (Experiment C) — sample Y at
   `d=5, rb∈{0,1,2,3,4,6,8,10}, p=0.001`.
8. **Verdict adjudication** — apply headline-exercised rule: all four claim
   families (structural, footprint, round-envelope, LER-matches-braid) tested
   on real simulations of paper's own circuits → REPLICATED.

## Compute + budget

- **Host:** CherryRd (single core, no GPU).
- **Wall time:** ~7 minutes total.
- **Endpoints:** zero paid, zero LLM calls, zero managed compute. Pure
  local numerical simulation on open-source `stim + pymatching`.
- **Sampling budget per cell:** up to 500k shots / 300 logical errors / 90–240 s
  wall (whichever first). All reported cells reached ≥125 logical errors →
  Poisson error bars < 10% of estimate.

## Decoder choice + known offset

- Paper uses Google's proprietary **correlated matching** decoder.
- We use **pymatching 2.4** (MWPM only). Paper's own README explicitly warns
  the pymatching result will be worse.
- Observed inflation ratio: `1.17× (d=3)`, `1.43–1.94× (d=5)`,
  `1.99–2.61× (d=7)`, growing smoothly with `d`.
- Critically: **ratio grows identically across X, Y, Z, Y_folded bases**.
  A Y-specific bug would show as X/Z-match + Y-diverge; we see uniform
  divergence → decoder gap, not construction bug.

## Files produced by this workflow

- `scripts/replicate.py` — driver script (~230 lines).
- `report/REPORT.md` — canonical prose report.
- `report/REPORT.tex` — LaTeX build.
- `report/evidence/expA_cross_check.json` — LER cross-check table.
- `report/evidence/expB_inplace_vs_braid.json` — d=9 head-to-head.
- `report/evidence/expC_padding_sweep.json` — padding sweep.
- `report/evidence/expD_structure.json` — round-count structure.
- `report/evidence/run_log.txt` — verbatim stdout.
- `work/paper.pdf`, `work/stats.csv`, `work/circuits/*.stim` — paper's
  own artifacts, redistributed under Zenodo CC-BY-4.0.

## Reproduction (fresh machine)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2302.07395-surface-code-y-basis
mkdir -p work && cd work
curl -sL https://arxiv.org/pdf/2302.07395 -o paper.pdf
curl -sL https://zenodo.org/api/records/7487893/files/stats.csv/content -o stats.csv
curl -sL https://zenodo.org/api/records/7487893/files/circuits.zip/content -o circuits.zip
unzip -q circuits.zip -d circuits/
python3.13 -m venv .venv && source .venv/bin/activate
pip install stim sinter pymatching numpy scipy
cd .. && python scripts/replicate.py | tee report/evidence/run_log.txt
```

Expected wall time ~7 min single-core, no network after step 1–4.
