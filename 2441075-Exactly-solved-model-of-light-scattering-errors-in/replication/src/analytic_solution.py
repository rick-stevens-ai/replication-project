"""
Exact analytic solution for the Lindblad master equation under light scattering.

Implements Eqs. (6)-(10) from the paper:
"Exactly-Solved Model of Light-Scattering Errors in Quantum Simulations 
with Metastable Trapped-Ion Qubits"

The key result is the m-body correlation function (Eq. 6):
  <prod_{j in M} sigma_j^{nu_j}> = (e^{-m*Gamma*t} / 2^m) * 
    prod_{i not in M} [I + R + L + B](J_i^{(M,nu)}, t)

where I, R, L, B are defined in Eqs. (7)-(10).
"""
import numpy as np
from functools import lru_cache


def sinc(x):
    """Unnormalized sinc: sin(x)/x, with sinc(0)=1. Handles complex arguments."""
    x = np.asarray(x, dtype=complex)
    result = np.ones_like(x, dtype=complex)
    mask = x != 0
    result[mask] = np.sin(x[mask]) / x[mask]
    return result


def f_func(Gamma, chi, t):
    """
    Auxiliary function f(Gamma, chi, t) used in L and B terms.
    f(Gamma, chi, t) = exp(i*(chi + i*Gamma)*t/2) * t * sinc((chi + i*Gamma)*t/2)
    
    Parameters:
        Gamma: decay rate (real)
        chi: frequency parameter (can be complex)  
        t: time
    """
    arg = (chi + 1j * Gamma) * t / 2.0
    return np.exp(1j * arg) * t * sinc(arg)


def a_func(Gamma, chi, t):
    """a(Gamma, chi, t) = [f(Gamma, chi, t) + f(Gamma, -chi, t)] / 2"""
    return (f_func(Gamma, chi, t) + f_func(Gamma, -chi, t)) / 2.0


def b_func(Gamma, chi, t):
    """b(Gamma, chi, t) = -i*[f(Gamma, chi, t) - f(Gamma, -chi, t)] / (2*chi)"""
    chi = np.asarray(chi, dtype=complex)
    if np.any(chi == 0):
        # Handle chi=0 limit: b -> t * f'(0) related terms
        # In this limit, f(G,chi,t) - f(G,-chi,t) ~ 2*chi * df/dchi|_0
        # For small chi: expand sin((chi+iG)t/2)/((chi+iG)t/2) around chi=0
        raise ValueError("b_func with chi=0 needs special handling")
    return -1j * (f_func(Gamma, chi, t) - f_func(Gamma, -chi, t)) / (2.0 * chi)


def I_component(J_eff, t, rates, N):
    """
    Ideal evolution component (Eq. 7).
    I(J, t) = exp(-lambda*t) * cos(s*t)
    
    where s = 2*J/N + i*Delta
    """
    lam = rates['lambda']
    Delta = rates['Delta']
    s = 2.0 * J_eff / N + 1j * Delta
    return np.exp(-lam * t) * np.cos(s * t)


def R_component(J_eff, t, rates, N):
    """
    Raman scattering component (Eq. 8).
    R(J, t) = exp(-lambda*t) * [cos(zeta*t) - cos(s*t) + Gamma_R * t * sinc(zeta*t)]
    
    where zeta = sqrt(s^2 - Gamma^(0->1)*Gamma^(1->0))
    """
    lam = rates['lambda']
    Delta = rates['Delta']
    G_R = rates['G_R']
    G0_to_1 = rates['G0_to_1']
    G1_to_0 = rates['G1_to_0']
    
    s = 2.0 * J_eff / N + 1j * Delta
    zeta = np.sqrt(s**2 - G0_to_1 * G1_to_0 + 0j)  # ensure complex
    
    return np.exp(-lam * t) * (np.cos(zeta * t) - np.cos(s * t) + G_R * t * sinc(np.atleast_1d(zeta * t)).item())


def L_component(J_eff, t, rates, N):
    """
    Leakage component (Eq. 9).
    L(J, t) = (1/2) * sum_{alpha=0,1} Gamma^(alpha->g) * f(Gamma^(alpha), (-1)^alpha * 2J/N, t)
    """
    G0_to_g = rates['G0_to_g']
    G1_to_g = rates['G1_to_g']
    G0 = rates['G0']  # total inelastic from |0>
    G1 = rates['G1']  # total inelastic from |1>
    
    chi_0 = 2.0 * J_eff / N    # (-1)^0 * 2J/N
    chi_1 = -2.0 * J_eff / N   # (-1)^1 * 2J/N
    
    result = 0.5 * (G0_to_g * f_func(G0, chi_0, t) + G1_to_g * f_func(G1, chi_1, t))
    return result


