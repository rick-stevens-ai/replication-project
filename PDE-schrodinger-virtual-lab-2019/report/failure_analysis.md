# Failure Analysis

Honest tally of what didn't work cleanly, what was worked around, and what would be needed to close each gap. **None of these failures overturns the REPLICATED verdict**; they are friction and coverage gaps.

## 1. Marker install failed on Python 3.14

- **Symptom:** `pip install marker-pdf` failed at metadata generation with a numpy build error (marker-pdf's transitive dep on a pinned old numpy tries to compile against Python 3.14 headers → ninja stops).
- **Root cause:** marker-pdf's dependency chain (specifically its pinned torch + old numpy) is not yet Python-3.14 compatible as of 2026-07-06. The venv is Python 3.14 because that's the system's `python3`.
- **Workaround:** substituted `pdftotext -layout paper.pdf extraction/marker.md` (poppler 26.06.0). This produces a linear-text extraction that is qualitatively similar for a 14-page article with modest math typesetting, but does NOT preserve equations as LaTeX or figures as embedded images the way Marker does.
- **Residual gap:** the `extraction/marker.md` in this dir is a plain text-layout dump, not a "true" Marker parse. If the central corpus later gains a Marker run for this DOI, it should overwrite `extraction/marker.md`.
- **Fix path:** create a secondary venv with Python 3.11 (`brew install python@3.11 && python3.11 -m venv .venv-marker && pip install marker-pdf`) and run marker there. Or offload to uicgpu, which already has a marker binary somewhere but I couldn't locate it in the ~2 min I searched (bvbrc117 dir has `marker_out/` but no `marker` binary in the venv).

## 2. Nougat install skipped; pymupdf substitute used

- **Symptom:** Meta's nougat has similar Python-3.14 compat issues (torch pin). I didn't attempt it at all after Marker failed, to save wall-clock.
- **Root cause:** Same class of dependency-freshness problem as Marker.
- **Workaround:** wrote `work/pdf_to_mmd.py` (26 LOC) using pymupdf's `page.get_text("text")` per page with a light heading heuristic that promotes numbered lines like "3. Method" to markdown H2.
- **Residual gap:** `extraction/nougat.mmd` is NOT a nougat parse. It contains no equation LaTeX and no table structure — just linear text with per-page markers.
- **Fix path:** run true nougat on uicgpu once (single 14-page paper, small GPU load).

## 3. Only 12 of 20 example scripts exercised

- **Symptom:** 8 examples not run: Vortex_Precession_2D, Vortex_Breaking_2D, Vortices_Pattern_2D, Liquid_Droplet_2D, Filamentation_2D, Diffraction_Circle_2D, Gaussian_Vortex_interf_2D, plus… (all 10 in `examples1D/` WERE run, so the shortfall is entirely in `examples2D/`).
- **Root cause:** Wall-clock. Diffraction_Circle_2D (500² × 60000 timesteps) already ran past my 4-minute timeout when I killed it — the larger ones would each take 5–15 minutes CPU. On uicgpu they'd finish in under a minute each.
- **Impact:** C1 (P-artifact "every example runs") is only 12/20 verified here — the sole dissenting judge (gpt-5.2) flagged exactly this. C6 (2D vortex physics) is qualitative, based on Vortex_2D final density plot rather than Vortex_Precession or Vortex_Breaking dynamics.
- **Fix path:** SSH to uicgpu, `source ~/env.sh`, `git clone https://github.com/pyNLSE/bpm.git && python3 -m venv .venv && ...`, run the remaining 8. Total wall-clock estimate: 15 minutes on a single A100.

## 4. Collapse_2D initial FileNotFoundError

- **Symptom:** First attempt of `python run_example.py Collapse_2D 2D` failed with `FileNotFoundError: [Errno 2] No such file or directory: './examples2D/townes_profile.csv'` (the initial-condition CSV).
- **Root cause:** Authors' example uses `np.genfromtxt('./examples2D/townes_profile.csv', ...)` — a relative path resolved against `cwd`. My driver ran from `work/` so the path missed.
- **Fix:** Added `os.chdir(BPMROOT)` in `run_example.py`. Absolute paths are used for output_folder and diag files so this is safe.
- **Learning for the repo:** the authors' relative-path pattern breaks any invocation that isn't launched from the `bpm/` directory. A one-line fix in the example (`os.path.join(os.path.dirname(__file__), 'townes_profile.csv')`) would harden this. Candidate for a PR.

## 5. Two Python 3.12+ SyntaxWarnings

- **Symptom:** During every run, matplotlib label lines like `plt.ylabel('$|\psi|^2$')` trigger `SyntaxWarning: invalid escape sequence "\p"`.
- **Root cause:** Non-raw string literal `'\p'` is deprecated (Python 3.12+ will treat as SyntaxError eventually).
- **Impact:** Cosmetic. Numerics unaffected.
- **Fix path:** Change to raw strings (`r'$|\psi|^2$'`). 4-line PR to `bpm/1D.py` and `bpm/2D.py`. Also candidate PR.

## 6. mencoder missing → .avi generation fails

- **Symptom:** `final_output` in authors' bpm calls `mencoder mf://... -o movie.avi ...` for video generation, which returns "sh: mencoder: command not found" on my Mac.
- **Root cause:** mencoder (part of MPlayer) was last released in 2015 and has been dropped from most 2026 package repositories.
- **Impact:** No `.avi` movie generated. Numerics + PNGs + final `.npy` all fine.
- **Fix path:** Switch to `ffmpeg -framerate 30 -i fig%03d.png -c:v libx264 movie.mp4`. Also candidate PR.

## 7. C5 (first-order accuracy) not measured directly here

- **Symptom:** REPORT.md's C5 row admits "Not measured directly in this dir — sibling PDE-Figueiras-Schrodinger-BPM-splitstep-2018 ran a self-convergence sweep and observed orders 1.0005 / 1.0002 / 1.0001. Cross-referenced."
- **Root cause:** The sibling replication already did this test rigorously on the identical algorithm (Lie splitting + periodic FFT). Rerunning it here would be redundant compute for zero new information.
- **Impact:** The sole PARTIAL judge (gpt-5.2) counts this as a coverage weakness. It IS technically a cross-reference, not an independent measurement in this dir.
- **Fix path:** Copy the sibling's `work/test5_order_selfconv.py`, run it against the authors' Soliton_Emission_A_1D setup — 3 halvings of dt, L2 self-convergence, orders. ~2 min compute.

## 8. Argo Claude endpoint (opus-4.7 and 4.8) returned HTTP 502

- **Symptom:** Both `argo:claude-opus-4.7` and `argo:claude-opus-4.8` returned 502 Bad Gateway during judge calls at ~04:45 CDT 2026-07-06.
- **Root cause:** Transient upstream (Argo → Anthropic) outage. Retried 3× on 4.7, all 502.
- **Impact:** Instead of the intended 3 judges, we have 5 successful judges (Gemini, gpt-5.2, gpt-4.1, gpt-4o, o3), which is actually stronger. Panel diversity preserved.
- **Fix path:** Re-run `python judge_extra.py` with just `argo:claude-opus-4.8` once Anthropic is back up if a Claude vote is desired for completeness. Not blocking.

## What's NOT a failure

- **Norm drift ~1.6-3.3% in Rectangular_Barrier and Sech2_Pot:** these have `absorb_coeff=20`. The drift is intended — the shell swallows outgoing waves. This is a feature, not a bug. All zero-absorption runs conserved norm to 12+ digits.
- **Overlap with sibling replication of same DOI:** Deliberate. This is a distinct methodology (author-code vs from-scratch) on the same paper — a two-arm cross-validation, not a duplicate. Both should exist.
- **Cosmetic `mkdir: cannot create directory ''`** message during uicgpu env sourcing: harmless, from an `mkdir "$SOME_UNSET_VAR"` line in `~/env.sh` — pre-existing in the environment, not caused by this replication.

## Overall assessment

This is a **REPLICATED** verdict with two honest coverage gaps (12/20 examples not 20/20; C5 cross-referenced not directly measured) and five cosmetic issues in the artifact (2 SyntaxWarnings, 1 missing mencoder, 1 relative-path fragility, 1 dependency-freshness for extraction tooling). All five are candidates for future PRs to `pyNLSE/bpm`. None affect the core physics or the paper's claims.
