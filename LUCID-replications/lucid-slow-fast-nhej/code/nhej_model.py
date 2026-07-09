"""
Open SciPy/ODE replica of Qi et al. 2021 (Cancers 13:2202) slow/fast NHEJ
G0/G1 DSB repair model.

Original is a spatial Monte Carlo (Geant4-DNA / DaMaRiS). This is a *well-mixed
compartmental* ODE re-implementation that uses the rate constants from
Table 1 of the paper (interpreted as mean transition times -> exponential rates
k = 1/tau). It is faithful to the *pathway topology* and *timescales*, but it
abstracts away DSB-end diffusion (CTRW) and spatial mismatch geometry.
The "Parallel"-pathway mismatch effect at long times is captured through
a single phenomenological probability `p_mismatch` which represents the
fraction of DSBs whose two ends progress down different sub-pathways and
therefore cannot form a synaptic complex (becoming residual unrepaired
breaks). This is documented as a *partial* replication: Monte Carlo
spatial details are NOT reproduced.

Cell-line specific variants: wild-type, Artemis-deficient, XLF-deficient
(these are modelled by zeroing or weakening the appropriate transitions
as the paper does).

Units throughout: time in seconds, DSBs as a fraction of initial yield N0.
"""
from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# Parameters (Table 1 of Qi et al. 2021, all values in *seconds* as the paper
# specifies — these are mean transition times; we convert to rate = 1/time).
# ---------------------------------------------------------------------------

@dataclass
class ModelParams:
    # Recruitment / processing time constants [s]
    tau_ku_inhibit:        float = 0.85   # Ku70/80 inhibition (fast-end protection)
    tau_release_ku_inhib:  float = 3.8    # Release from Ku70/80 inhibition
    tau_ku_recruit:        float = 1.1    # Ku70/80 recruitment
    tau_dnapk_fast:        float = 1.2    # DNA-PKcs recruitment in fast process
    tau_artemis_dnapk_slow:float = 500.0  # Artemis:DNA-PKcs recruitment, slow path
    tau_ctip:              float = 7.0    # CtIP recruitment
    tau_exo1:              float = 1.2    # EXO1 recruitment
    tau_become_blunt:      float = 60.0   # Become blunt (60 Model A, 400 Model B)
    tau_dissoc_synapsis:   float = 400.0  # Dissociation of synapsis (11 if XLF-def)
    tau_remove_base:       float = 300.0  # Remove base lesion
    tau_remove_ssb:        float = 900.0  # Remove SSB
    tau_stab_synapsis:     float = 250.0  # Stabilisation of synapsis
    tau_ligation_fast:     float = 1200.0 # Final ligation, fast branch (Model A & B)
    tau_ligation_slow:     float = 8000.0 # Final ligation, slow branch (Model A only)
    tau_ligation_B:        float = 3000.0 # Final ligation, Model B (intermediate)

    # Pathway choice and damage-input parameters
    # Probability of an individual DSB end going down the slow (resection-dep) path
    # Paper target is ~15% (Riballo et al.).
    p_slow: float = 0.15

    # Probability that the two ends of a DSB take DIFFERENT pathways and
    # CANNOT recover (permanent mismatch) in Model A. In the paper's spatial
    # Monte Carlo many mismatched pairs would still co-locate within 24h via
    # CTRW diffusion before getting truly stuck; only a subset become true
    # residual breaks. We fit p_mismatch_A to ~0.12 to reproduce the paper's
    # observed Model-A 24h residual of ~10-15% (Figs 3,4,5). p_mismatch_B = 0
    # because pathways can cross in Model B.
    p_mismatch_A: float = 0.12
    p_mismatch_B: float = 0.0

    # DSB yield input (photon assumption from paper)
    dsb_per_gy_per_cell: float = 25.0   # 25 DSBs/Gy/cell, Poisson mean (photon)

    # Deficiency flags
    artemis_deficient: bool = False     # block DNA-PKcs:Artemis recruitment
    xlf_deficient:     bool = False     # set tau_dissoc_synapsis = 11.0
    ctip_inhibited:    bool = False     # rescues Artemis-def, see Fig S6


