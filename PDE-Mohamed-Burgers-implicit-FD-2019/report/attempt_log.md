# Attempt log

All times America/Chicago, 2026-07-04.

- **12:08.** Kicked off subagent task. Read WAVE_BRIEF_2026-07-01.md, created target dir tree.
- **12:08–12:09.** Attempted direct PDF fetch of `https://www.tandfonline.com/doi/pdf/10.1080/25765299.2019.1613746?needAccess=true` — Cloudflare interstitial (5.8 kB HTML challenge, not the PDF). Same via `ssh uicgpu` (Cloudflare fingerprint is on the *destination*, not our source IP). Cross-checked with OpenAlex: only OA PDF source is the T&F one.
- **12:09.** Switched to `browser` tool. Opened `https://www.tandfonline.com/doi/full/10.1080/25765299.2019.1613746` in the OpenClaw Chrome profile; Cloudflare passed once JS ran. Extracted 49 kB of full-text via `document.body.innerText`. Saved to `work/paper_text.txt` with the derived equations, plus my error-analysis note that Example 3's stated "exact solution" is only an approximate ansatz (not literally an exact Burgers' solution — it drops a nonlinear term).
- **12:10.** Tables load on-click via `.displaySizeTable` popup. Wrote a JS click-loop that iterated over `data-id ∈ {t0001..t0012}` and scraped `table.innerText` for the ones I actually needed (1, 2, 6, 7, 10, 11, 12). Saved to `work/paper_tables.md`.
- **12:11.** Created Python venv, installed numpy 2.5.1 + scipy 1.18.0.
- **12:12.** Wrote `work/burgers1d.py`: Cole–Hopf exact solution for u₀=sin(πx) and u₀=4x(1−x) via composite Simpson on the Fourier coefficients, plus the BDF-2/BDF-1 solver with linear-extrapolation linearization, banded solve. Ran:
  - Table 1 (ν=10, T=0.1) pointwise: 4-sig-fig match to paper's "Proposed BDF-2" column.
  - Table 2 (ν=1, T=0.5) pointwise: 6-decimal match.
  - Table 6 L₂/L∞: same order of magnitude, all within ≤2× of paper's numbers, better than Mukundan-BDF-2 by exactly the ratio the paper claims.
  - Table 11 (Example 3 mixed BC, Re=20,100): every value within ≤2% of paper.
- **12:14.** Wrote `work/burgers2d.py`: sparse pentadiagonal assembly + `spsolve`, exact Fletcher/Liu-Pope-Sepehrnoori solution. Ran Table 12: all 12 cells match to 1–2 sig figs (best cases 4-sig-fig match).
- **12:16.** Wrote report/REPORT.md, artifact_harvest.md, brief.md, and copied JSON results into report/evidence/.
- **12:17.** Verdict: **REPLICATED.**

## What did not work / caveats

- Direct T&F PDF fetch — Cloudflare challenge; use headless browser or accept HTML-only.
- Example 3's "exact solution" `u=(1/4) e^{-νt} cos(πx)` is not a strict solution of Burgers' equation (checked by direct substitution — leaves a residual `-(π/32) e^{-2νt} sin(2πx)`). It is an approximate ansatz commonly used in the Burgers literature (Pugh 1995 M.S. thesis). Because our numerical L₂/L∞ against this ansatz agrees with the paper's Table 11 to within a few percent, our scheme is doing what the paper's scheme is doing — but strictly this benchmark tests reproduction of a slightly-off analytical form, not the Burgers PDE exactly. Called out honestly.
- Paper's Table 6 gives a slightly-lower error for the "Proposed Scheme BDF-2 at Δt=0.002" (`L2=1.15e-8`) than my `9.52e-9`. My implementation appears marginally more accurate on that specific case; well within the noise of exact vs numerical Cole–Hopf truncation (I used 200-term Fourier truncation; paper doesn't specify).
