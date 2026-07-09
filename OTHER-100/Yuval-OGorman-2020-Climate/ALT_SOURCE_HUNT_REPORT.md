# Alt-Source Hunt Report — Yuval & O'Gorman 2020 (Slot E)

**Subagent:** 296efd9d-6be1-4835-ac49-c852e8ea70bf
**Date:** 2026-05-27
**Wall time:** ~25 min
**Outcome:** **C — Definitively unrecoverable** from public artifacts; only viable path is author contact.

---

## TL;DR

The Yuval & O'Gorman 2020 Nature Communications paper's training/test data is **not retrievable from any public source** as of 2026-05-27. The paper's own data-availability statement names only OSF as the canonical host, and OSF has had zero file activity since 2020-05-18 — uploads stopped right around publication and never resumed. No mirror exists on Zenodo, Pangeo, GitHub, NCAR/ESGF, IPSL, NSF PAR, or anywhere else our reconnaissance touched. The follow-up papers (Yuval-O'Gorman 2021, Wang-Yuval-O'Gorman 2022) point back to the **same** Google Drive folder, which still requires explicit author permission for data access.

**Recommended next action:** Send the email at `AUTHOR_EMAIL_DRAFT.md`. If no useful response in ~2 weeks, finalize the PARTIAL/data-blocked verdict and (separately) use Wang-Yuval-O'Gorman 2022 (Zenodo DOI 10.5281/zenodo.6672908) as the P018 reinforcement under Slot F or a new slot.

---

## What was checked in this round

This hunt extends the prior subagent's reconnaissance (`REPORT_BACK_TO_OLLIE.md`). New checks performed here:

| Source | Method | Result |
|---|---|---|
| **OSF node 36ypt** | Direct API: `api.osf.io/v2/nodes/36ypt/files/osfstorage/` | Only `README.txt` (2.9 KB, last modified **2020-05-18T23:57Z**, downloads=31). `test_data_x8/` and `snapshots_different_resolutions/` folders still empty. |
| **OSF activity log** | `api.osf.io/v2/nodes/36ypt/logs/` | **Zero activity since 2020-05-18.** Last 10 actions all from Apr-May 2020 (file uploads + wiki edits). No comments ever posted on the project. |
| **Zenodo (Yuval+O'Gorman)** | `zenodo.org/api/records?q=Yuval+O'Gorman` (704 hits, scanned all relevant) | **Only one deposit** matches: Wang/Yuval/O'Gorman 2022 (DOI 10.5281/zenodo.6672908, 34 GB) — confirms no separate 2020 deposit was ever made. |
| **Zenodo (hypohydrostatic aquaplanet)** | Topic search (51 hits) | None match the Yuval-O'Gorman SAM 4-km hi-res config. |
| **GitHub code search** | `hypohydrostatic aquaplanet yuval` | Single hit: `tbeucler/HybridESM` README, which is a literature index that *cites* the paper but hosts no data. |
| **GitHub repo search** | `aquaplanet random forest parameterization` | Zero hits. |
| **yaniyuval (Janni) GitHub** | Full repo list | Two relevant repos: `Neural_nework_parameterization` (2021 follow-up paper code; points to the same Google Drive for raw data) and `jax-gcm` (active May 2026, Janni's current Google Research work — unrelated to 2020 SAM data). |
| **Yuval-O'Gorman 2021 repo README** | Direct fetch | Same Google Drive folder `1TRPDL6JkcLjgTHJL9Ib_Z4XuPyvNVIyY` cited — same access barrier. |
| **Nature paper data availability** | PDF extraction | Verbatim: "RF estimators and snapshots for different resolutions are available at osf.io (https://doi.org/10.17605/OSF.IO/36YPT). Additional data that support the findings of this study are available from the corresponding author upon request." **No secondary mirror by design.** |
| **O'Gorman MIT group page** | `pog.mit.edu` | Cloudflare blocked our fetch — needs manual verification before sending email. |
| **Pangeo Discourse** | Search for "Yuval O'Gorman" | No relevant threads (JS-rendered search returned no extractable hits). |

## What the prior subagent already confirmed (not re-checked)

- OSF folders empty since 2020-05-18 ✓ (re-confirmed this round).
- Google Drive `DATA3D` requires explicit author permission ✓.
- MATLAB pipeline hardcoded to `/glade/scratch/` Cheyenne paths ✓.
- Brief's `janniyuval/keras_matlab_compatible` repo doesn't exist; real handle is `yaniyuval` ✓.
- Wang-Yuval-O'Gorman 2022 Zenodo deposit (10.5281/zenodo.6672908) exists with 34 GB of similar-but-not-identical SAM-derived data.

## Why this is definitive

The paper's data-availability statement designates OSF as the **sole** public canonical archive. The OSF project has had no file or comment activity in over five years. The corresponding-author Google Drive is intentionally permissioned. There is no community redistribution because:

- This was a single-PI MIT project (O'Gorman group), not a community MIP.
- The raw SAM aquaplanet simulation used a custom hypohydrostatic configuration not present in standard archives (ESGF/CMIP6, NCAR data catalogs, Pangeo).
- The 2021 and 2022 follow-up papers from the same group reuse the same simulation and the same Google Drive — so the entire data chain has a single human gatekeeper (Paul O'Gorman / Janni Yuval).

The author-contact path is therefore not just *one* option — it is the **only remaining** option for genuine replication.

## Recommendation

1. **Send the email** at `AUTHOR_EMAIL_DRAFT.md`. Verify the two contact-address questions in that file's "Sender notes" section before sending.
2. **In parallel, do not block on it.** Treat the 2020 paper as PARTIAL/data-blocked in `REPORTS_INDEX.md` and proceed with:
   - **Slot F (Rasp 2018)** as the primary P018 reinforcement (per the brief).
   - Optionally, **Wang-Yuval-O'Gorman 2022** (clean Zenodo deposit, same group, same SAM simulation, more general method) as a secondary P018 reinforcement — this is the strongest substitute if a response from O'Gorman is slow or negative.
3. **If O'Gorman responds positively** within ~2 weeks: spawn a Q5-retry subagent with the recovered data; the prior subagent already wrote a working `methodology_check.py` that can be adapted to consume the real `.pkl` files with minor changes.
4. **If O'Gorman doesn't respond** or says the data is gone: keep the email exchange in `AUTHOR_EMAIL_DRAFT.md` (and reply chain) as **first-class evidence** for the replication-friction meta-paper. "Data unavailable five years post-publication despite single-PI archive intent and active follow-up work by the same group" is itself a meaningful finding.

## Files produced this round

- `AUTHOR_EMAIL_DRAFT.md` — polite, specific email to O'Gorman (cc Yuval) requesting any of four progressively heavier data deliverables. Includes sender notes for Rick on address verification and tone calibration.
- `ALT_SOURCE_HUNT_REPORT.md` — this file.
- `memory/subagent-progress/q5_yuval_ogorman.json` — updated with `status="alt_source_hunt_complete"`, `outcome="C"`.


## Verdict

**Verdict: BLOCKED**. — Training data unrecoverable from all public sources; only author contact viable, no replication run

<!-- census-verdict: BLOCKED assigned 2026-07-08 by LLM judge (Argo Opus) -->
