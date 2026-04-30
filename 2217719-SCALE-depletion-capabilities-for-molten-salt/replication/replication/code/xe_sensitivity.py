"""
Tier-lift OSTI 2217719 — Xe-135 removal-rate reactivity sensitivity (Q1).

The MSRE used continuous off-gas (helium) sparging to remove noble
gases including Xe-135.  In a static (closed-system) reactor, Xe-135
reaches an equilibrium where (production from I-135 decay + direct fission)
balances (Xe absorption + Xe decay).  Online removal at rate λ_rem
shifts the equilibrium and reduces the negative reactivity penalty from
Xe poisoning.

We solve the I/Xe Bateman pair at thermal equilibrium and convert
ΔN_Xe → Δρ via the standard Xe-poisoning formula:
    Δρ ≈ -(σ_a^Xe / σ_a^fuel) * (N_Xe / N_fuel)
and then evaluate dρ/d(ln λ_rem) at the MSRE removal rate (4.067e-5 /s,
from Sec. 4 of the paper).

This addresses follow-on Q1 of the existing replication report
("How sensitive is the 375-day reactivity swing to the online Xe-135
removal rate?") with a fully analytical, defensible computation.
"""
import numpy as np
import matplotlib.pyplot as plt
import os, json

# Constants
LAMBDA_I135  = np.log(2) / (6.57 * 3600)      # s^-1, t1/2 = 6.57 h
LAMBDA_XE135 = np.log(2) / (9.14 * 3600)      # s^-1, t1/2 = 9.14 h
GAMMA_I135   = 0.0629                          # cumulative I-135 fission yield (U-235 thermal)
GAMMA_XE135  = 0.00237                         # direct Xe-135 yield
SIGMA_A_XE135_b   = 2.65e6                     # barns, thermal microscopic absorption
SIGMA_F_U235_b    = 585.0                      # barns
SIGMA_A_FUEL_b    = 681.0                      # barns (fission + capture, U-235 thermal)

# MSRE-relevant operating parameters
PHI_TH = 1.0e13        # thermal flux, n/cm^2/s (paper Sec 4 typical for 8 MWth MSRE)
N_FUEL = 4.5e-5 * 6.022e23 / 235  # not exact — derived from fuel atom density
# Paper-stated baseline removal rate for noble gases:
LAMBDA_REM_BASE = 4.067e-5

def equilibrium_NXe(lambda_rem, phi=PHI_TH):
    """Equilibrium Xe-135 number density per fission rate:
       at steady state:
         I:  γ_I Σ_f φ - λ_I N_I = 0  →  N_I = γ_I Σ_f φ / λ_I
         Xe: γ_Xe Σ_f φ + λ_I N_I - (λ_Xe + σ_a^Xe φ + λ_rem) N_Xe = 0
    We use cross sections in cm^2 (1 b = 1e-24 cm^2)."""
    sig_a_xe = SIGMA_A_XE135_b * 1e-24
    sig_f    = SIGMA_F_U235_b * 1e-24
    Sigma_f  = sig_f * N_FUEL
    NI = GAMMA_I135 * Sigma_f * phi / LAMBDA_I135
    Nxe = (GAMMA_XE135 * Sigma_f * phi + LAMBDA_I135 * NI) / \
          (LAMBDA_XE135 + sig_a_xe * phi + lambda_rem)
    return Nxe, NI

def reactivity_penalty(NXe):
    sig_a_xe = SIGMA_A_XE135_b * 1e-24
    sig_a_f  = SIGMA_A_FUEL_b * 1e-24
    return -(sig_a_xe * NXe) / (sig_a_f * N_FUEL)

def main():
    lams = np.logspace(-7, -2, 100)
    rho = []
    for L in lams:
        nxe, _ = equilibrium_NXe(L)
        rho.append(reactivity_penalty(nxe))
    rho = np.array(rho)

    # Baseline reactivity penalty
    nxe0, _ = equilibrium_NXe(LAMBDA_REM_BASE)
    rho0 = reactivity_penalty(nxe0)
    # Compare: no removal (λ_rem = 0)
    nxe_no, _ = equilibrium_NXe(0.0)
    rho_no = reactivity_penalty(nxe_no)
    delta_rho = rho0 - rho_no

    # Sensitivity dρ/dlnλ at baseline (numerical)
    eps = 0.01
    nxe_p, _ = equilibrium_NXe(LAMBDA_REM_BASE * (1+eps))
    nxe_m, _ = equilibrium_NXe(LAMBDA_REM_BASE * (1-eps))
    drho = (reactivity_penalty(nxe_p) - reactivity_penalty(nxe_m)) / (2*eps)

    print(f"Xe poisoning (no removal):    ρ = {rho_no*1e5:8.1f} pcm")
    print(f"Xe poisoning (MSRE removal):  ρ = {rho0*1e5:8.1f} pcm  (baseline λ_rem={LAMBDA_REM_BASE:.3e}/s)")
    print(f"Δρ benefit of online removal: Δρ = {delta_rho*1e5:8.1f} pcm")
    print(f"Local sensitivity: dρ/d(ln λ_rem) ≈ {drho*1e5:.2f} pcm per e-fold")

    # Plot
    fig, ax = plt.subplots(figsize=(7,4.5))
    ax.semilogx(lams, rho*1e5, 'b-')
    ax.axvline(LAMBDA_REM_BASE, color='r', ls='--', label=f"MSRE design ({LAMBDA_REM_BASE:.2e}/s)")
    ax.axvline(LAMBDA_XE135, color='g', ls=':', label=f"natural Xe decay ({LAMBDA_XE135:.2e}/s)")
    ax.set_xlabel(r"Online Xe removal rate $\lambda_{\rm rem}$ (s$^{-1}$)")
    ax.set_ylabel(r"Equilibrium Xe-135 reactivity (pcm)")
    ax.set_title("MSRE Xe-135 poisoning vs online removal (tier-lift Q1)")
    ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout()
    out_fig = os.path.expanduser(
        "~/Dropbox/REPLICATE-PROJECT/2217719-scale-msr/replication/figures/xe_sensitivity.png")
    fig.savefig(out_fig, dpi=140); print(f"saved {out_fig}")

    # Save numbers
    out_json = os.path.expanduser(
        "~/Dropbox/REPLICATE-PROJECT/2217719-scale-msr/replication/data/xe_sensitivity.json")
    with open(out_json, "w") as f:
        json.dump(dict(
            lambda_rem_baseline=LAMBDA_REM_BASE,
            rho_no_removal_pcm=float(rho_no*1e5),
            rho_with_removal_pcm=float(rho0*1e5),
            delta_rho_benefit_pcm=float(delta_rho*1e5),
            drho_dlnlambda_pcm=float(drho*1e5),
        ), f, indent=2)
    print(f"saved {out_json}")

if __name__ == "__main__":
    main()
