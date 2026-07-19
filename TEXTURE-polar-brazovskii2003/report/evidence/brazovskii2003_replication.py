#!/usr/bin/env python
"""
Independent replication of core physics of Brazovskii (2003), cond-mat/0306006v2:
"Theory of the ferroelectric phase in organic conductors: optics and physics of solitons"

Reimplemented from the paper's analytic equations (NOT author code).
Key equations used (line refs to corpus .txt):

  (H)  HU = -Us cos2phi - Ub sin2phi = -U cos(2phi-2alpha),
       U = sqrt(Us^2+Ub^2),  tan(2alpha)=Ub/Us                       [l.96]
  Gap: Delta ~ U^(1/(2-2gamma)),  U* ~ Delta^2/(hbar vF)             [l.99-100]
  CD instability requires gamma < 1/2                                [l.102]
  Soliton charges (in units of e):
       pi-soliton (holon): q=1,  delta_phi=pi                        [l.114]
       alpha-soliton (FE wall): delta_phi=-2alpha or pi-2alpha
       => noninteger charge q=-2alpha/pi or 1-2alpha/pi              [l.117-119]
  Optical collective-mode gap:  omega_t ~ pi*gamma*Delta < 2Delta    [l.153]
       (small-gamma simplification); photoconductivity gap = 2Delta  [l.22]
  Mixed electron-phonon dielectric response (eq. 2)                  [l.176-190]:
       eps(w)/eps_inf = 1 + (wp*/wt)^2 (1-(w/w0)^2)
                            / [ (1-(w/w0)^2)(1-(w/wt)^2) - Z ]
       Z = (wcr/wt)^(2-4gamma) <= 1
  Combined e-ph resonance:  w0t^2 ~ w0^2 + wt^2                      [l.196-198]
  FE soft mode:  wfe^2 ~ (1-Z)/(w0^-2 + wt^-2)                       [l.200-203]
  Curie divergence: eps(T) = A|T/T0-1|^-1, A~(wp*/wt)^2~1e3          [l.210-211]
  Spin gap: Delta_sigma ~ Uao^(2/3)                                  [l.140]
  Soliton core/tail lengths: xi_rho~vF/Delta, xi_sigma~vF/Delta_sigma[l.145-147]
"""
import numpy as np

results = {}

# ---------------------------------------------------------------------------
# 1. Combined Mott-Hubbard Hamiltonian: minimum and effective amplitude U
# ---------------------------------------------------------------------------
def U_and_alpha(Us, Ub):
    U = np.hypot(Us, Ub)
    alpha = 0.5 * np.arctan2(Ub, Us)
    return U, alpha

def HU(phi, Us, Ub):
    return -Us*np.cos(2*phi) - Ub*np.sin(2*phi)

Us, Ub = 0.7, 0.4
U, alpha = U_and_alpha(Us, Ub)
# Verify -U cos(2phi-2alpha) form equals -Us cos2phi - Ub sin2phi
phi = np.linspace(0, np.pi, 2001)
lhs = HU(phi, Us, Ub)
rhs = -U*np.cos(2*phi - 2*alpha)
max_form_err = np.max(np.abs(lhs - rhs))
# Ground-state minimum should sit at phi = alpha (mod pi)
phi_min = phi[np.argmin(lhs)]
results["hamiltonian"] = {
    "Us": Us, "Ub": Ub, "U_computed": float(U),
    "U_check_sqrt(Us^2+Ub^2)": float(np.sqrt(Us**2+Ub**2)),
    "alpha_rad": float(alpha), "tan2alpha_computed": float(np.tan(2*alpha)),
    "tan2alpha_target_Ub/Us": float(Ub/Us),
    "form_identity_max_abs_err": float(max_form_err),
    "phi_min_numeric": float(phi_min), "phi_min_expected_alpha": float(alpha),
    "min_matches_alpha": bool(abs(phi_min - alpha) < (phi[1]-phi[0])*2),
}

# ---------------------------------------------------------------------------
# 2. Soliton charges (noninteger alpha-solitons, FE domain walls)
# ---------------------------------------------------------------------------
q_holon = 1.0                       # pi-soliton, delta_phi=pi
q_alpha_a = -2*alpha/np.pi          # delta_phi = -2alpha
q_alpha_b = 1 - 2*alpha/np.pi       # delta_phi = pi-2alpha
results["soliton_charges_in_e"] = {
    "pi_soliton_holon": q_holon,
    "alpha_soliton_(-2a/pi)": float(q_alpha_a),
    "alpha_soliton_(1-2a/pi)": float(q_alpha_b),
    "note": "noninteger FE-domain-wall charges; sum of the two = 1-4a/pi",
}

