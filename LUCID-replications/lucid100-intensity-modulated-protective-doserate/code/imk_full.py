#!/usr/bin/env python3
"""
Full IMK (Integrated Microdosimetric-Kinetic) model — single-dose acute exposure
implementation for Matsuya et al. 2019, Sci Rep 9:9533.

Eqs implemented (from the paper):
  Eq 2 (DNA-TE acute, T->0 with single fraction):
        -ln S_T = (alpha_0 + gamma * beta_0) * D + beta_0 * D^2
  Eq 5 (NTE survival, intercellular communication):
        -ln S_NT = delta * [1 - exp( -((alpha_b + gamma_IF * beta_b)*D_IF + beta_b*D_IF^2) )]
                       * exp( -((alpha_b + gamma_*  * beta_b)*D_*  + beta_b*D_* ^2) )
  Eq 6 (total): w = w_T + w_NT  =>  S_* = exp(-w)

  f_h(D)  = 1 - exp(-((alpha_b + gamma*beta_b)*D + beta_b*D^2))   (Poisson hit fraction)
  f_b(D)  = exp(-((alpha_b + gamma*beta_b)*D + beta_b*D^2))       (non-hit fraction)

Microdosimetric coefficient:
  gamma = y_D / (rho * pi * r_d^2)
  with rho = 1.0 g/cm^3, r_d = 0.5 um, y_D in keV/um.
  Numerical conversion: 1 keV/um / (1 g/cm^3 * pi * (0.5 um)^2)
    = 1 keV/um / (pi * 0.25 g um^-1 * (1e-12 cm^3/um^3) * (1 cm^3 / g)*(...))
  Easier: gamma[Gy] = y_D[keV/um] / (rho[g/cm^3] * pi * r_d[um]^2) * 0.1602
    (because 1 keV/um divided by 1 g/cm^3 * 1 um^2 -> 1 keV / (g * (1e-2 mm)^3 * 1e-6 mm^2 ) = ...
     simpler: 1 keV/um^3 (energy per volume) in water of density 1 g/cm^3 = 1.602e-19 * 1e3 / (1e-12 * 1e-3) J/kg = 0.1602 Gy)
  So gamma(Gy) = (y_D(keV/um) / (pi * r_d(um)^2 * rho(g/cm^3))) * 0.1602

Paper values:
  y_D (in-field)     = 4.393 keV/um
  y_D (out-of-field) = 4.769 keV/um   (slightly higher due to softer scattered photons)
  r_d = 0.5 um, rho = 1 g/cm^3
"""
import math
import json
import os

PARAMS = {
    # DNA-TE branch parameters (Table 1)
    'AGO1522_MF': {'alpha0': 0.363, 'beta0': 0.011, 'aplusc': 0.034},  # MF fits
    'AGO1522_UF': {'alpha0': 0.388, 'beta0': 0.081, 'aplusc': 1.684},  # UF fits
    'DU145_MF'  : {'alpha0': 0.032, 'beta0': 0.039, 'aplusc': 2.509},
    'DU145_UF'  : {'alpha0': 0.022, 'beta0': 0.041, 'aplusc': 1.506},
}

# Intercellular communication parameters (Table 1, per cell line, independent of field)
IC_PARAMS = {
    'AGO1522': {'alpha_b': 0.388, 'beta_b': 0.031, 'delta': 0.617},
    'DU145'  : {'alpha_b': 0.041, 'beta_b': 0.023, 'delta': 0.470},
}

# Microdosimetric input
Y_D_IF = 4.393  # keV/um, in-field
Y_D_OF = 4.769  # keV/um, out-of-field
R_D    = 0.5    # um
RHO    = 1.0    # g/cm^3

def gamma_Gy(y_D_keV_per_um, r_d_um=R_D, rho_g_per_cm3=RHO):
    """gamma microdosimetric quantity in Gy."""
    # y_D / (pi r_d^2 * rho) in keV / um^3 / (g/cm^3)
    # 1 keV/um^3 / (1 g/cm^3) = 1.602e-19*1e3 J / (1e-15 m^3) / 1e3 kg/m^3
    #                          = 1.602e-19*1e3 / (1e-15 * 1e3) Gy
    #                          = 0.1602 Gy
    return (y_D_keV_per_um / (math.pi * r_d_um**2 * rho_g_per_cm3)) * 0.1602

GAMMA_IF = gamma_Gy(Y_D_IF)  # ~0.1602 * 4.393/(pi*0.25) ~ 0.896 Gy
GAMMA_OF = gamma_Gy(Y_D_OF)

def w_TE(D, alpha0, beta0, gamma):
    """DNA-TE -ln S_T in acute limit (single fraction, T->0)."""
    return (alpha0 + gamma * beta0) * D + beta0 * D**2

