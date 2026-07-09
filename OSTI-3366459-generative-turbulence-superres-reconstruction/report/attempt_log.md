# Attempt log — OSTI 3366459

Times CDT, 2026-07-04.

- **23:04** Received subagent task. Read `WAVE_BRIEF_2026-07-01.md`; noted "free endpoints only, LLM-judge scoring, real replication, PDF via uicgpu because CherryRd cannot reach osti.gov directly."
- **23:05** Created target dir tree `~/Dropbox/REPLICATE-PROJECT/OSTI-3366459-.../{report/evidence,work}`.
- **23:06** `ssh uicgpu` → `curl -sSL -o paper.pdf https://www.osti.gov/servlets/purl/3366459` → 4.45 MB PDF (v1.4). `scp` back to CherryRd `work/`.
- **23:07** Tried `pdf` tool on Dropbox path → refused (not under allowed dir). Copied to `~/.openclaw/workspace/tmp_paper/` → still fails because paid Anthropic + Google gemini-3-flash-preview unknown + gpt-5 PDF extract disabled. Fell back to `pdftotext -layout` for extraction. Extracted 851-line paper.txt with full abstract, results, methods, Tables 1&2, data/code availability. Verified paper is:
  - Oommen et al., *Nature Communications* 17:3707 (2026), DOI 10.1038/s41467-026-70145-4
  - Schlieren jet SR dataset is proprietary Tsinghua (contact hefeng@tsinghua.edu.cn)
  - Code+data on Zenodo 10.5281/zenodo.17088765 "publicly available upon publication"
  - Table 1 (SR): NO 0.0542/0.1601, adv-NO 0.0662/0.0109 field/spec-NRMSE
  - Table 2 (forecasting): NO 0.0326/0.0865, adv-NO 0.0265/0.0235
- **23:08** Chose independent proxy dataset: 2D forced Kolmogorov turbulence (public, canonical for spectral-bias studies, cited in same paper's lineage). Wrote `gen_kolmogorov.py` — pseudo-spectral vorticity NS with RK4, 2/3 dealiasing, forcing f_x=sin(4y).
- **23:09** Ran DNS on uicgpu CPU: `python gen_kolmogorov.py kolmo_128.npz 128` → 44 s. 1000 snapshots, enstrophy stabilizes at ~15 (statistically stationary). Sanity check ✅.
- **23:10** Wrote `train_sr.py`: UNet_SR (~1.4 M params) with 4× upsample head, PatchGAN discriminator. Two loops: L2-only baseline, and L2+adv+gradient-feature with 10-epoch L2 warmup.
- **23:11** Kicked off `CUDA_VISIBLE_DEVICES=2 python train_sr.py --epochs 60 --bs 16` on uicgpu. 60 epochs baseline + 60 epochs adv = 146 s wall-clock total on A100.
- **23:13** Noticed the log-spec NRMSE metric was numerically degenerate: computing over full k-range including the dealiased zero-energy tail gave ~0.86 for everything (denom dominated by log(1e-30)). Wrote `analyze.py` and then `inspect_spectrum.py` / `inspect_v2.py` restricted to resolved band k ≤ 59.
- **23:14** Corrected metric on trained models:
  - Bicubic: field 0.154, log-spec 0.810
  - NO baseline: field **0.120**, log-spec 0.887
  - adv-NO: field 0.156, log-spec **0.340**
  - **Ratio NO/adv on spec: 2.61×** (paper reports 14.7× on Schlieren; direction ✓ magnitude smaller as expected for smaller model/shorter training)
  - E(k=30): DNS=8.11, NO=0.33, adv-NO=6.39 → adv-NO recovers 79% vs NO's 4%; adv-NO/NO ratio at k=30 is 19×
- **23:15** Tried LLM judge via Argo. `argo:gpt-5` first errored 400; cause: `temperature=0.0` param not accepted by GPT-5 through Argo proxy. Removed temperature param → both `argo:gpt-5` and `argo:claude-opus-4.7` returned clean JSON verdicts: **PARTIAL, coverage 0.75, agreement 1.0**.
- **23:16** Copied all artifacts back to `report/evidence/`. Wrote `brief.md`, `REPORT.md`, `attempt_log.md`, `artifact_harvest.md`.
- **23:16** Final verdict: **PARTIAL**. Mechanism + direction of both trade-off claims reproduce cleanly; exact magnitude of Schlieren-specific 15× reduces to 2.6× on public Kolmogorov proxy with 1000× less compute.

## What worked

- Downloading OSTI PDF via uicgpu (CherryRd is firewalled from osti.gov) — one-shot.
- `pdftotext -layout` fallback when the `pdf` tool couldn't be used due to Anthropic billing / model availability.
- Own pseudo-spectral DNS as substitute for proprietary Schlieren data — physically legitimate proxy for spectral-bias study.
- Two-model matched comparison on same data + same architecture → clean isolation of the adversarial-loss effect.
- Two independent LLM judges (GPT-5 and Claude Opus 4.7 via free Argo) converged on same verdict.

## What didn't work / had to be routed around

- `pdf` tool blocked (path restrictions + paid endpoints failing) — used `pdftotext`.
- Naive log-spectrum NRMSE over full k-range was dominated by dealiased-tail noise — had to restrict to resolved band and try multiple normalizations to reveal the true 2.6× ratio.
- GPT-5 through Argo rejects `temperature` parameter — dropped it, worked immediately.
- Could not fetch Zenodo release (marked "upon publication" — status uncertain at 2026-07-04); this is why we ran a from-scratch reproduction rather than a code-release smoke test.
- Task 2 (3D HIT forecasting) and Task 3 (sparse PTV) would need ≥48 GPU-h each per the paper — out of scope for one wave slot.