# ---------------------------------------------------------------------------
# 3. Gap scaling Delta ~ U^{1/(2-2gamma)} and optical edge omega_t ~ pi gamma Delta
# ---------------------------------------------------------------------------
def Delta_from_U(U, gamma, C=1.0):
    return C * U**(1.0/(2.0-2.0*gamma))

def omega_t(gamma, Delta):
    return np.pi*gamma*Delta          # collective (ferroelectric) optical gap

gamma = 0.25                          # below CD threshold 1/2, small-gamma regime
Delta = 1.0                           # set energy unit Delta = 1
wt = omega_t(gamma, Delta)
results["gaps"] = {
    "gamma": gamma,
    "CD_instability_satisfied_gamma<1/2": bool(gamma < 0.5),
    "Delta_unit": Delta,
    "omega_t": float(wt),
    "omega_t_over_2Delta": float(wt/(2*Delta)),
    "optical_edge_below_2Delta": bool(wt < 2*Delta),
    "gamma_max_for_wt<2Delta": float(2.0/np.pi),  # pi*gamma<2 => gamma<2/pi
    "photoconductivity_gap_2Delta": 2*Delta,
    "Delta_scaling_exponent_1/(2-2gamma)": float(1.0/(2-2*gamma)),
}

# ---------------------------------------------------------------------------
# 4. Dielectric response eq.(2): poles vs analytic resonance/soft-mode formulas
# ---------------------------------------------------------------------------
def eps_over_epsinf(w, wp_star, wt, w0, Z):
    a = 1 - (w/w0)**2
    b = 1 - (w/wt)**2
    return 1 + (wp_star/wt)**2 * a / (a*b - Z)

def denom_roots(wt, w0, Z):
    # denominator=0 :  x^2 - (w0^2+wt^2) x + (1-Z) w0^2 wt^2 = 0,  x=w^2
    A = 1.0
    B = -(w0**2 + wt**2)
    Cc = (1-Z)*w0**2*wt**2
    disc = B*B - 4*A*Cc
    x1 = (-B - np.sqrt(disc))/2   # lower (soft FE mode)
    x2 = (-B + np.sqrt(disc))/2   # upper (combined e-ph resonance)
    return np.sqrt(x1), np.sqrt(x2)

w0 = 1.3*wt                # bare molecular vibration freq (arbitrary, ~wt scale)
wp_star = 30.0*wt          # renormalized plasma freq (=> A=(wp*/wt)^2=900 ~1e3)

# The paper's resonance/soft-mode formulas carry "~/≈": they are the leading
# (1-Z)->0 expansion of the exact denominator roots, valid NEAR criticality
# Z(T0)=1. Verify convergence: exact roots -> analytic formulas as Z->1.
w0t_analytic = np.sqrt(w0**2 + wt**2)
Z_scan = [0.5, 0.9, 0.99, 0.999, 0.9999]
w0t_errs, wfe_errs = [], []
for z in Z_scan:
    wfe_n, w0t_n = denom_roots(wt, w0, z)
    wfe_a = np.sqrt((1-z)/(w0**-2 + wt**-2))
    w0t_errs.append(abs(w0t_n-w0t_analytic)/w0t_analytic)
    wfe_errs.append(abs(wfe_n-wfe_a)/wfe_a)

Z = 0.9999                 # near criticality: analytic formulas apply
wfe_num, w0t_num = denom_roots(wt, w0, Z)
wfe_analytic = np.sqrt((1-Z)/(w0**-2 + wt**-2))

# Antiresonance (Fano): numerator vanishes at w=w0 => eps/eps_inf = 1 there
eps_at_w0 = eps_over_epsinf(w0, wp_star, wt, w0, Z)

results["dielectric_response"] = {
    "wp_star": float(wp_star), "w0": float(w0), "wt": float(wt),
    "Z_scan": Z_scan,
    "w0t_rel_err_vs_Z": [float(e) for e in w0t_errs],
    "wfe_rel_err_vs_Z": [float(e) for e in wfe_errs],
    "errors_decrease_toward_criticality": bool(
        w0t_errs[-1] < w0t_errs[0] and wfe_errs[-1] < wfe_errs[0]),
    "Z_near_crit": Z,
    "upper_resonance_w0t_numeric": float(w0t_num),
    "upper_resonance_w0t_analytic_sqrt(w0^2+wt^2)": float(w0t_analytic),
    "w0t_rel_err_near_crit": float(abs(w0t_num-w0t_analytic)/w0t_analytic),
    "soft_mode_wfe_numeric": float(wfe_num),
    "soft_mode_wfe_analytic": float(wfe_analytic),
    "wfe_rel_err_near_crit": float(abs(wfe_num-wfe_analytic)/wfe_analytic),
    "antiresonance_eps_over_epsinf_at_w0": float(eps_at_w0),
    "antiresonance_is_unity": bool(abs(eps_at_w0 - 1.0) < 1e-9),
}

