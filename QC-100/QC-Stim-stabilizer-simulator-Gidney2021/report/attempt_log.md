# Attempt log — Stim (Gidney 2021) — 2026-07-01

1. Read WAVE_BRIEF; inspected QC-100/ existing structure (siblings W1/W2/W3 use REPORT.md + replicate.py + results.json; BVBRC-17 uses report/ + work/). Created target subdir with report/{evidence} + work/.
2. Fetched arXiv abs + PDF (arxiv.org/pdf/2103.02202, 980 KB, v3). Confirmed headline: d=100 surface code (~20k qubits, ~8M gates, ~1M meas) analyze ~15 s, then ~1 kHz.
3. PDF vision-model path unavailable (Anthropic credit exhausted; gemini/gpt PDF disabled). Fell back to `pdftotext -layout` → 87 KB text; grepped out all quantitative + benchmark claims (Figs 1,5,6,7,8; complexity claims; comparison setup on i7-8650U laptop).
4. Defined 5 testable claims C1–C5. Built `replicate.py` (stim + pymatching API only).
5. Created venv; `pip install stim==1.16.0 pymatching==2.4.0 numpy==2.5.0` on Python 3.14.6.
6. C4 correctness: ALL PASS (Bell=1.0, GHZ-5 all-equal=1.0 P0=0.502, deterministic M, silent noiseless detectors).
7. C3 amortization (initially d=15, too cheap to show effect → raised to d=51): per-shot 225 µs→~22 µs, ~8–10× amortization confirmed.
8. C2 scaling (unrotated d=3..45): log-log slope time-vs-qubits = 0.885 → ~linear, sub-quadratic. Supports linear-vs-CHP-quadratic claim.
9. C5 threshold (Stim DEM → PyMatching, 50k shots/point, d=3/5/7, p=0.002..0.02): clean crossover between p=0.005 and 0.008 → threshold ~0.5–1%, textbook surface-code result.
10. C1 headline: FIRST attempt hung — my `sum(1 for _ in circ.flattened())` iterated ~1M instructions in pure Python (>5 min). Killed, replaced with C-level `len(flattened())` + target-slot sum. Rebuilt cleanly: 20,299 qubits, 1,009,900 measurements — matches paper. Compile+first DETECTOR sample 0.12 s.
11. Faithfulness fix: paper's "1 kHz full shots" = MEASUREMENT sampling, not detectors. Ran `c1_measrate.py` (compile_sampler): compile+first meas sample = **10.7 s** (≈ paper's 15 s ✓); sustained **0.148–0.151 kHz** (100/1000 batches).
12. Investigated 1 kHz gap: larger batches (`c1_ratebig.py`) got WORSE (0.11→0.08 kHz) → memory-bound (1M-meas output ~126 KB/shot even bit-packed). Isolated engine marginal cost (`c1_enginerate.py`): (t201−t1)/200 = 4.25 ms/shot = **0.235 kHz**. Consistently ~4–7× under 1 kHz; attributable to hardware/version/memory-bound output/single-thread, not a method failure.
13. Consolidated results_*.json → results_all.json; copied evidence.
14. LLM judge (free Argo `argo:gpt-4.1`, temp 0.1) on full measured-vs-claimed bundle → per-claim: C1 partial, C2/C3/C4/C5 reproduced. **FINAL_VERDICT: PARTIAL.**
15. Wrote REPORT.md, brief.md, artifact_harvest.md, this log.

## What worked
- Public Stim+PyMatching API reproduced correctness, linear scaling, amortization, and the surface-code threshold cleanly.
- Analyze-time headline reproduced (even faster than paper).

## What didn't / caveats
- Exact 1 kHz sustained rate not hit (~0.15–0.24 kHz); memory-bound output + hardware/version differences.
- PDF vision extraction unavailable → used pdftotext (fine for text/claims; figures read via captions, not pixel data).
- target-slot count (~24M) over-counts vs paper's "~8M gates" (counts every qubit target incl. noise/reset ops).
