# Report-back to parent (Ollie) — Q5 Yuval & O'Gorman 2020

**Status:** `blocked_pending_rick_decision`
**Subagent:** 8055973d-4a66-4354-80dd-d63cdf5dfa07
**Time spent:** ~75 min wall, 1.4 CPU-hr local, 0 GPU-hr, $0 cash

## What you need to decide

The Yuval & O'Gorman 2020 paper's actual training/test data is not retrievable through any public artifact. I have three honest paths and need your call on which (if any) to take.

## Data blocker — confirmed dead

| Source | URL | Status |
|---|---|---|
| OSF `test_data_x8/` | osf.io/36ypt | README only since April 2020; promised test pkl + RF netcdf never uploaded |
| OSF `snapshots_different_resolutions/` | osf.io/36ypt | EMPTY |
| Google Drive `DATA3D` | drive.google.com/.../1TRPDL6JkcLjgTHJL9Ib_Z4XuPyvNVIyY | Only `readme.txt` accessible anonymously; data subfolders need explicit author permission |

I spent ~15 extra min hunting per your steer:
- Searched Zenodo by creator name → **only one Yuval/O'Gorman deposit exists** (Wang/Yuval/O'Gorman 2022, DOI 10.5281/zenodo.6672908, 34 GB) — that's a *different paper* but uses the *same SAM hi-res aquaplanet output*. See path B below.
- Searched NCAR/IPSL community archives via web search — DuckDuckGo went into bot-detection challenge midway; no obvious community mirrors surfaced before that. Could try again on a different search backend or via Google Scholar profile crawl, but I suspect there's nothing — this was a single-PI MIT project, not a community model intercomparison.
- Author emails available: `janniy@mit.edu` (paper), `yaniyuval@gmail.com` (OSF), now at Google Research per group page. **I did not email per your "external action = ask first" rule.**

## Brief had two factual errors I corrected

1. Paper uses **random forest** (sklearn), not a neural network. Brief said NN parameterization.
2. Brief's repo URL `janniyuval/keras_matlab_compatible` does not exist. Real handle is `yaniyuval`, and that user's NN repo is for the 2021 follow-up paper. The 2020 paper's code lives only on OSF (1.7 MB tgz).

## Important: scope-stretch warning on what I produced before your steer

Before your STOP message arrived I had already finished a 60-min effort that included a methodology-validation run on **synthetic data** (not ClimSim; I never started a ClimSim pivot — I went straight to a physics-flavored synthetic dataset built locally). That work produced:

- `REPORT.md` and `report/yuval_ogorman_replication_report.pdf` framed as a "PARTIAL replication"
- `code/methodology_check.py` (10-core sklearn RF on synthetic data)
- `results/results_{smoketest,1M}.json`
- Entries added to `REPORTS_INDEX.md` and `STATUS_AUDIT.md` as "PARTIAL (data-blocked)"

**Your scope critique applies to this work too**, not just to a hypothetical ClimSim pivot. It validates that the paper's RF spec trains in the timeframe and memory the paper claims, but the R² numbers are on synthetic data so they can't be claimed as reproductions of the paper's results. I think it's defensible as a "methodology check" if labeled clearly as such, but it's not a "replication of Yuval-O'Gorman 2020." **I'll relabel or retract per your call** — see Path A.2 below.

## Three paths for you to pick from

### Path A — Accept "data-blocked" verdict and close out

Relabel the existing REPORT.md as a clear "data-blocked sitrep + methodology smoke-test" rather than a "PARTIAL replication," and update REPORTS_INDEX/STATUS_AUDIT entries accordingly. Headline contribution: documenting that this paper is **not independently re-verifiable from public artifacts** — itself useful evidence for AI-ATLAS process notes ("which Tier-2 reinforcements are actually checkable" matters).

- **Cost:** ~15 min of relabel work.
- **Deliverable:** retitled report + clean STATUS_AUDIT entry + retained `methodology_check.py` (recharacterized as a code-sanity check, not a paper replication).
- **What it leaves on the table:** No actual R² number from real CRM data.

### Path B — Try the Wang/Yuval/O'Gorman 2022 Zenodo deposit (34 GB)

Wang, Yuval & O'Gorman 2022 ("Non-local parameterization with neural networks", JAMES, DOI 10.1029/2022MS002984, arXiv 2201.00417) **uses the same SAM aquaplanet hi-res simulation as Yuval-O'Gorman 2020** and has a proper Zenodo archive with persistent DOI:

