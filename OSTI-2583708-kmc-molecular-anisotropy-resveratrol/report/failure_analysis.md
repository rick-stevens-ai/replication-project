# Failure analysis

## What we could not reproduce, and why

### F1. `diffusion/disphere` app style + `resv` lattice style — the paper's own headline software claim
**What failed.** The paper Section 2.2 explicitly says the `resveratrol` branch of `tdjanic-snl/spparks` contains a new `diffusion/disphere` app style and a `resv` lattice style. Neither exists in the public branch as of the branch head `f6bcc3b` (2025-03-31).

Evidence (from `spparks-resv/src/lattice.cpp`):
```
39:  if (strcmp(arg[0],"none") == 0) style = NONE;
40:  else if (strcmp(arg[0],"line/2n") == 0) style = LINE_2N;
41:  else if (strcmp(arg[0],"sq/4n") == 0) style = SQ_4N;
42:  else if (strcmp(arg[0],"sq/8n") == 0) style = SQ_8N;
43:  else if (strcmp(arg[0],"tri") == 0) style = TRI;
44:  else if (strcmp(arg[0],"hcp") == 0) style = HCP;      ← the ONLY addition vs upstream
45:  else if (strcmp(arg[0],"sc/6n") == 0) style = SC_6N;
... no "resv" ...
```

And `grep -riIn "disphere\|resv\|bound.sphere" src/*.cpp src/*.h` returns zero matches.

**Root cause (best hypothesis).** The paper's Data Availability Statement uses future tense: "The data that support the findings of this study *will be* openly available following an embargo…" — i.e. an embargo period is in force and the disphere/resv extensions have not yet been pushed to the public fork. The publication is 2025-06-18, so if the embargo is 6–12 months this could still be in progress.

**Workaround.** None. We ran the infrastructure-only test (HCP + hex-region + 3D-random deposition) and used a surrogate isotropic Arrhenius ladder to establish an isotropic control. We did NOT attempt to independently reimplement the disphere logic (that would be a substantial engineering project — the paper only describes the algorithm at Table 1 level of detail, not code).

**Residual gap.** Claims C3, C4, C5, C6 of the paper cannot be independently verified from currently-public artifacts. Once the embargo lifts and the disphere/resv code + DFT ecoord tables are published, this replication can be extended in ~1 day of work.

### F2. IOP supplementary bundle — captcha-blocked
**What failed.** `curl` to the IOP suppdata URL returns 200 but with a Radware Bot Manager captcha HTML page (14 KB of anti-bot JS). Direct-CDN URL returns 403.

**Root cause.** IOP infrastructure aggressively bot-blocks automated fetches to their supplementary CDN.

**Workaround.** None automated. A human with a browser session could pull the bundle, but we did not have one in the replication loop. The paper's supplementary is said to contain: (a) representative FHI-aims input script, (b) SPPARKS input files, (c) tabulated binding energies (the 74-point DFT library that parametrizes claim C4).

**Residual gap.** Same as F1 — even if the disphere code were released, without the DFT ecoord tables we cannot reproduce the specific numerical morphology results of Section 3.2 and Figure 7. If a human can pull the supplementary bundle later, drop it into `work/supplementary/` and the KMC production run becomes reproducible in ~30 minutes.

### F3. `marker` / `nougat` binaries unavailable on uicgpu
**What failed.** `marker_single`, `marker`, and `nougat` are not installed on uicgpu; base env and `marlamr` conda env both empty. `pdf` MCP tool (which normally routes Anthropic-native PDF extraction) is also unavailable in this run (`credit balance too low`).

**Root cause.** These are heavyweight PyTorch-based extraction stacks (~5-10 GB each). Not pre-provisioned for this OSTI-set wave.

**Workaround.** Used `pdftotext -layout` (poppler 26.06.0) locally + IOPscience HTML fallback for table structure. Produced `extraction/marker.md` and `extraction/nougat.mmd` that preserve section/figure/table structure and equations transcribed in ASCII. Faithful for text, not character-exact for math.

**Residual gap.** Minor. Anyone re-running with marker/nougat installed will get slightly more polished math rendering but no substantive content changes. Note explicitly written into each extraction file.

## What we could reproduce cleanly

### R1. HCP lattice + hex region + 3D random deposition (infrastructure claim C1, C2)
- Builds clean with system mpicxx + g++ 12 + `-std=c++17 -O2` on uicgpu.
- `lattice hcp 1.0` + `region … hex …` → correct site count (2 basis × N_x × N_y × N_z), 12 neighbors per site, primitive-HCP box dimensions.
- 48×16×24 paper-scale box: 36,864 sites, box (56, 13.86, 39.19) with xy-tilt 8, matches expected HCP geometry.
- `deposition event 0.1 0.0 0.0 0.0 5.0 1 9` (3D random mode) accepts input, runs, and produces linear-in-time deposition acceptance count.
- 10 seeds × 2000 KMC-time-units × 48×16×24 completed in ~4 s wall each on 1 CPU thread.

## Aggregate honest assessment

- **Replication success on infrastructure claims: HIGH.** The `nonorth` additions (HCP + hex-region + 3D random dep) are exactly as described in the paper and work as documented.
- **Replication success on scientific claims: BLOCKED.** The core disphere/DFT-ecoord/aspect-ratio-match story is not testable from released artifacts. This is not a *contradiction* of the science — the paper's own Data Availability Statement admits an embargo — but it is a hard blocker for now.
- **Verdict-consistency check.** Our isotropic-ladder control gives W:L=0.53 (vs experimental ~0.35) and H:L=0.87 (vs experimental ~0.55) — both distinctly more isotropic than experiment. This is CONSISTENT with the paper's central claim (anisotropy needs the bound-sphere logic) but does NOT constitute a positive test of Figure 7.