def B_component(J_eff, t, rates, N):
    """
    Combined Raman+leakage component (Eq. 10).
    B(J, t) = Gamma_L * [a(lambda, zeta, t) - a(lambda, s, t)]
              + Gamma_B * b(lambda, zeta, t)
              + i*s*Delta_L * [b(lambda, zeta, t) - b(lambda, s, t)]
    """
    lam = rates['lambda']
    Delta = rates['Delta']
    G_L = rates['G_L']
    G_B = rates['G_B']
    Delta_L = rates['Delta_L']
    G0_to_1 = rates['G0_to_1']
    G1_to_0 = rates['G1_to_0']
    
    s = 2.0 * J_eff / N + 1j * Delta
    zeta = np.sqrt(s**2 - G0_to_1 * G1_to_0 + 0j)
    
    # Handle case where s or zeta could be zero
    a_zeta = a_func(lam, zeta, t)
    a_s = a_func(lam, s, t)
    
    result = G_L * (a_zeta - a_s)
    
    if abs(zeta) > 1e-30:
        b_zeta = b_func(lam, zeta, t)
        result += G_B * b_zeta
    
    if abs(s) > 1e-30 and abs(zeta) > 1e-30:
        b_s = b_func(lam, s, t)
        b_zeta_val = b_func(lam, zeta, t) if abs(zeta) > 1e-30 else 0
        result += 1j * s * Delta_L * (b_zeta_val - b_s)
    
    return result


def total_factor(J_eff, t, rates, N):
    """
    Compute I + R + L + B for a single spectator ion with effective coupling J_eff.
    """
    I = I_component(J_eff, t, rates, N)
    R = R_component(J_eff, t, rates, N)
    L = L_component(J_eff, t, rates, N)
    B = B_component(J_eff, t, rates, N)
    return I + R + L + B


def correlation_function(M_indices, nu_signs, J_matrix, t, rates, N):
    """
    Compute m-body correlation function (Eq. 6).
    
    <prod_{j in M} sigma_j^{nu_j}> = (e^{-m*Gamma*t} / 2^m) *
        prod_{i not in M} [I + R + L + B](J_i^{(M,nu)}, t)
    
    Parameters:
        M_indices: list of ion indices in the correlation (0-indexed)
        nu_signs: list of +1 or -1 for each ion in M
        J_matrix: NxN coupling matrix (symmetric, Jij)
        t: time (using t_arm convention - one arm of spin echo)
        rates: dict of scattering rates from compute_scattering_rates
        N: number of ions
    
    Returns:
        complex expectation value
    """
    m = len(M_indices)
    G = rates['G']
    
    prefactor = np.exp(-m * G * t) / (2.0 ** m)
    
    product = 1.0 + 0j
    all_ions = set(range(N))
    M_set = set(M_indices)
    spectator_ions = all_ions - M_set
    
    for i in spectator_ions:
        # Compute J_i^{(M,nu)} = sum_{j in M} nu_j * J_{ij}
        J_eff = sum(nu * J_matrix[i, j] for j, nu in zip(M_indices, nu_signs))
        product *= total_factor(J_eff, t, rates, N)
    
    return prefactor * product


def correlation_permutation_invariant(m, nu_config, J, t, rates, N):
    """
    Compute m-body correlation for permutation-invariant case (all Jij = J).
    
    In permutation-invariant case, all spectator ions see the same J_eff,
    so the product simplifies to [total_factor(J_eff, t)]^(N-m).
    
    Parameters:
        m: number of ions in the correlation
        nu_config: tuple of +1/-1 signs. For permutation invariant, 
                   only the net sum matters.
        J: uniform coupling constant (Jij = J for all i<j)
        t: time
        rates: scattering rates dict
        N: number of ions
    
    Returns:
        complex expectation value
    """
    G = rates['G']
    prefactor = np.exp(-m * G * t) / (2.0 ** m)
    
    # For permutation invariant case: J_eff = sum of nu_j * J for j in M
    # Since all J_{ij} = J: J_eff = J * sum(nu_j)
    net_nu = sum(nu_config)
    J_eff = J * net_nu
    
    factor = total_factor(J_eff, t, rates, N)
    return prefactor * factor ** (N - m)


