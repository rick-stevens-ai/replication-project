# PARSER PROVENANCE — GLOBLE re-pass (2026-06-23)

Target paper: Herr L, Friedrich T, Durante M, Scholz M (2014). *A Model of Photon Cell Killing Based on the Spatio-Temporal Clustering of DNA Damage in Higher Order Chromatin Structures.* PLoS ONE 9(1): e83923. DOI: 10.1371/journal.pone.0083923.

## Canonical Marker/Nougat output

- Checked: `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/`
- Result: **NOT PRESENT** for DOI 10.1371/journal.pone.0083923.
  - Confirmed by directory listing (`ls | grep -iE "0083923|herr"`) returning empty.
  - Confirmed by content scan for the title `Spatio-Temporal Clustering of DNA Damage`: only papers that **cite** Herr 2014 were found, not Herr 2014 itself.
- Action: fell back to pre-existing parsed markdown copy in repo (`paper.md`, sourced from `/data/stevens/lucid-corpus-extracted/LUCID-papers/30afbb7d84f54d5d.md` on uicgpu during pass 1).

## Primary parser used (this re-pass): pre-existing `paper.md`

- Path: `paper.md` (this repo)
- SHA / MD5: `cb54cfea58b7e35f222e5ea942e032c0`
- Size: 90,621 bytes / 540 lines
- Provenance: copied during pass 1 from a prior uicgpu Marker/Nougat-style extraction of the PLOS ONE PDF.
- Verified content present:
  - Table 1 (cell-line dataset + source list)
  - Table 2 (17 cell-line GLOBLE parameters, dose-rate + split-dose fits)
  - Table 3 (HLT_i comparison between GLOBLE and IR/LPL models)
  - All five GLOBLE ODE equations (Eqs. 13–17), survival expression (Eq. 18),
    Lea-Catcheside factor (Eqs. 40–41), low-dose-rate closed form (Eq. 38)
  - Figures 2 (dose rate, RT112+MT), 3 (MT split dose), 4 (LQ vs GLOBLE),
    5 (deterministic effects), 6 (LL split-dose prediction).
- Cross-check parser: `pdftotext -layout artifacts/paper.pdf` produced
  `/tmp/herr2014_pdftotext.txt` (MD5 `7595c7482330b346e91311d316e1afd4`,
  1,048 lines). Verified all numerical values used by the re-pass code
  (Table 2, Table 3, RT112/MT dose-rate panels, HX138/HX142 dose-rate panels)
  agree between `paper.md` and the pdftotext output. No transcription
  discrepancies were detected.

## Source PDF

- Path: `artifacts/paper.pdf`
- MD5: `4b7d8f781555b400a191c12d7f4c3cc2`
- Size: 1,393,551 bytes

## Why not switch to a re-parsed Marker run

The canonical uicgpu Marker merge (2026-06-22) does not include this DOI. The
pre-existing `paper.md` is itself a Marker/Nougat-style markdown extract of the
same PLOS ONE source; spot-checking against `pdftotext -layout` shows no
material discrepancies for the numbers, equations, and table values used by the
replication. Re-running Marker locally would not change the values used.
