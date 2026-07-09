# Workflow — OSTI 3363025 replication

## Step-by-step

1. **Read the wave brief.** `cat WAVE_BRIEF_2026-07-01.md` — established the mandatory 8-artifact completion bar, free-endpoints rule, LLM-judge rule, real-data rule.
2. **Fetch the PDF via uicgpu.** Standing rule: route OSTI downloads through uicgpu. `ssh uicgpu 'source ~/env.sh && curl -sL https://www.osti.gov/servlets/purl/3363025 -o /tmp/osti_3363025.pdf'`. Copy back via `scp uicgpu:/tmp/osti_3363025.pdf paper.pdf`.
3. **Extract paper text.** `pdftotext -layout paper.pdf paper.txt` → 942 lines. Enumerate claims C1..C6, tag which are reproducible from released code + shipped data.
4. **Clone the code repo.** `ssh uicgpu 'cd /tmp && git clone https://github.com/miscquanta/HMRRL-tersoff-silica.git'`. Inspect all four files.
5. **Verify baseline density of seed.** Compute density of `quartz.data` from its box vectors + atom count: matches 2.648 g/cm³ (experimental α-quartz).
6. **Run verbatim in.relax with ML-Tersoff.** LAMMPS 29Aug2024 at `/data/stevens/envs/lammps-cuda/bin/lmp`. Capture density, energy, cell vectors.
7. **Repeat with Q-Tersoff.** Same protocol, different pair_coeff file.
8. **Diagnose iso vs. anisotropic scaling.** Rerun with `fix box/relax aniso` and `fix box/relax tri`. Same qualitative result, tighter density values.
9. **Diagnose NVE vs. NPT.** Rerun with `fix npt temp 298 298 0.1 tri 1 1 1` for 20 ps. Get equilibrium 298 K structure.
10. **Compute angles + coordination.** Custom `angles.py` script parses LAMMPS write_data, uses triclinic min-image, 2.2 Å Si-O cutoff.
11. **LLM-judge verdict.** POST evidence packet to `argo:gpt-5.1` via CherryRd `:4000` LiteLLM aggregator (Bearer stevens). Repeat with `argo:gemini-2.5-pro` for second opinion. Both returned CONTRADICTED.
12. **Write reports.** brief.md, REPORT.md (16 kB), attempt_log.md, artifact_harvest.md, open_questions.json (5 questions), workflow.md, artifacts_summary.md, failure_analysis.md, REPORT.tex.

## Tools + versions

| Tool | Version | Where |
|---|---|---|
| LAMMPS | 29 Aug 2024 | `/data/stevens/envs/lammps-cuda/bin/lmp` (uicgpu) |
| Python | 3 (system) | uicgpu `/usr/bin/python3` |
| NumPy | 2.4.3 | uicgpu, for angle analysis |
| pdftotext | poppler-utils | CherryRd host |
| curl | system | uicgpu (via `env.sh` proxy) |
| git | system | uicgpu |
| ssh + scp | OpenSSH | CherryRd for uicgpu transport |
| LiteLLM aggregator | :4000 on CherryRd Tailscale | Bearer stevens (Argo wrapper) |

## Free LLM endpoints used

- `argo:gpt-5.1` — primary judge for CONTRADICTED verdict
- `argo:gemini-2.5-pro` — second judge for CONTRADICTED verdict
- (attempted first) `argo:claude-opus-4.7` — hit LiteLLM upstream parse error, so fell back to gpt-5.1

All routed through `http://<tailnet-aggregator>:4000/v1/chat/completions` with `Authorization: Bearer stevens`.

## Effort estimate

- **Wall time**: ~28 minutes end-to-end (task received 18:07, WAVE_RESULT emitted ~18:36 CDT).
- **Compute**: ~4 minutes of LAMMPS CPU on uicgpu across 6 runs. Total ~1125-atom * ~30k steps summed = 34M atom-step. All single-core.
- **LLM tokens**: ~4000 input + ~1200 output per judge, 2 judges, 1 payload attempted with a third model = ~15k total tokens on Argo free endpoints.
- **Human time to replicate given this report**: ~10 minutes (clone repo, run 3 lmp commands, run angles.py, compare to Table above).
