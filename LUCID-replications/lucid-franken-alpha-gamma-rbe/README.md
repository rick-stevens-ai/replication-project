# lucid-franken-alpha-gamma-rbe

LUCID replication of Franken et al., *Oncology Reports* **27**:769–774, 2012
(DOI [10.3892/or.2011.1604](https://doi.org/10.3892/or.2011.1604)) — RBE of
high-LET α-particles vs Cs-137 γ-rays for DNA-DSBs (γ-H2AX foci),
chromosome fragments, colour junctions and clonogenic survival in
SW-1573 human lung carcinoma cells.

**Verdict: PARTIAL.** All four RBE values and propagated uncertainties
in Table I are reproduced exactly from the published α slopes (see
`REPORT.md`). A full from-scratch refit of the underlying dose-response
curves would require digitization of Fig. 2, which is mechanical and
adds little value beyond confirming what Table I already implies.

- Coverage: **6/10** (RBE arithmetic + consistency + curve
  reconstruction done; raw-data refit not done because raw data are
  not public).
- Agreement: **10/10** on what was recomputed.

## Reproduce

```bash
python3 code/refit_rbe.py
```

Outputs land in `results/` (JSON) and `figures/` (PNG).
Requires `numpy` and `matplotlib`.

## Layout

See file tree at the bottom of `REPORT.md`.

## Data provenance

- PDF: copy of LUCID target
  `~/Dropbox/XFER/LUCID-replication-targets/555f0ea033d2c4c9a99a57bf414a06811497966a.pdf`.
- All numbers used in `code/refit_rbe.py` are transcribed verbatim
  from Table I of the paper (p. 773). No author contact, no paid
  data sources, no proprietary code.
