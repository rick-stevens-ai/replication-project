# Author Email Draft — Yuval & O'Gorman 2020 data request

**Status:** DRAFT — not sent. Rick reviews and sends manually.
**Drafted:** 2026-05-27

---

## Recipients

- **To:** Paul A. O'Gorman `<pog@mit.edu>`
- **Cc:** Janni Yuval `<janniy@mit.edu>`, Janni Yuval (personal/Google) `<yaniyuval@gmail.com>`
- **From:** Rick Stevens `<stevens@anl.gov>` (or your preferred address)

> **Verification note for Rick before sending:**
> - `pog@mit.edu` follows the standard MIT EAPS pattern; the paper PDF lists Paul O'Gorman as corresponding author at MIT. Quick verify: load `pog.mit.edu` in a browser (Cloudflare blocked our fetch) and confirm the contact email there.
> - `janniy@mit.edu` is the paper's listed email; `yaniyuval@gmail.com` is what Janni used on the OSF README. Janni is now at Google Research (per the O'Gorman group page and his active `yaniyuval/jax-gcm` GitHub repo). The Gmail address is the safer bet — MIT may have deactivated `janniy@mit.edu`. Consider Cc'ing only the Gmail.

---

## Subject

Subject: **Request: training/test data for Yuval & O'Gorman 2020 (Nat. Commun.) — replication study for a meta-paper on DL-for-science reproducibility**

---

## Body

Dear Paul (and Janni),

I hope this finds you well. I'm Rick Stevens at Argonne National Laboratory (Associate Lab Director for Computing, Environment and Life Sciences, and Professor at UChicago). I'm leading a small "replication friction" project — a forthcoming meta-paper on how easily independent groups can re-verify high-profile ML-for-science results from the last several years. Your 2020 *Nature Communications* paper, "Stable machine-learning parameterization of subgrid processes for climate modeling at a range of resolutions" (DOI 10.1038/s41467-020-17142-3), is one of about a dozen exemplars we're trying to reproduce end-to-end.

We've made good progress on the methodology side — your code archive on OSF is complete, well-commented, and the RF spec is unambiguous — but the **training and test data** referenced in the data-availability statement appear not to have been uploaded. Specifically:

- OSF node 36ypt (https://osf.io/36ypt/) currently contains only `README.txt` (last modified 2020-05-18), and the `test_data_x8/` and `snapshots_different_resolutions/` folders are empty. The README notes uploads were "delayed due to COVID-19," which understandably never resumed.
- The Google Drive folder linked from the README (`1TRPDL6JkcLjgTHJL9Ib_Z4XuPyvNVIyY`) exposes only a `readme.txt` to anonymous viewers; the `DATA3D` subfolders require explicit owner permission.
- Reconstructing the data ourselves would require running your MATLAB coarse-graining pipeline on the raw SAM aquaplanet output, which itself isn't publicly hosted and whose paths in `high_res_processing_code/main.m` are hardcoded to `/glade/scratch/` on Cheyenne.

If it's feasible on your end, **any of the following would unblock us**, in rough order of value:

1. **The processed train/test `.pkl` files** for the x4, x8, x16, and x32 coarse-graining factors as used in the paper's Figure 2 / Table-level R² results. These are presumably what was originally intended for `test_data_x8/` and the analogous folders for the other resolutions. If only one resolution is convenient, **x8 (the headline 96-km RF)** is plenty.
2. **The trained RF estimator pickles** (the `.pkl` outputs of the training script), so we can at least reproduce the offline R² and the snapshot prediction figures even if we can't re-train.
3. **A runnable bundle of the raw SAM aquaplanet output + your MATLAB preprocessing scripts** with paths adapted off `/glade/scratch/`. This is heavier (presumably tens of GB), but it would let us reproduce end-to-end. Argonne can host a transfer endpoint (Globus, S3, or a temporary scp staging area) if useful.
4. Alternatively, if you'd prefer to grant access to the existing Google Drive `DATA3D` folder, my Google account is `<rick's preferred gmail>`.

I'd be glad to share what we find back with you — both the reproduced numbers and any documentation gaps we hit — well before we publish. Our intent with the meta-paper is constructive: identifying patterns that make ML-for-science results easier or harder to verify independently, not to call out any individual paper. Your 2020 paper is one of the **good examples** in our sample on the code side; the data gap is squarely on the COVID-era infrastructure failures we want to characterize, not on you.

A couple of clarifying questions in case the data is hard to recover but you can answer them quickly:

- Do you happen to know whether the original `.pkl` files still exist on a Cheyenne, Engaging, or MIT-archived disk somewhere? Even a "no, they're gone" is useful for our methods section.
- Has anyone else asked for them since 2020 — i.e., is this a one-off request or a recurring one we should help solve systemically (e.g., a Zenodo deposit)?

No rush, and no pressure if the data is truly gone — we'll document that outcome honestly. Thank you for the careful methods write-up in the original paper; it made the reconnaissance straightforward even where the artifacts were missing.

With thanks,
Rick Stevens
Argonne National Laboratory · University of Chicago
stevens@anl.gov

---

## Sender notes (NOT for inclusion in email)

- **Tone calibration:** Polite, specific, non-accusatory. Frames the gap as "COVID-era infrastructure" rather than author negligence. Offers concrete reciprocity (sharing findings back, hosting transfer).
- **Ask hierarchy:** Cheapest ask (the pkl files) first; heaviest ask (raw SAM + MATLAB) last. Most authors will pick whichever is easiest for them.
- **Escape valves built in:** Two clarifying questions at the end give O'Gorman a way to respond helpfully even if the data is truly gone.
- **Rick's Argonne credentials:** Mentioned briefly to establish standing but not overplayed.
- **Don't mention:** the in-progress Wang/Yuval/O'Gorman 2022 path B work — keep this email focused. If O'Gorman responds positively about data, Wang 2022 becomes irrelevant. If he says it's gone, we have a clean "tried in good faith" record for the meta-paper.
- **Verify before send:**
  - The Gmail vs. MIT address for Janni (Gmail safer).
  - That `pog@mit.edu` is current (load `pog.mit.edu` in a browser — Cloudflare blocked our fetch from this session).
  - Whether you want to use `<rick's preferred gmail>` for Google Drive sharing or omit that option.
- **Suggested follow-up cadence:** If no response in ~2 weeks, a single short bump email is reasonable. After that, accept silence as the answer.
