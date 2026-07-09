# LUCID Replication — UNIVERSE repair kinetics / dose-rate RBE

Paper: Liew et al. (2022), **Impact of DNA Repair Kinetics and Dose Rate on RBE Predictions in the UNIVERSE**, *Int. J. Mol. Sci.* 23, 6268. DOI `10.3390/ijms23116268`.

## Scope

This is a **formula/table/diagnostic partial replication**. The paper's data availability statement is "Not applicable"; no public UNIVERSE code, raw simulation outputs, FLUKA SOBP beamline model, or GPU three-step radial-dose parametrization were released. The original subagent built useful scaffolding but timed out while debugging the stochastic RBE solver. I therefore added a lightweight deterministic audit driver that validates the released parameters/tables and reproduces the qualitative dose-rate/RBE trends without overclaiming bit-exact reproduction.

## Files

- `REPORT.md` — audit report and verdict
- `PROGRESS.md` — chronology and blockers
- `code/universe_core.py` — stochastic photon-domain UNIVERSE scaffold from equations
- `code/kiefer_chatterjee.py` — radial-dose / ion-track scaffold
- `code/simulate_universe.py` — heavier stochastic driver; unfinished/debuggy
- `code/lightweight_universe_audit.py` — deterministic table/diagnostic audit used for final results
- `results/summary.json` — parameter/table/benchmark summary
- `results/diagnostic_rbe_curves.csv` — diagnostic RBE-vs-dose-rate curves
- `figures/*.png` — diagnostic plots

## Rerun

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-universe-repair-doserate-rbe
python3 code/lightweight_universe_audit.py
```

Expected runtime: <10 seconds on laptop CPU.

Dependencies: `numpy`, `matplotlib`.

The heavier stochastic scaffold can be inspected, but should not be treated as validated final output.
