# Paper Census — the standing way to count REPLICATE-PROJECT

**Problem this solves:** counting verdicts off a hand-edited snapshot CSV
(`RECONCILED_MASTER_2026-06-24.csv`) was fragile — duplicate rows, mis-extracted
paper_ids, and rows that drifted from what's actually on disk. The headline
number changed every time someone touched the CSV.

**The fix:** `scripts/census.py` treats the **report files on disk as ground
truth**, auto-ingests the 3-judge panel score CSVs as authoritative verdicts,
and prints a collection × verdict matrix + a GAPS section.

## Usage
```bash
cd ~/Dropbox/REPLICATE-PROJECT
python3 scripts/census.py                      # matrix + headline + gaps
python3 scripts/census.py --csv CENSUS.csv     # also dump per-paper census
```

## How it counts
1. Enumerates every paper directory under `LUCID-replications/`,
   `LUCID-second100/`, `PDE-replications/`, and the top level (OSTI-numbered,
   `BVBRC-*`, named one-offs). Skips infra dirs (`common`, `scoring`, `scripts`,
   `.git`, `_*ADMIN`, `_harvest`, …).
2. Finds the canonical report per dir (top-level `REPORT*.md` preferred, then
   `report/REPORT.md`, then largest `*.md`), skipping `*prereconcile*`,
   `*pass1*`, `*BACK_TO*`, `_superseded` siblings — this avoids the
   "two report files in one dir" double-count that inflated the old CSV.
3. Verdict precedence:
   - **panel** — a verdict from any `scoring/MASTER_SCORES_*3judge*.csv`
     (3-judge median/majority, ties→conservative; newest file wins). Authoritative.
   - **self** — the report's own `## Verdict` block (canonical token), used only
     when no panel verdict exists.
   - **(unscored)** — no extractable verdict; surfaced in GAPS.
4. Verdict labels normalized to the canonical ladder:
   `REPLICATED → PARTIAL → SPOT-CHECK → CONTRADICTED → NO-GO → BLOCKED → FAILED`
   (FULL/CONFIRMED/EXACT/MOSTLY→REPLICATED; DATA-BLOCKED→BLOCKED, etc.)

## Collections (note the real sizes)
- **LUCID-100** — the 100-paper radiobiology set (dirs ~108 incl. a few dupes/admin)
- **LUCID-second100** — the computational LUCID expansion set
- **PDE-100** — PDE/operator-learning replications
- **BVBRC-19** — the BV-BRC microbiology set is **19**, not 100 (don't call it BVBRC-100)
- **OTHER** — original 44-repo set + one-offs (NANOGrav, SOWFA, MSM, PVMol-Gen, Spears, Alter, …)

## Consistency policy
Per Rick's 2026-05-19 standing rule (reinforced 2026-06-23): **3-judge LLM panel
on free Argo endpoints, no regex/substring as the final scorer.** `census.py`
self-extraction is only a *fallback display* for papers not yet panel-scored; to
make a row authoritative, run the panel:
```bash
# put unscored dirs (relative paths) into SCORE_TARGETS_LIST.txt, then:
cd scoring && python3 score_unscored_3judge.py --concurrency 5 \
    --csv ../scoring/MASTER_SCORES_$(date +%F)_3judge.csv
```
census.py picks up the new CSV automatically on the next run.

## Known soft spots (as of 2026-06-25)
- A handful of mature projects (PVMol-Gen, MSM, perovskite) scored FAILED/NO-GO
  cov=0 because their substance lives in a **nested/PDF report** the scorer's
  text reader didn't pick the best file for — these are false-negatives to fix by
  pointing the panel at the right report path, not real failures.
- `RECONCILED_MASTER_2026-06-24.csv` still carries legacy duplicate rows; prefer
  `census.py` output over that CSV for any headline number.