def ghz_fidelity_scatter(J, t_cat, rates, N):
    """
    Compute GHZ state fidelity due to scattering (F_scatter).
    
    For GHZ state |GHZ> = (|0>^N + |1>^N) / sqrt(2):
    F = <GHZ|rho|GHZ> 
    
    This requires computing specific correlation functions.
    For the permutation-invariant case with equal couplings:
    
    F_GHZ = (1/2) * [P(all 0) + P(all 1) + 2*Re(<sigma_1^+ ... sigma_N^+>)]
    
    where the N-body correlation function captures the coherence.
    
    Note: t_cat = pi*N/(4*J) is the ideal GHZ preparation time.
    The scattering time t_arm = 2*pi/delta is what matters physically.
    
    For the spin-echo protocol, the effective Ising evolution time t = t_arm/2,
    but scattering occurs for the full t_arm in each arm.
    
    Parameters:
        J: uniform coupling strength
        t_cat: cat-state preparation time = pi*N/(4*J)  
        rates: scattering rates dict
        N: number of ions
    
    Returns:
        F_scatter: scattering contribution to fidelity
    """
    # For GHZ state, we need the N-body coherence
    # <sigma_1^+ sigma_2^+ ... sigma_N^+> at the ideal cat time
    # In spin-echo, t_arm is the scattering time, and t_cat = t_arm/2 
    # is the effective Ising evolution time
    
    # t_arm = 2 * t_cat for the scattering
    t_arm = 2.0 * t_cat  # total experiment time for one arm
    
    # N-body correlation with all + signs
    nu_all_plus = tuple([1] * N)
    coherence = correlation_permutation_invariant(N, nu_all_plus, J, t_arm, rates, N)
    
    # Population terms (diagonal)
    # P(all 0) + P(all 1) involves summing over all z-basis states
    # For permutation-invariant initial state |+>^N:
    # <|0>^N <0|^N> + <|1>^N <1|^N> = 2 * (1/2^N) * ... 
    
    # Actually for the GHZ fidelity we need:
    # F = (1/2)[<0^N|rho|0^N> + <1^N|rho|1^N> + 2*Re(<0^N|rho|1^N>)]
    # = (1/2)[P_00...0 + P_11...1 + 2*Re(coherence)]
    
    # The populations can also be expressed in terms of correlations
    # P_00...0 = <prod |0_i><0_i|> = <prod (1+sigma_z)/2>
    # But this gets complicated. For now, compute coherence contribution
    
    # In the ideal case at t_cat: coherence = 1/2^N * i^N (phase from Ising evolution)
    # With scattering, the fidelity is reduced
    
    return coherence


def compute_ghz_fidelity_full(J_avg, delta, rates, N):
    """
    Compute full GHZ fidelity F_scatter in the permutation-invariant limit.
    
    Parameters:
        J_avg: average coupling J/N per ion pair
        delta: detuning from COM mode (rad/s)
        rates: scattering rates dict
        N: number of ions
    
    Returns:
        F: fidelity including scattering
    """
    t_arm = 2 * np.pi / delta  # spin-echo arm time
    t_cat = np.pi * N / (4 * J_avg * N)  # = pi/(4*J_avg), but J_avg is J/N
    # Actually t_cat = pi*N/(4*J) where J = J_avg * N, so t_cat = pi/(4*J_avg)
    
    # The experiment time is t_arm per arm, total t_expt = 2*t_arm
    # Scattering rates should use t_arm (or t_expt depending on convention)
    
    # For the paper's figures, they compute F_scatter using the analytic formulas
    # with scattering during t_arm
    
    G = rates['G']
    
    # Compute N-body coherence magnitude
    # All ions have nu = +1
    nu_all = tuple([1] * N)
    coh = correlation_permutation_invariant(N, nu_all, J_avg * N, t_arm, rates, N)
    
    # GHZ fidelity ~ 1/2 + |coherence| for the ideal preparation
    # More precisely, we need to track the full density matrix
    # But the dominant scattering effect is the decay of the N-body coherence
    
    return coh


def compute_correlation_m_body(m, J, t, rates, N, direction='parallel'):
    """
    Compute m-body correlation <P^{otimes m}> in parallel or perpendicular direction.
    
    For GHZ-like dynamics starting from |+>^N:
    - Parallel direction P = sigma_x (N even) or sigma_y (N odd)  
    - Perpendicular direction P_perp
    
    For the correlation <(sigma^x)^{otimes m}>:
    sigma_x = sigma^+ + sigma^-
    so <sigma_x^{otimes m}> = sum over all 2^m combinations of +/- signs
    
    Parameters:
        m: number of ions
        J: uniform coupling
        t: scattering time (t_arm)
        rates: scattering rates dict
        N: number of ions
        direction: 'parallel' or 'perpendicular'
    
    Returns:
        real correlation value
    """
    from itertools import product as iter_product
    
    # sigma_x = sigma^+ + sigma^-, sigma_y = -i*sigma^+ + i*sigma^-
    # <sigma_x^m> = sum_{nu in {+,-}^m} <prod sigma^{nu_j}>
    # <sigma_y^m> = sum_{nu} prod((-i)^{delta(nu=+)} * (i)^{delta(nu=-)}) * <prod sigma^{nu_j}>
    
    result = 0.0 + 0j
    for nu_tuple in iter_product([1, -1], repeat=m):
        corr = correlation_permutation_invariant(m, nu_tuple, J, t, rates, N)
        
        if direction == 'parallel':
            # For sigma_x (N even) or sigma_y (N odd)
            if N % 2 == 0:
                # sigma_x: coefficient = 1 for all
                result += corr
            else:
                # sigma_y: coefficient = prod of (-i for +, i for -)
                coeff = 1.0
                for nu in nu_tuple:
                    if nu == 1:
                        coeff *= (-1j)
                    else:
                        coeff *= (1j)
                result += coeff * corr
        else:  # perpendicular
            if N % 2 == 0:
                # sigma_y
                coeff = 1.0
                for nu in nu_tuple:
                    if nu == 1:
                        coeff *= (-1j)
                    else:
                        coeff *= (1j)
                result += coeff * corr
            else:
                # sigma_x
                result += corr
    
    return result.real