def make_params(model: str = "B", **overrides) -> ModelParams:
    """Build a ModelParams for 'A' (Parallel) or 'B' (Entwined)."""
    p = ModelParams()
    if model.upper() == "A":
        p.tau_become_blunt = 60.0
        p.tau_ligation_slow = 8000.0
        # Long slow ligation in A; fast branch uses tau_ligation_fast = 1200
        p.p_mismatch = p.p_mismatch_A
        p.tau_ligation_used = p.tau_ligation_fast  # default for fast branch
        p._model = "A"
    elif model.upper() == "B":
        p.tau_become_blunt = 400.0
        p.tau_ligation_used = p.tau_ligation_B   # single intermediate ligation
        p.p_mismatch = p.p_mismatch_B
        p._model = "B"
    else:
        raise ValueError("model must be 'A' or 'B'")
    for k, v in overrides.items():
        setattr(p, k, v)
    if p.xlf_deficient:
        p.tau_dissoc_synapsis = 11.0
    return p


# ---------------------------------------------------------------------------
# ODE system
#
# We track the *fraction of initial DSB sites* in each macro-state.
# A DSB site is the unit (two ends collapsed). End-level dynamics are folded
# into effective transition rates derived from the slowest end-level step
# (rate-limiting), which is a standard reduction for well-mixed kinetics.
#
# Macro states (fraction of N0):
#   X_dsb     : DSB present, ends bare / Ku not yet bound
#   X_ku      : Ku70/80 bound to both ends (committed)
#   X_fast    : fast branch — DNA-PKcs bound, en route to synapsis
#   X_slow    : slow branch — CtIP/EXO1 recruited, awaiting Artemis:DNA-PKcs
#   X_slow_proc: slow branch after Artemis recruited, undergoing end-processing
#   X_syn     : synaptic complex formed (stable enough for ligation)
#   X_rep     : repaired
#   X_mis     : permanently mis-matched/unresolved (residual)
#
# Conservation: sum of all = 1.
# ---------------------------------------------------------------------------

STATE_NAMES = ["dsb", "ku", "fast", "slow", "slow_proc", "syn", "rep", "mis"]
N_STATES = len(STATE_NAMES)
IDX = {n: i for i, n in enumerate(STATE_NAMES)}


def rates_from_params(p: ModelParams):
    """Compute first-order rate constants (1/s) from mean-time params."""
    r = {}
    r["k_ku"]        = 1.0 / p.tau_ku_recruit
    r["k_path"]      = 1.0 / max(p.tau_dnapk_fast, p.tau_ctip)  # commit to a branch
    r["k_fast_form"] = 1.0 / p.tau_dnapk_fast
    r["k_slow_form"] = 1.0 / (p.tau_ctip + p.tau_exo1)          # CtIP -> EXO1 chain
    r["k_artemis"]   = 0.0 if p.artemis_deficient else 1.0 / p.tau_artemis_dnapk_slow
    r["k_blunt"]     = 1.0 / p.tau_become_blunt
    r["k_syn_form"]  = 1.0 / (p.tau_stab_synapsis)              # synapsis stabilisation
    r["k_dissoc"]    = 1.0 / p.tau_dissoc_synapsis              # synapsis -> back to bare
    r["k_lig_fast"]  = 1.0 / p.tau_ligation_used
    r["k_lig_slow"]  = 1.0 / p.tau_ligation_slow if p._model == "A" else 1.0 / p.tau_ligation_used
    return r


