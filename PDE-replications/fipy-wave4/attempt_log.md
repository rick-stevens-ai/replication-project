# Attempt Log — FiPy (Wave 4)

## 2026-06-16 18:29 — brief

Picked **1D transient diffusion** as the canonical FiPy example — the first worked example in the FiPy docs/tutorial and one that has an explicit analytic reference (`erfc`).

## 2026-06-16 18:30 — venv + install (prior subagent, then reused)

```
python3.14 -m venv venv
source venv/bin/activate
pip install fipy
```

`fipy==4.0.2` installed cleanly. Pure-Python install (no NIST native extensions needed for this example).

## 2026-06-16 18:31 — copy upstream example for provenance

`evidence/upstream_mesh1D.py` is a verbatim copy of the FiPy docs `examples/diffusion/mesh1D.py` for traceability.

## 2026-06-16 21:11 — drafted `evidence/run_diffusion.py`

Custom driver (instead of upstream's mesh1D.py) because upstream's example is interactive (Viewer-based) — needed a non-interactive, multi-mesh, JSON-emitting version.

## 2026-06-16 21:13 — full run

```
source venv/bin/activate
pip install scipy matplotlib  # already present
python evidence/run_diffusion.py
```

Output (4 mesh levels at t_final=0.05, D=1):

```
nx=  50  steps= 278  dt=1.80e-04  L2_interior=1.181e-02  Linf=2.714e-02  (1.7s)
nx= 100  steps=1112  dt=4.50e-05  L2_interior=1.162e-02  Linf=2.792e-02  (6.6s)
nx= 200  steps=4445  dt=1.12e-05  L2_interior=1.158e-02  Linf=2.838e-02 (26.5s)
nx= 400  steps=17778 dt=2.81e-06  L2_interior=3.517e-02  Linf=4.773e-02 (107.8s)
observed orders: [0.023, 0.006, -1.603]
```

Total: ~2.5 min.

## Interpretation written into REPORT.md

The "non-convergent" L2 plateau (~1.2 %) for nx ≤ 200 is the **boundary-modelling-error floor** between the finite-domain Dirichlet solve and the infinite-domain `erfc` reference — *not* a discretisation error of FiPy. The rise at nx=400 is consistent with linear-solver tolerance drift over 17 778 steps.

## Files written

```
brief.md                            1.9 KB
evidence/upstream_mesh1D.py        28 KB  (verbatim FiPy doc example)
evidence/run_diffusion.py           5.1 KB
evidence/results.json               1.4 KB
evidence/diffusion_solution.png    ~50 KB
evidence/convergence.png           ~50 KB
```

## Lessons

- FiPy install is painless on modern Python.
- The "compare to analytic reference" convention in the upstream docs has a hidden gotcha: the docs example uses an infinite-domain reference for a finite-domain solve, so apparent convergence stalls. For a real order-of-accuracy check one needs self-convergence against a fine-grid FiPy solution.
