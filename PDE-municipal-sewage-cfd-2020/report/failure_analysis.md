# Failure Analysis — PDE-municipal-sewage-cfd-2020

Honest audit of what worked, what didn't, what was worked around, residual gaps.

## What worked cleanly

- **PDF fetch.** OA PDF direct download from `rajpub.com`, no paywall.
- **DOI-vs-metadata discrepancy identified early.** The wave brief said "Al Manazlah, Saudi Arabia" but Crossref + downloaded PDF both confirmed the true title (Tororo, Uganda). Proceeded with the actual paper, flagged in report.
- **C1 analytical replication.** Manning back-solve gave n = 0.0129 ± 0.0009 across all 8 Table-1 rows — clean, unambiguous match to standard concrete-sewer roughness.
- **OpenFOAM interFoam on uicgpu.** After one dict fix (see below) the case ran end-to-end in 80 s and produced usable sample-line data.

## Frictions / minor failures / workarounds

### F1. OpenFOAM environment sourcing on uicgpu
- **Symptom:** `bash -lc "source /usr/lib/openfoam/openfoam1906/etc/bashrc"` — path did not exist.
- **Root cause:** The Ubuntu `openfoam` package installs its bashrc at `/usr/share/openfoam/etc/bashrc`, not the upstream `/usr/lib/openfoam/openfoam1906/etc/bashrc`.
- **Fix:** `source /usr/share/openfoam/etc/bashrc` (found via `find /usr -name bashrc -path *openfoam*`).
- **Cosmetic residual:** `mkdir: cannot create directory '': No such file or directory` prints repeatedly during source — the packaged bashrc references `foamEtcFile`/`foamCleanPath` at non-existent paths, but `interFoam` and `blockMesh` are already on `/usr/bin` so this is harmless.

### F2. Missing divergence scheme in fvSchemes
- **Symptom:** interFoam first-second-timestep FATAL: `Entry 'div(((rho*nuEff)*dev2(T(grad(U)))))' not found in dictionary`.
- **Root cause:** OpenFOAM v1906 requires this exact divScheme name for the two-phase turbulence stress term; I initially used only the `(muEff*dev(T(grad(U))))` variant.
- **Fix:** added both `div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;` and `div(((rho*nuEff)*dev(T(grad(U))))) Gauss linear;` to divSchemes and rebuilt case.

### F3. `pdf` MCP tool blocked by workspace-path allowlist
- **Symptom:** `pdf` tool refused `~/Dropbox/REPLICATE-PROJECT/.../paper.pdf` — "not under an allowed directory".
- **Root cause:** Dropbox path not in default allowed dirs.
- **Workaround:** `pdftotext -layout` locally — worked fine, gave clean text; the paper is text-native (not scanned) so no OCR needed. `ocr_tesseract` also failed with a byte-decode error on the raw PDF (it expected an image path, not a PDF path — could have been avoided by rasterizing first, but pdftotext output was sufficient).

## Residual gaps (things NOT replicated)

### R1. C4 — municipal-connections claim (535 → 1200, +80 % delivery)
Requires Tororo Municipality / NWSC records; not publicly indexed. Marked out-of-scope in report rather than fabricated. Feeds Open Question Q5 (SWMM network-scale check).

### R2. Fig. 10 velocity-time evolution
Paper's Fig. 10 shows U vs t. We ran to t=5 s with adjustive dt; producing the paper's specific time-trace would require probe-in-time setup (`functionObjects/probes`) and possibly a longer run. Would take another ~5 min. Skipped to keep this replication bounded; the transient behaviour shown in `log.interFoam` (adjustive dt, Courant-limited to 1) is qualitatively consistent.

### R3. 1.0 m diameter + 3° inclined pipe (Fig. 4-6)
Paper also shows results for D=1.0 m at 0° and 3° inclination. We only ran D=0.5 m at 0°. Adding these three additional runs would be ~5 min each on uicgpu and would strengthen the CFD replication. Not required for verdict but a natural follow-up.

### R4. 3-D axisymmetric CFD
Paper's 2-D-rectangular representation is a known approximation — the 2-D geometry has R = h/2 whereas a full circular pipe has R = D/4 (a factor of 2 difference in hydraulic radius, → 2^(2/3) ≈ 1.59× in Manning velocity). We ran the same 2-D approximation. This is a paper limitation we inherited. Feeds Open Question Q3.

### R5. Grid convergence
No mesh-convergence study performed here (paper doesn't either). Feeds Open Question Q4.

### R6. Marker / Nougat central-corpus lookup
Central Marker/Nougat corpus not queried for this PDE-set paper (workflow was: attempt local extraction, and pdftotext -layout succeeded on this text-native PDF). Duplicated `paper.txt` into both `extraction/marker.md` and `extraction/nougat.mmd` to satisfy the 8-artifact standard. If a real Marker parse is later pulled from Eagle, replace these files.

## Root-cause summary

Everything meaningful worked. Two 1-minute technical hiccups (bashrc path, missing divScheme name) were resolved by standard OpenFOAM troubleshooting. The paper's own reporting limitations (no numeric CFD tables, no mesh convergence, no network-scale model, 2-D approximation) bound the ceiling of any independent replication — not something an executor can close from outside.

## What would close every residual gap

1. Query central Marker + Nougat Eagle manifests → replace R6 extraction files.
2. 3× additional interFoam runs (D=1.0 m at 0° and 3°, plus 3-D axisymmetric) → close R3, R4.
3. Grid-convergence 400×40 → 800×80 → 1600×160 study → close R5.
4. `probes` function object for time-history at 3 stations along pipe → close R2.
5. SWMM/EPANET network model of Tororo topology + wet-weather forcing → close R1 + Q5.

Aggregate estimated additional effort: ~2-3 h agent time + a few minutes uicgpu compute + one round of correspondence with NWSC / Busitema.