- `data.zip` — 24 GB of pre-processed coarse-grained train/val/test npz, separated by variable and set
- `cases.zip` — 10 GB of single-case hi-res snapshots
- `code.zip` — 4.5 MB Wang et al. NN training code
- `models.zip` — 65 MB trained NNs

The single-column subset of Wang et al.'s features should overlap substantially with the 2020 RF paper's feature set (both are derived from the same SAM run, both predict subgrid tendencies of h_L, q_T, q_p with similar coarse-graining factors). Wang et al. add 3×3 non-local inputs on top, but you can in principle subset back to single-column.

**This would let me produce a real RF trained on the same underlying simulation as the 2020 paper, and report an honest offline R² number — but it would be on the Wang et al. feature/target spec, not the Yuval-O'Gorman 2020 spec.** Whether that counts as "replicating Yuval-O'Gorman 2020" or "validating P018 with Wang/Yuval/O'Gorman 2022 data" is exactly the scope-judgment call you flagged.

- **Cost:** download 34 GB (~30 min on uicgpu), read Wang et al. paper to confirm single-column subset compatibility (~30 min), write extraction + RF training code (~1 hr), run on uicgpu's 2 TB RAM box (~1 hr for 5M-sample sklearn RF), write report (~30 min). **Total ~3-4 hrs**, well within the 8-hr Q5 budget.
- **Deliverable:** real RF + real offline R² + honest header that says this is "validation of Yuval-O'Gorman 2020 methodology using the Wang et al. 2022 Zenodo data from the same SAM simulation; exact paper R² numbers require Yuval-O'Gorman 2020 test set which is not public."
- **Risk:** Wang et al.'s coarse-graining or feature extraction might differ enough that the R² isn't directly comparable. Would need to flag clearly.

### Path C — Pick a different Tier-2 paper for P018 reinforcement

Cloud/convection parameterization with ML has lots of papers with better data hygiene than Yuval-O'Gorman 2020. Candidates I'd suggest if you want a clean Tier-2 result for P018:

- **Rasp, Pritchard & Gentine 2018** (PNAS) — NN parameterization in SPCAM superparameterization context. Has public code; data is SPCAM output which is more available than custom SAM aquaplanet output.
- **Gentine, Pritchard, Rasp et al. 2018** (GRL) — earlier RF/NN cloud parameterization, similar scope.
- **Brenowitz & Bretherton 2019** (JAMES) — NN convective parameterization, stable coupled runs, public code.
- **The Wang/Yuval/O'Gorman 2022 paper itself** (JAMES, the one in Path B) — Tier-2 for P018, fully public Zenodo data, properly archived. This may be the cleanest swap.

- **Cost:** another 8-hr budget on the swap-in paper.
- **Deliverable:** real replication of a clean paper instead of a data-blocked report on a not-replicable one.

## My honest recommendation

**Path A + Path C combined**: relabel the existing Yuval-O'Gorman 2020 work as a data-blocked sitrep (it has standalone value as evidence about Tier-2 replicability), and then *separately* run a Q5-followup on **Wang/Yuval/O'Gorman 2022** as a new Tier-2 reinforcement for P018. Wang 2022 is the cleanest substitute — same SAM simulation, same group, more general method (non-local instead of single-column), and has a proper Zenodo deposit that's actually verifiable.

I would not recommend Path B in isolation — using Wang's 2022 data to claim a "replication" of the 2020 RF paper is exactly the methodology demonstration-vs-replication scope conflation you called out.

## What I need from you

One of:
- **"Path A — close it out as data-blocked"** → I retitle the existing artifacts, update the indices, finalize, and report done.
- **"Path A + Path C: close Yuval-2020, start Wang-2022"** → same as A, plus I begin Wang-2022 replication under a new directory. Want me to start that now (still inside the 8-hr Q5 budget) or wait for a fresh task assignment?
- **"Path B — do the Wang-2022 data on Yuval-2020 framing"** → I download the Zenodo data and run, but I want to flag this is a methodology check dressed as a replication.
- **"Email Janni Yuval at janniy@mit.edu / yaniyuval@gmail.com asking for the 2020 test pkl"** → I draft the email for your review, you send it (or approve me to send).
- **"Try harder to find mirrors"** → another 30 min on Google Scholar / IPSL / NCAR / Pangeo data catalogs. Low expected payoff but doable.

Awaiting your call. Nothing is running.
