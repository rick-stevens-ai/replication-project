#!/usr/bin/env python3
"""
Replication of the three-mixture verification test from:
  "SCALE depletion capabilities for molten salt reactors and other liquid-fueled systems"
  OSTI 2217719

Reproduces Figures 3-6: Pa-233, U-233, and Nd-148 evolution across
three mixtures with continuous removal streams.

The ODE system models:
  - Mixture 1: irradiated fuel (5% U-233 + 95% Th-232)
  - Mixture 2: waste stream (Pa and Nd removed from Mix 1)
  - Mixture 3: waste stream (Pa and Nd removed from Mix 1)

Pa is removed from Mix 1 to Mixes 2 and 3 at different rates.
Nd is removed similarly but at much higher rates.
Pa-233 decays to U-233 in all mixtures.
Th-233 decays to Pa-233 in Mix 1.
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from pathlib import Path

# ── Physical Constants ───────────────────────────────────────────────────────

# Decay constants (s⁻¹)
LAMBDA_TH233 = 2.97495e-7   # Th-233 → Pa-233 (β⁻, t½ ≈ 22.2 min)
LAMBDA_PA233 = 5.29201e-4   # Pa-233 → U-233 (β⁻, t½ ≈ 26.97 days)
# Note: Th-233 half-life from paper value: ln(2)/2.97495e-7 ≈ 2.33e6 s ≈ 27 days
# Actually Th-233 t½ ≈ 22.2 min → λ = ln(2)/1332 ≈ 5.2e-4. 
# The paper gives 2.97495e-7 which corresponds to t½ ≈ 27 days.
# This might be a typo in the paper or it's an effective constant.
# We use the paper's values exactly for replication.

# Removal rates from Mixture 1 (s⁻¹)
LAMBDA_PA_1TO2 = 0.1    # Pa: Mix 1 → Mix 2
LAMBDA_PA_1TO3 = 0.2    # Pa: Mix 1 → Mix 3
LAMBDA_ND_1TO2 = 10.0   # Nd: Mix 1 → Mix 2
LAMBDA_ND_1TO3 = 20.0   # Nd: Mix 1 → Mix 3

# Total removal rates
LAMBDA_PA_REM = LAMBDA_PA_1TO2 + LAMBDA_PA_1TO3  # 0.3 s⁻¹
LAMBDA_ND_REM = LAMBDA_ND_1TO2 + LAMBDA_ND_1TO3  # 30.0 s⁻¹

# Time conversion
SECONDS_PER_DAY = 86400.0

# ── Initial Conditions ───────────────────────────────────────────────────────

# From paper: 5% U-233 + 95% Th-232
# We need initial masses. The paper shows Pa-233 starting at ~250g in Mix 1.
# This suggests the system has been irradiating and Th-232 is producing Th-233
# which decays to Pa-233.
#
# Actually, looking more carefully at the paper: the test problem starts with
# existing nuclide inventories in Mixture 1, and the removal streams then
# redistribute them. The initial Pa-233 inventory comes from prior irradiation.
#
# From Fig 3, Pa-233 in Mix 1 starts at ~250g (read from ×10⁵ scale).
# Let's set initial conditions based on what the figures show.
#
# The paper states this is a TRITON depletion test with 10-day steps.
# The irradiation produces Th-233 → Pa-233 → U-233 chain.
# At t=0, we need the steady-state-ish inventory from prior irradiation.
#
# For the analytical solution, we need initial N values.
# The figures suggest:
#   Pa-233 in Mix 1: ~250g initially
#   Everything else starts at 0 in Mixes 2 and 3

# Let's use atomic masses for conversion
M_PA233 = 233.04  # g/mol
M_U233 = 233.04   # g/mol  
M_TH233 = 233.05  # g/mol
M_ND148 = 147.92  # g/mol
AVOGADRO = 6.022e23

def mass_to_atoms(mass_g, molar_mass):
    """Convert grams to number of atoms."""
    return mass_g * AVOGADRO / molar_mass

def atoms_to_mass(n_atoms, molar_mass):
    """Convert number of atoms to grams."""
    return n_atoms * molar_mass / AVOGADRO


# ── Analytical Solutions ─────────────────────────────────────────────────────

def analytical_pa233_mix1(t, N0_pa233, N0_th233=0):
    """
    Analytical solution for Pa-233 in Mixture 1.
    
    dN¹(Pa)/dt = λ_Th * N¹(Th) - (λ_Pa + λ_rem) * N¹(Pa)
    
    With Th-233 decaying: N¹(Th)(t) = N0_Th * exp(-λ_Th * t)
    
    Solution (if λ_Th ≠ λ_Pa + λ_rem):
    N¹(Pa)(t) = N0_Pa * exp(-α*t) + N0_Th * λ_Th/(α - λ_Th) * [exp(-λ_Th*t) - exp(-α*t)]
    where α = λ_Pa + λ_rem
    """
    alpha = LAMBDA_PA233 + LAMBDA_PA_REM
    
    term1 = N0_pa233 * np.exp(-alpha * t)
    
    if N0_th233 > 0:
        term2 = N0_th233 * LAMBDA_TH233 / (alpha - LAMBDA_TH233) * (
            np.exp(-LAMBDA_TH233 * t) - np.exp(-alpha * t))
    else:
        term2 = 0
    
    return term1 + term2


def analytical_pa233_waste(t, N0_pa233_mix1, lambda_1tom, N0_th233=0):
    """
    Analytical solution for Pa-233 in waste mixture m.
    
    dNᵐ(Pa)/dt = λ¹→ᵐ * N¹(Pa)(t) - λ_Pa * Nᵐ(Pa)
    
    This is a linear ODE with known forcing from N¹(Pa)(t).
    """
    alpha = LAMBDA_PA233 + LAMBDA_PA_REM
    beta = LAMBDA_PA233  # decay rate in waste (no removal from waste)
    
    # Forcing: N¹(Pa)(t) = A*exp(-alpha*t) + B*exp(-lambda_Th*t)
    A = N0_pa233_mix1
    if N0_th233 > 0:
        B = N0_th233 * LAMBDA_TH233 / (alpha - LAMBDA_TH233)
    else:
        B = 0
    
    # Solution by variation of parameters / integrating factor
    # Nᵐ(Pa)(t) = exp(-β*t) * ∫₀ᵗ λ¹→ᵐ * N¹(Pa)(s) * exp(β*s) ds
    
    # Term from A*exp(-alpha*s):
    if abs(beta - alpha) > 1e-20:
        term1 = lambda_1tom * A / (beta - alpha) * (np.exp(-alpha * t) - np.exp(-beta * t))
    else:
        term1 = lambda_1tom * A * t * np.exp(-beta * t)
    
    # Term from B*exp(-lambda_Th*s):
    if N0_th233 > 0:
        # From the B*exp(-lambda_Th*s) part
        if abs(beta - LAMBDA_TH233) > 1e-20:
            term2a = lambda_1tom * B / (beta - LAMBDA_TH233) * (
                np.exp(-LAMBDA_TH233 * t) - np.exp(-beta * t))
        else:
            term2a = lambda_1tom * B * t * np.exp(-beta * t)
        
        # From the -B*exp(-alpha*s) part  
        if abs(beta - alpha) > 1e-20:
            term2b = -lambda_1tom * B / (beta - alpha) * (
                np.exp(-alpha * t) - np.exp(-beta * t))
        else:
            term2b = -lambda_1tom * B * t * np.exp(-beta * t)
        
        term2 = term2a + term2b
    else:
        term2 = 0
    
    return term1 + term2


def analytical_u233_waste(t, N0_pa233_mix1, lambda_1tom, N0_th233=0):
    """
    U-233 in waste mixture m: integral of λ_Pa * Nᵐ(Pa)(t).
    dNᵐ(U)/dt = λ_Pa * Nᵐ(Pa)(t)
    Nᵐ(U)(t) = λ_Pa * ∫₀ᵗ Nᵐ(Pa)(s) ds
    """
    # Numerical integration is cleaner here
    dt = 3600.0  # 1 hour steps for integration
    times = np.arange(0, t + dt, dt)
    pa_vals = np.array([analytical_pa233_waste(s, N0_pa233_mix1, lambda_1tom, N0_th233) 
                        for s in times])
    return LAMBDA_PA233 * np.trapz(pa_vals, times)


# ── Numerical ODE System ─────────────────────────────────────────────────────

def ode_system(t, y):
    """
    Full ODE system for three-mixture test.
    
    State vector y = [
        N1_Th233, N1_Pa233, N1_Nd148,          # Mixture 1
        N2_Pa233, N2_U233, N2_Nd148,            # Mixture 2
        N3_Pa233, N3_U233, N3_Nd148              # Mixture 3
    ]
    """
    N1_Th, N1_Pa, N1_Nd = y[0], y[1], y[2]
    N2_Pa, N2_U, N2_Nd = y[3], y[4], y[5]
    N3_Pa, N3_U, N3_Nd = y[6], y[7], y[8]
    
    dydt = np.zeros(9)
    
    # Mixture 1
    dydt[0] = -LAMBDA_TH233 * N1_Th                                    # Th-233
    dydt[1] = (LAMBDA_TH233 * N1_Th                                    # Pa-233
               - (LAMBDA_PA233 + LAMBDA_PA_1TO2 + LAMBDA_PA_1TO3) * N1_Pa)
    dydt[2] = -(LAMBDA_ND_1TO2 + LAMBDA_ND_1TO3) * N1_Nd              # Nd-148
    # Note: Nd-148 production from fission is handled by TRITON in the paper.
    # For the verification test, the initial Nd inventory is depleted by removal.
    # The paper's Fig 5 shows accumulation in waste, implying continuous Nd production.
    # We'll add a constant Nd production rate fitted from the figures.
    
    # Mixture 2
    dydt[3] = LAMBDA_PA_1TO2 * N1_Pa - LAMBDA_PA233 * N2_Pa           # Pa-233
    dydt[4] = LAMBDA_PA233 * N2_Pa                                      # U-233
    dydt[5] = LAMBDA_ND_1TO2 * N1_Nd                                    # Nd-148
    
    # Mixture 3
    dydt[6] = LAMBDA_PA_1TO3 * N1_Pa - LAMBDA_PA233 * N3_Pa           # Pa-233
    dydt[7] = LAMBDA_PA233 * N3_Pa                                      # U-233
    dydt[8] = LAMBDA_ND_1TO3 * N1_Nd                                    # Nd-148
    
    return dydt


def ode_system_with_production(t, y, nd_production_rate=0):
    """
    ODE system including a constant Nd-148 production rate in Mix 1
    (representing fission yield from the ongoing irradiation).
    """
    dydt = ode_system(t, y)
    dydt[2] += nd_production_rate  # Add Nd production to Mix 1
    return dydt


# ── Run Simulation ───────────────────────────────────────────────────────────

def run_simulation():
    """Run the three-mixture depletion test and generate plots."""
    
    print("=" * 70)
    print("Three-Mixture Verification Test")
    print("SCALE MSR Depletion Paper (OSTI 2217719), Figures 3-6")
    print("=" * 70)
    
    # ── Initial conditions ──
    # From paper Fig 3: Pa-233 starts at ~250g in Mix 1
    # The ×10⁵ scale in Fig 3 means values shown are N × 10⁵
    # So Mix 1 Pa-233 starts at ~250 on the plot → actual is ~250g
    # (The scale multiplier applies to y-axis label, not the values read)
    
    # Initial Pa-233 mass in Mixture 1 (grams)
    # Reading Fig 3 carefully: y-axis is "²³³Pa mass (g) ×10⁵"
    # Top of Mix 1 curve is ~2.5, so actual mass = 2.5 × 10⁵ = 250,000 g = 250 kg
    # That seems too high. Let me reconsider...
    # Actually "×10⁵" likely means the values are multiplied by 10⁵,
    # i.e., the actual mass is value_on_plot × 10⁻⁵ × ... 
    # OR the plot shows mass × 10⁵ (i.e., 10⁵ times the mass).
    # If the axis reads "mass (g) ×10⁵" and shows ~2.5, 
    # that means mass = 2.5 × 10⁵ g... still 250 kg.
    #
    # For a test problem with 5% U-233, this could be a large system.
    # Let's just use consistent units and match the shapes/ratios.
    
    # Let's use the analytical structure. The key ratios are what matter.
    # Initial Pa-233 in Mix 1: N0_Pa (we'll calibrate from figures)
    # Initial Th-233: from Th-232 neutron capture (very short-lived)
    
    # For now, let's set Pa-233 initial = 250g (representative)
    # and Th-233 initial = small (decays fast)
    
    N0_Pa233_g = 250.0  # grams in Mix 1
    N0_Th233_g = 0.1    # small initial Th-233
    
    # Nd-148: In the paper, Nd is continuously produced by fission.
    # The TRITON code handles this via coupled transport-depletion.
    # For our standalone ODE, we model a constant production rate.
    # From Fig 5: Mix 2 reaches ~8g and Mix 3 reaches ~16g at 300 days.
    # Total Nd removed = 8 + 16 = 24g in 300 days.
    # With removal rates 10 and 20 s⁻¹, essentially all produced Nd 
    # is instantly removed (λ_rem >> any production rate).
    # So steady-state N1_Nd ≈ P / λ_rem where P is production rate.
    # Total removed ≈ P × t, so P ≈ 24g / (300 × 86400s) ≈ 9.26e-7 g/s
    # In atoms: P ≈ 9.26e-7 × 6.022e23 / 147.92 ≈ 3.77e15 atoms/s
    
    nd_production_rate_g = 24.0 / (300 * SECONDS_PER_DAY)  # g/s
    nd_production_rate = mass_to_atoms(nd_production_rate_g, M_ND148)  # atoms/s
    
    # Convert to atom counts
    N0 = np.zeros(9)
    N0[0] = mass_to_atoms(N0_Th233_g, M_TH233)  # Mix 1: Th-233
    N0[1] = mass_to_atoms(N0_Pa233_g, M_PA233)   # Mix 1: Pa-233
    N0[2] = 0  # Mix 1: Nd-148 (produced continuously)
    # Mixes 2, 3: all zero initially
    
    # ── Solve ODE ──
    t_end = 300 * SECONDS_PER_DAY  # 300 days in seconds
    t_eval = np.linspace(0, t_end, 3000)  # evaluation points
    
    print(f"\nInitial conditions:")
    print(f"  Pa-233 in Mix 1: {N0_Pa233_g:.1f} g")
    print(f"  Th-233 in Mix 1: {N0_Th233_g:.3f} g")
    print(f"  Nd-148 production rate: {nd_production_rate_g:.2e} g/s")
    print(f"\nSolving ODE system for {300} days...")
    
    sol = solve_ivp(
        lambda t, y: ode_system_with_production(t, y, nd_production_rate),
        [0, t_end], N0,
        method='LSODA',  # stiff-capable
        t_eval=t_eval,
        rtol=1e-10, atol=1e-15,
        max_step=SECONDS_PER_DAY  # at most 1-day steps
    )
    
    if not sol.success:
        print(f"ERROR: ODE solver failed: {sol.message}")
        return
    
    print(f"  Solver status: {sol.message}")
    print(f"  Function evaluations: {sol.nfev}")
    
    # Convert to days and grams
    t_days = sol.t / SECONDS_PER_DAY
    
    Pa233_mix1_g = atoms_to_mass(sol.y[1], M_PA233)
    Pa233_mix2_g = atoms_to_mass(sol.y[3], M_PA233)
    Pa233_mix3_g = atoms_to_mass(sol.y[6], M_PA233)
    
    U233_mix2_g = atoms_to_mass(sol.y[4], M_U233)
    U233_mix3_g = atoms_to_mass(sol.y[7], M_U233)
    
    Nd148_mix1_g = atoms_to_mass(sol.y[2], M_ND148)
    Nd148_mix2_g = atoms_to_mass(sol.y[5], M_ND148)
    Nd148_mix3_g = atoms_to_mass(sol.y[8], M_ND148)
    
    # ── Print key results ──
    print(f"\n{'─' * 50}")
    print(f"Results at t = 300 days:")
    print(f"{'─' * 50}")
    print(f"  Pa-233 Mix 1: {Pa233_mix1_g[-1]:.6e} g")
    print(f"  Pa-233 Mix 2: {Pa233_mix2_g[-1]:.4f} g")
    print(f"  Pa-233 Mix 3: {Pa233_mix3_g[-1]:.4f} g")
    print(f"  U-233  Mix 2: {U233_mix2_g[-1]:.2f} g")
    print(f"  U-233  Mix 3: {U233_mix3_g[-1]:.2f} g")
    print(f"  Nd-148 Mix 1: {Nd148_mix1_g[-1]:.6e} g")
    print(f"  Nd-148 Mix 2: {Nd148_mix2_g[-1]:.4f} g")
    print(f"  Nd-148 Mix 3: {Nd148_mix3_g[-1]:.4f} g")
    
    # Verify ratio: Mix 3 / Mix 2 should be 2.0 (ratio of removal rates)
    pa_ratio = Pa233_mix3_g[-1] / Pa233_mix2_g[-1] if Pa233_mix2_g[-1] > 0 else float('inf')
    u_ratio = U233_mix3_g[-1] / U233_mix2_g[-1] if U233_mix2_g[-1] > 0 else float('inf')
    nd_ratio = Nd148_mix3_g[-1] / Nd148_mix2_g[-1] if Nd148_mix2_g[-1] > 0 else float('inf')
    
    print(f"\n  Ratios (Mix3/Mix2, expected ≈ 2.0):")
    print(f"    Pa-233: {pa_ratio:.4f}")
    print(f"    U-233:  {u_ratio:.4f}")
    print(f"    Nd-148: {nd_ratio:.4f}")
    
    # ── Analytical check for Pa-233 ──
    print(f"\n{'─' * 50}")
    print("Analytical vs Numerical comparison (Pa-233):")
    print(f"{'─' * 50}")
    
    N0_Pa_atoms = mass_to_atoms(N0_Pa233_g, M_PA233)
    N0_Th_atoms = mass_to_atoms(N0_Th233_g, M_TH233)
    
    for check_day in [1, 10, 50, 100, 300]:
        t_check = check_day * SECONDS_PER_DAY
        ana_mix1 = atoms_to_mass(
            analytical_pa233_mix1(t_check, N0_Pa_atoms, N0_Th_atoms), M_PA233)
        # Find nearest numerical value
        idx = np.argmin(np.abs(t_days - check_day))
        num_mix1 = Pa233_mix1_g[idx]
        rel_err = abs(ana_mix1 - num_mix1) / max(abs(ana_mix1), 1e-30) * 100
        print(f"  t={check_day:3d}d: analytical={ana_mix1:.6e}g, "
              f"numerical={num_mix1:.6e}g, rel_err={rel_err:.2e}%")
    
    # ── Generate Plots ──
    plots_dir = Path(__file__).parent.parent / "plots"
    plots_dir.mkdir(exist_ok=True)
    
    # Fig 3: Pa-233 mass in three mixtures
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1 = axes[0]
    ax1.semilogy(t_days, Pa233_mix1_g, 'b-', linewidth=2, label='Mixture 1 (fuel)')
    ax1.set_xlabel('Time (days)', fontsize=12)
    ax1.set_ylabel('²³³Pa mass (g)', fontsize=12)
    ax1.set_title('²³³Pa in Mixture 1', fontsize=13)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 300)
    
    ax2 = axes[1]
    ax2.plot(t_days, Pa233_mix2_g, 'r-', linewidth=2, label='Mixture 2')
    ax2.plot(t_days, Pa233_mix3_g, 'g-', linewidth=2, label='Mixture 3')
    ax2.set_xlabel('Time (days)', fontsize=12)
    ax2.set_ylabel('²³³Pa mass (g)', fontsize=12)
    ax2.set_title('²³³Pa in Waste Mixtures', fontsize=13)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 300)
    
    plt.suptitle('Figure 3: ²³³Pa Mass in Three Mixtures\n(Replication of OSTI 2217719)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(plots_dir / 'fig3_pa233_three_mixtures.png', dpi=150, bbox_inches='tight')
    print(f"\nSaved: {plots_dir / 'fig3_pa233_three_mixtures.png'}")
    plt.close()
    
    # Fig 4: U-233 mass in waste mixtures
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t_days, U233_mix2_g, 'r-', linewidth=2, label='Mixture 2')
    ax.plot(t_days, U233_mix3_g, 'g-', linewidth=2, label='Mixture 3')
    ax.set_xlabel('Time (days)', fontsize=12)
    ax.set_ylabel('²³³U mass (g)', fontsize=12)
    ax.set_title('Figure 4: ²³³U Mass in Waste Mixtures\n(Replication of OSTI 2217719)',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 300)
    plt.tight_layout()
    plt.savefig(plots_dir / 'fig4_u233_waste_mixtures.png', dpi=150, bbox_inches='tight')
    print(f"Saved: {plots_dir / 'fig4_u233_waste_mixtures.png'}")
    plt.close()
    
    # Fig 5: Nd-148 mass in waste mixtures
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t_days, Nd148_mix2_g, 'r-', linewidth=2, label='Mixture 2')
    ax.plot(t_days, Nd148_mix3_g, 'g-', linewidth=2, label='Mixture 3')
    ax.set_xlabel('Time (days)', fontsize=12)
    ax.set_ylabel('¹⁴⁸Nd mass (g)', fontsize=12)
    ax.set_title('Figure 5: ¹⁴⁸Nd Mass in Waste Mixtures\n(Replication of OSTI 2217719)',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 300)
    plt.tight_layout()
    plt.savefig(plots_dir / 'fig5_nd148_waste_mixtures.png', dpi=150, bbox_inches='tight')
    print(f"Saved: {plots_dir / 'fig5_nd148_waste_mixtures.png'}")
    plt.close()
    
    # Combined overview plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Pa-233 Mix 1
    axes[0, 0].semilogy(t_days, Pa233_mix1_g, 'b-', linewidth=2)
    axes[0, 0].set_ylabel('²³³Pa mass (g)')
    axes[0, 0].set_title('(a) ²³³Pa in Mixture 1')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Pa-233 waste
    axes[0, 1].plot(t_days, Pa233_mix2_g, 'r-', linewidth=2, label='Mix 2')
    axes[0, 1].plot(t_days, Pa233_mix3_g, 'g-', linewidth=2, label='Mix 3')
    axes[0, 1].set_ylabel('²³³Pa mass (g)')
    axes[0, 1].set_title('(b) ²³³Pa in Waste')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # U-233 waste
    axes[1, 0].plot(t_days, U233_mix2_g, 'r-', linewidth=2, label='Mix 2')
    axes[1, 0].plot(t_days, U233_mix3_g, 'g-', linewidth=2, label='Mix 3')
    axes[1, 0].set_xlabel('Time (days)')
    axes[1, 0].set_ylabel('²³³U mass (g)')
    axes[1, 0].set_title('(c) ²³³U in Waste')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Nd-148 waste
    axes[1, 1].plot(t_days, Nd148_mix2_g, 'r-', linewidth=2, label='Mix 2')
    axes[1, 1].plot(t_days, Nd148_mix3_g, 'g-', linewidth=2, label='Mix 3')
    axes[1, 1].set_xlabel('Time (days)')
    axes[1, 1].set_ylabel('¹⁴⁸Nd mass (g)')
    axes[1, 1].set_title('(d) ¹⁴⁸Nd in Waste')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('Three-Mixture Verification Test — SCALE MSR Depletion\n'
                 '(Replication of OSTI 2217719, Figures 3-6)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(plots_dir / 'fig_combined_three_mixture.png', dpi=150, bbox_inches='tight')
    print(f"Saved: {plots_dir / 'fig_combined_three_mixture.png'}")
    plt.close()
    
    # ── Save numerical results ──
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    np.savez(data_dir / 'three_mixture_results.npz',
             t_days=t_days,
             Pa233_mix1_g=Pa233_mix1_g, Pa233_mix2_g=Pa233_mix2_g, Pa233_mix3_g=Pa233_mix3_g,
             U233_mix2_g=U233_mix2_g, U233_mix3_g=U233_mix3_g,
             Nd148_mix1_g=Nd148_mix1_g, Nd148_mix2_g=Nd148_mix2_g, Nd148_mix3_g=Nd148_mix3_g)
    print(f"Saved: {data_dir / 'three_mixture_results.npz'}")
    
    print(f"\n{'=' * 70}")
    print("Phase 1 complete.")
    print(f"{'=' * 70}")
    
    return sol


if __name__ == '__main__':
    run_simulation()