# ---------------------------------------------------------------------------
# 5. Soft-mode -> 0 and Curie law eps ~ A |T/T0-1|^-1 as Z -> 1 (criticality)
# ---------------------------------------------------------------------------
# Model: near T0, wcr(T)->wt so Z->1. Take reduced temp t=(T-T0)/T0>0 with
# 1-Z proportional to t (leading order). eps(0) static dielectric constant.
A_amp = (wp_star/wt)**2
t_vals = np.array([0.2, 0.1, 0.05, 0.02, 0.01, 0.005])
Z_vals = 1 - t_vals                       # 1-Z = t  (leading order)
eps0 = np.array([eps_over_epsinf(0.0, wp_star, wt, w0, z) for z in Z_vals])
# eps(0)/eps_inf = 1 + A/(1-Z) = 1 + A/t  => (eps0-1)*t should equal A (constant)
curie_product = (eps0 - 1.0)*t_vals
wfe_vals = np.array([denom_roots(wt, w0, z)[0] for z in Z_vals])
results["curie_law_and_soft_mode"] = {
    "A_amplitude_(wp*/wt)^2": float(A_amp),
    "A_order_of_magnitude_target": "~1e3",
    "reduced_temps_t": t_vals.tolist(),
    "eps0_over_epsinf": eps0.tolist(),
    "curie_product_(eps-1)*t_should_be_constant_A": curie_product.tolist(),
    "curie_product_std_over_mean": float(np.std(curie_product)/np.mean(curie_product)),
    "soft_mode_wfe_vs_t_(should_->0)": wfe_vals.tolist(),
    "wfe_scales_as_sqrt(t)": bool(np.corrcoef(wfe_vals, np.sqrt(t_vals))[0,1] > 0.999),
    "experimental_eps_amplitude": "~1e4 * T0/(T-T0)",
}

# ---------------------------------------------------------------------------
# 6. Spin gap and soliton lengths (functional forms)
# ---------------------------------------------------------------------------
def spin_gap(Uao, C=1.0):
    return C * Uao**(2.0/3.0)         # spin-Peierls-type

Uao = 0.05
Dsig = spin_gap(Uao)
vF = 1.0
xi_rho = vF/Delta
xi_sigma = vF/Dsig
results["spin_sector"] = {
    "Uao": Uao, "Delta_sigma": float(Dsig),
    "spin_gap_exponent_2/3": 2.0/3.0,
    "xi_rho_charge_core": float(xi_rho),
    "xi_sigma_spin_tail": float(xi_sigma),
    "xi_sigma>>xi_rho": bool(xi_sigma > xi_rho),
}

# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------
checks = {
    "H_form_identity": results["hamiltonian"]["form_identity_max_abs_err"] < 1e-9,
    "H_min_at_alpha": results["hamiltonian"]["min_matches_alpha"],
    "wt_below_2Delta": results["gaps"]["optical_edge_below_2Delta"],
    "resonance_matches_analytic_near_crit": results["dielectric_response"]["w0t_rel_err_near_crit"] < 1e-3,
    "softmode_matches_analytic_near_crit": results["dielectric_response"]["wfe_rel_err_near_crit"] < 1e-3,
    "resonance_softmode_converge_to_crit": results["dielectric_response"]["errors_decrease_toward_criticality"],
    "antiresonance_unity": results["dielectric_response"]["antiresonance_is_unity"],
    "curie_law_constant": results["curie_law_and_soft_mode"]["curie_product_std_over_mean"] < 1e-6,
    "softmode_sqrt_t": results["curie_law_and_soft_mode"]["wfe_scales_as_sqrt(t)"],
    "spin_tail_longer": results["spin_sector"]["xi_sigma>>xi_rho"],
}
results["verdict"] = {
    "checks": {k: bool(v) for k,v in checks.items()},
    "n_passed": int(sum(checks.values())),
    "n_total": len(checks),
}

import json
print(json.dumps(results, indent=2))