def w_NT(D_IF, D_star, alpha_b, beta_b, delta, gamma_IF, gamma_star):
    """NTE -ln S_NT per Eq 5. D_IF is delivered dose to in-field cells; D_star is
    dose to the * cell (IF or OF)."""
    a = (alpha_b + gamma_IF * beta_b) * D_IF + beta_b * D_IF**2
    b = (alpha_b + gamma_star * beta_b) * D_star + beta_b * D_star**2
    return delta * (1.0 - math.exp(-a)) * math.exp(-b)

def survival_IMK(cell_line, field, D, scatter_OF=0.0):
    """
    Compute predicted surviving fraction for combined TE+NTE.
    field = 'MF_inField' | 'MF_outField' | 'UF'
    D: nominal delivered dose.
      MF_inField: D is delivered to in-field cells; out-of-field receives scatter_OF (default 0)
      MF_outField: in-field cells get D; this cell is out-of-field, gets scatter_OF
      UF: all cells get D (D_IF = D_* = D)
    Uses the field-specific DNA-TE params (MF or UF) per Table 1, and the cell-line-wide IC params.
    """
    ic = IC_PARAMS[cell_line]
    if field == 'UF':
        p = PARAMS[f'{cell_line}_UF']
        gamma_star = GAMMA_IF  # uniform = all in-field
        D_IF = D
        D_star = D
    elif field == 'MF_inField':
        p = PARAMS[f'{cell_line}_MF']
        gamma_star = GAMMA_IF
        D_IF = D
        D_star = D
    elif field == 'MF_outField':
        p = PARAMS[f'{cell_line}_MF']
        gamma_star = GAMMA_OF
        D_IF = D
        D_star = scatter_OF
    else:
        raise ValueError(field)

    wT = w_TE(D_star, p['alpha0'], p['beta0'], gamma_star)
    wN = w_NT(D_IF, D_star, ic['alpha_b'], ic['beta_b'], ic['delta'],
              GAMMA_IF, gamma_star)
    return math.exp(-(wT + wN)), wT, wN


def main():
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(out_dir, exist_ok=True)

    print(f'GAMMA_IF = {GAMMA_IF:.4f} Gy   (y_D={Y_D_IF} keV/um)')
    print(f'GAMMA_OF = {GAMMA_OF:.4f} Gy   (y_D={Y_D_OF} keV/um)')

    doses = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    results = {
        'gamma_IF_Gy': round(GAMMA_IF, 5),
        'gamma_OF_Gy': round(GAMMA_OF, 5),
        'params_TE': PARAMS,
        'params_IC': IC_PARAMS,
        'doses_Gy': doses,
        'predictions': {}
    }

    for cell in ['AGO1522', 'DU145']:
        results['predictions'][cell] = {}
        for field in ['MF_inField', 'MF_outField', 'UF']:
            curve = []
            for D in doses:
                S, wT, wN = survival_IMK(cell, field, D)
                curve.append({
                    'D': D, 'S': round(S, 6),
                    'wT': round(wT, 5), 'wN': round(wN, 5),
                    'S_TEonly': round(math.exp(-wT), 6),
                })
            results['predictions'][cell][field] = curve

    # Also: comparison table at canonical doses 2, 4, 6 Gy
    print('\n=== Full IMK predictions (S = TE + NTE) ===')
    print(f'{"Cell":<10} {"Field":<13} {"D=2Gy":>10} {"D=4Gy":>10} {"D=6Gy":>10}')
    for cell in ['AGO1522', 'DU145']:
        for field in ['MF_inField', 'MF_outField', 'UF']:
            vals = []
            for D in [2.0, 4.0, 6.0]:
                S, _, _ = survival_IMK(cell, field, D)
                vals.append(f'{S:10.4g}')
            print(f'{cell:<10} {field:<13} {vals[0]} {vals[1]} {vals[2]}')

    print('\n=== TE-only (Eq 2) — what the old SPOT-CHECK computed ===')
    print(f'{"Cell":<10} {"Field":<13} {"D=2Gy":>10} {"D=4Gy":>10} {"D=6Gy":>10}')
    for cell in ['AGO1522', 'DU145']:
        for field in ['MF_inField', 'UF']:
            vals = []
            for D in [2.0, 4.0, 6.0]:
                _, wT, _ = survival_IMK(cell, field, D)
                vals.append(f'{math.exp(-wT):10.4g}')
            print(f'{cell:<10} {field:<13} {vals[0]} {vals[1]} {vals[2]}')

    out_path = os.path.join(out_dir, 'imk_full_predictions.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'\nWrote: {out_path}')


if __name__ == '__main__':
    main()
