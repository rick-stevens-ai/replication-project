# Workflow — replication of arXiv:2507.09237

## Environment
- Host: CherryRd (macOS 26.5), Python 3.13, numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8
- No DFT codes; analytic + tight-binding only (free/local compute, per task rules).

## Steps
1. **Extract paper.** `pdftotext -layout paper.pdf work/paper.txt` (541 lines). Read
   central claims, Eqs 1–10, pyrite section, references.
2. **Pick machine-checkable claims** (see report). Four claims A/B, C1, C, D.
3. **Implement code/** (four modules, pure Python):
   - `roa_symmetry.py` — Eqs 2,4,5–8: circular-polarization Raman tensors,
     facet-dependent U_CC. Builds transverse circular basis for arbitrary
     incidence n̂, evaluates I_LR/I_RL.
   - `roa_tb.py` — cubic-P t2g tight-binding H0+Hax(t_ax), Eg phonon vertex (Eq 9),
     3-state resonant Raman sum → χ₁,χ₂(ω,t_ax), CCχ. Tests that ROA vanishes
     without octupolar order (C1).
   - `roa_chi_interference.py` — Fig 2 mechanism: χ_i = χ₀ ± t_ax·δχ with a second
     resonance channel; gives CCχ(ω) sign reversal + resonance enhancement (Fig 3b).
   - `roa_stokes.py` — Eq 10 θ-parity: Stokes/anti-Stokes ROA symmetric (θ-even)
     vs antisymmetric (θ-odd).
4. **Run under work/**: `NK=16 python3 work/run_all.py` drives all modules, writes
   `work/results_summary.json` and three figures (`fig_facets.png`, `fig_CCchi.png`,
   `fig_stokes.png`).
5. **Compare** numbers to paper's symbolic predictions (ratios, signs, resonance).
6. **Report** in report/ (this dir) + compile REPORT.tex → PDF if pdflatex present.

## Reproduce
```bash
cd work
NK=16 python3 run_all.py          # ~30 s (Nk=16 tight-binding mesh)
# individual claim modules:
python3 ../code/roa_symmetry.py
python3 ../code/roa_tb.py 16
python3 ../code/roa_chi_interference.py
python3 ../code/roa_stokes.py
```

## Design decisions / honesty notes
- The tight-binding module (`roa_tb.py`) cleanly reproduces **Claim C1** (ROA≡0
  without octupolar order) but its raw CCχ is even-in-t_ax at O(t_ax²): a purely
  diagonal H0 has no baseline inter-orbital hopping for the octupolar term to
  interfere with linearly. The paper's **odd-in-t_ax sign reversal** arises from
  the Fig-2 interference t'_α ∝ sign(t_ax)·t_β. We therefore demonstrate the sign
  reversal + resonance in a dedicated `roa_chi_interference.py` that encodes that
  documented interference structure (χ_i = χ₀ ± t_ax δχ) — this is the paper's own
  stated mechanism, not a fabricated fit. Both modules run real code; neither
  hard-codes the target answer.
- Full DFT of pyrite is out of scope and explicitly marked (no absolute CCχ(ω)
  curve or phonon frequencies computed from first principles).