def derivs(t, y, p: ModelParams):
    r = rates_from_params(p)
    dsb, ku, fast, slow, slow_proc, syn, rep, mis = y

    # 1. DSB -> Ku-bound
    flux_ku = r["k_ku"] * dsb

    # 2. Ku-bound -> fast or slow branch
    # Per-end the choice is p_slow vs (1-p_slow). At the DSB-site level we
    # split flux accordingly. In Model A, some pairs become mismatched.
    f_to_slow = p.p_slow
    f_to_fast = 1.0 - p.p_slow
    if p._model == "A":
        # Apply mismatch loss at this branching: a fraction p.p_mismatch of
        # the branching flux ends up permanently mismatched (cannot ever
        # synapse because the two ends are in different sub-pathways).
        m = p.p_mismatch
    else:
        m = 0.0
    flux_branch = r["k_path"] * ku
    flux_to_fast = flux_branch * f_to_fast * (1.0 - m)
    flux_to_slow = flux_branch * f_to_slow * (1.0 - m)
    flux_to_mis  = flux_branch * m

    # 3. fast -> synapsis (DNA-PK complex bridges, stabilises)
    flux_fast_syn = r["k_syn_form"] * fast

    # 4. slow -> slow_proc (Artemis:DNA-PKcs recruited & blunting starts)
    if p.artemis_deficient and not p.ctip_inhibited:
        # blocked: slow DSBs stall; cannot proceed to processing
        flux_slow_proc = 0.0
    else:
        flux_slow_proc = r["k_artemis"] * slow  # combine artemis + blunt timescales
    # 5. slow_proc -> synapsis
    flux_slowp_syn = r["k_blunt"] * slow_proc

    # 6. synapsis -> ligated (repaired) OR back-dissociation to Ku state
    # Ligation rate: use fast for synapses originating from fast branch.
    # Here we use the entwined ligation rate as a single effective rate,
    # since the well-mixed model can't track end provenance separately
    # without splitting `syn` into two compartments. For Model A we
    # weight by the branch fractions.
    if p._model == "A":
        # In Model A the synapse compartment is a mixture of fast-branch
        # (tau_lig=1200s) and slow-branch (tau_lig=8000s) complexes.
        k_lig_eff = (1.0 - p.p_slow) * r["k_lig_fast"] + p.p_slow * r["k_lig_slow"]
        # Per Table 1, in Model A "Dissociation in slow process: No", so
        # synapsis dissociation in Model A is reduced (occurs only in the
        # fast-branch fraction).
        k_dissoc_eff = (1.0 - p.p_slow) * r["k_dissoc"]
    else:
        k_lig_eff = r["k_lig_fast"]
        k_dissoc_eff = r["k_dissoc"]

    flux_lig    = k_lig_eff * syn
    flux_dissoc = k_dissoc_eff * syn
    # Dissociation returns the synapse to a Ku-bound state (proteins remain
    # loaded — only the synaptic bridge is broken). Avoid re-routing through
    # the pathway-commitment branching, which would falsely amplify the
    # one-time mismatch fraction by re-counting each dissociation cycle.

    # Assemble derivatives
    d = np.zeros(N_STATES)
    d[IDX["dsb"]]       = -flux_ku
    # Dissociation re-enters the appropriate pathway compartment, NOT the
    # bare-DSB / Ku-binding step (the proteins are still loaded). Route the
    # dissociation flux back to the `fast` and `slow_proc` compartments
    # weighted by branch fractions, so the mismatch isn't double-counted.
    diss_to_fast = (1.0 - p.p_slow) * flux_dissoc
    diss_to_slow_proc = p.p_slow * flux_dissoc
    d[IDX["ku"]]        = +flux_ku - flux_branch
    d[IDX["fast"]]      = +flux_to_fast - flux_fast_syn + diss_to_fast
    d[IDX["slow"]]      = +flux_to_slow - flux_slow_proc
    d[IDX["slow_proc"]] = +flux_slow_proc - flux_slowp_syn + diss_to_slow_proc
    d[IDX["syn"]]       = +flux_fast_syn + flux_slowp_syn - flux_lig - flux_dissoc
    d[IDX["rep"]]       = +flux_lig
    d[IDX["mis"]]       = +flux_to_mis
    return d


def simulate(model: str, t_hours: np.ndarray, dose_gy: float = 2.0, **kwargs):
    """Run simulation. Returns dict of state-fraction arrays vs t (in hours)."""
    p = make_params(model, **kwargs)
    t_s = t_hours * 3600.0
    y0 = np.zeros(N_STATES)
    y0[IDX["dsb"]] = 1.0  # normalised initial DSB fraction
    sol = solve_ivp(
        derivs, (t_s[0], t_s[-1]), y0, t_eval=t_s,
        args=(p,), method="LSODA", rtol=1e-8, atol=1e-10, max_step=10.0
    )
    if not sol.success:
        raise RuntimeError(f"ODE solver failed: {sol.message}")
    out = {n: sol.y[i] for i, n in enumerate(STATE_NAMES)}
    out["t_hours"] = t_hours
    # Total unrepaired = everything except 'rep'
    out["unrepaired_frac"] = 1.0 - out["rep"]
    # In absolute DSB count for dose_gy:
    N0 = dose_gy * p.dsb_per_gy_per_cell
    out["unrepaired_count"] = out["unrepaired_frac"] * N0
    out["N0"] = N0
    out["model"] = p._model
    out["params"] = p
    return out


if __name__ == "__main__":
    t = np.linspace(0, 24, 200)
    for m in ["A", "B"]:
        r = simulate(m, t, dose_gy=2.0)
        # Print residual at 1h, 6h, 24h
        for h in [1.0, 6.0, 24.0]:
            idx = np.argmin(np.abs(t - h))
            print(f"Model {m}  t={h:5.1f}h  unrepaired={r['unrepaired_count'][idx]:6.2f} "
                  f"({100*r['unrepaired_frac'][idx]:5.1f}%)")
        print()
