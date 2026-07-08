"""
Test: Validate analytic solution against numerical Lindblad integration.

For small N (2-4 ions), compare:
1. Analytic m-body correlation functions (Eqs. 6-10)
2. Numerical scipy ODE integration of full Lindblad equation

These should agree to near machine precision.
"""
import sys
sys.path.insert(0, '..')
import numpy as np
from src.scattering_rates import compute_scattering_rates
from src.analytic_solution import (
    correlation_function, correlation_permutation_invariant,
    total_factor, sinc, f_func
)
from src.numerical_solution import (
    solve_master_equation, extract_sigma_plus_correlation,
    extract_correlation_numerical
)


def test_sinc():
    """Test sinc function."""
    assert abs(sinc(np.array([0.0+0j]))[0] - 1.0) < 1e-15
    assert abs(sinc(np.array([np.pi+0j]))[0] - 0.0) < 1e-15  # sin(pi)/pi ~ 0
    x = 1.5
    assert abs(sinc(np.array([x+0j]))[0] - np.sin(x)/x) < 1e-15
    print("  sinc: PASS")


def test_no_scattering_limit():
    """
    With zero scattering rates, analytic solution should give ideal Ising evolution.
    For |+>^N under H = J/N * sum sigma_z^i sigma_z^j:
    <sigma_1^+ sigma_2^+> = (1/4) * cos(2Jt/N)   [for N=2]
    """
    N = 2
    J_val = 1.0
    J_matrix = np.array([[0, J_val], [J_val, 0]])
    
    # Zero scattering rates
    rates = compute_scattering_rates(0.0)
    
    t_vals = np.linspace(0, 2.0, 50)
    
    for t in t_vals:
        # Analytic: 2-body correlation with both + signs
        corr = correlation_function([0, 1], [1, 1], J_matrix, t, rates, N)
        # Ideal: <sigma_1^+ sigma_2^+> = (1/4) * exp(2iJt/N)
        # Wait - with zero scattering: s = 2J/N, lambda=0, Delta=0
        # I(J_eff, t) = cos(s*t) = cos(2*J_eff*t/N)
        # For m=2, no spectator ions, so product is empty = 1
        # Result: exp(-2*Gamma*t)/4 * 1 = 1/4
        # But with Gamma=0: result = 1/4
        # Hmm, this is just the prefactor. The time dependence comes from the Hamiltonian
        # For N=2 with M={0,1}, there are no spectator ions
        # So <sigma_1^+ sigma_2^+> = e^{-2Gt}/4 = 1/4 for G=0
        # But the ideal evolution gives <sigma_1^+ sigma_2^+> = (1/4)*e^{2iJt/N}
        # The Hamiltonian phase is NOT captured in the correlation function formula?
        
        # Actually, re-reading the paper: the Ising Hamiltonian H = (1/N)sum J_{ij} sigma_z^i sigma_z^j
        # Under H, |+>^N evolves. The exact evolution of sigma^+ sigma^+ involves
        # the Hamiltonian contribution through the spectator terms.
        # For N=2 with M={0,1}: no spectators, so the product is trivial.
        # The only time dependence is from e^{-2Gt}.
        # The Hamiltonian evolution for the m=N correlation is:
        # e^{-2Gt}/4 * (no spectator product)
        # This means for m=N, the correlation is just exponential decay!
        # That makes sense: if ALL ions are in the correlation, there are no
        # spectators to produce any oscillation.
        
        expected = 0.25  # 1/2^2, no time dependence for m=N with G=0
        assert abs(corr - expected) < 1e-12, f"t={t}: got {corr}, expected {expected}"
    
    print("  no_scattering_limit (m=N): PASS")


def test_analytic_vs_numerical_N2():
    """
    Compare analytic and numerical for N=2 with scattering.
    """
    N = 2
    J_val = 5.0  # coupling
    J_matrix = np.array([[0, J_val], [J_val, 0]])
    
    # Moderate scattering
    total_scatter = 2.0  # s^-1
    rates = compute_scattering_rates(total_scatter)
    
    t_end = 0.5
    t_eval = np.linspace(0, t_end, 20)
    
    print(f"  N=2, J={J_val}, total_scatter={total_scatter}")
    print(f"  Rates: G={rates['G']:.4f}, G_R={rates['G_R']:.4f}, G_L={rates['G_L']:.4f}")
    
    # Numerical solution
    sol, H, jumps = solve_master_equation(N, J_matrix, rates, (0, t_end), t_eval)
    
    # Extract <sigma_1^+> (1-body) numerically
    num_1body = extract_sigma_plus_correlation(sol, N, [0])
    
    # Analytic 1-body: M={0}, nu={+1}
    ana_1body = np.array([
        correlation_function([0], [1], J_matrix, t, rates, N)
        for t in t_eval
    ])
    
    max_err_1body = np.max(np.abs(num_1body - ana_1body))
    print(f"  1-body max error: {max_err_1body:.2e}")
    
    # Extract <sigma_1^+ sigma_2^+> (2-body) numerically
    num_2body = extract_sigma_plus_correlation(sol, N, [0, 1])
    
    # Analytic 2-body: M={0,1}, nu={+1,+1}
    ana_2body = np.array([
        correlation_function([0, 1], [1, 1], J_matrix, t, rates, N)
        for t in t_eval
    ])
    
    max_err_2body = np.max(np.abs(num_2body - ana_2body))
    print(f"  2-body max error: {max_err_2body:.2e}")
    
    return max_err_1body, max_err_2body


def test_analytic_vs_numerical_N3():
    """Compare analytic and numerical for N=3."""
    N = 3
    J_val = 3.0
    J_matrix = J_val * (np.ones((N, N)) - np.eye(N))  # uniform coupling
    
    total_scatter = 1.5
    rates = compute_scattering_rates(total_scatter)
    
    t_end = 0.3
    t_eval = np.linspace(0, t_end, 15)
    
    print(f"\n  N=3, J={J_val}, total_scatter={total_scatter}")
    
    # Numerical
    sol, H, jumps = solve_master_equation(N, J_matrix, rates, (0, t_end), t_eval)
    
    # 1-body correlation <sigma_0^+>
    num_1body = extract_sigma_plus_correlation(sol, N, [0])
    ana_1body = np.array([
        correlation_function([0], [1], J_matrix, t, rates, N)
        for t in t_eval
    ])
    
    max_err = np.max(np.abs(num_1body - ana_1body))
    print(f"  1-body max error: {max_err:.2e}")
    
    # 2-body correlation <sigma_0^+ sigma_1^+>
    num_2body = extract_sigma_plus_correlation(sol, N, [0, 1])
    ana_2body = np.array([
        correlation_function([0, 1], [1, 1], J_matrix, t, rates, N)
        for t in t_eval
    ])
    
    max_err_2 = np.max(np.abs(num_2body - ana_2body))
    print(f"  2-body max error: {max_err_2:.2e}")
    
    return max_err, max_err_2


def test_permutation_invariant_vs_general():
    """
    For uniform coupling, permutation-invariant formula should match general formula.
    """
    N = 4
    J_val = 2.0
    J_matrix = J_val * (np.ones((N, N)) - np.eye(N))
    
    total_scatter = 3.0
    rates = compute_scattering_rates(total_scatter)
    
    t = 0.2
    
    # General formula: 2-body, ions 0,1, both +
    gen = correlation_function([0, 1], [1, 1], J_matrix, t, rates, N)
    
    # Permutation invariant: m=2, nu=(+1,+1)
    perm = correlation_permutation_invariant(2, (1, 1), J_val, t, rates, N)
    
    err = abs(gen - perm)
    print(f"\n  Permutation invariant vs general (N=4, m=2): error = {err:.2e}")
    assert err < 1e-12, f"Mismatch: gen={gen}, perm={perm}"
    print("  PASS")


def test_initial_conditions():
    """Test that at t=0, correlations have correct values."""
    N = 3
    J_val = 1.0
    J_matrix = J_val * (np.ones((N, N)) - np.eye(N))
    rates = compute_scattering_rates(5.0)
    
    t = 0.0
    
    # <sigma^+> at t=0 for |+>^N: <+|sigma^+|+> = <+| |0><1| |+> = (1/2)
    corr_1 = correlation_function([0], [1], J_matrix, t, rates, N)
    assert abs(corr_1 - 0.5) < 1e-12, f"1-body at t=0: {corr_1}"
    
    # <sigma^+ sigma^+> at t=0: (1/2)^2 = 1/4
    corr_2 = correlation_function([0, 1], [1, 1], J_matrix, t, rates, N)
    assert abs(corr_2 - 0.25) < 1e-12, f"2-body at t=0: {corr_2}"
    
    # <sigma^+ sigma^+ sigma^+> at t=0: (1/2)^3 = 1/8
    corr_3 = correlation_function([0, 1, 2], [1, 1, 1], J_matrix, t, rates, N)
    assert abs(corr_3 - 0.125) < 1e-12, f"3-body at t=0: {corr_3}"
    
    print("\n  Initial conditions: PASS")


if __name__ == '__main__':
    print("Running validation tests...")
    print("\n1. sinc function:")
    test_sinc()
    
    print("\n2. Initial conditions:")
    test_initial_conditions()
    
    print("\n3. No-scattering limit:")
    test_no_scattering_limit()
    
    print("\n4. Permutation invariant vs general:")
    test_permutation_invariant_vs_general()
    
    print("\n5. Analytic vs Numerical (N=2):")
    err1_2, err2_2 = test_analytic_vs_numerical_N2()
    
    print("\n6. Analytic vs Numerical (N=3):")
    err1_3, err2_3 = test_analytic_vs_numerical_N3()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    all_pass = True
    for name, err, tol in [
        ("N=2 1-body", err1_2, 1e-6),
        ("N=2 2-body", err2_2, 1e-6),
        ("N=3 1-body", err1_3, 1e-6),
        ("N=3 2-body", err2_3, 1e-6),
    ]:
        status = "PASS" if err < tol else "FAIL"
        if err >= tol:
            all_pass = False
        print(f"  {name}: {err:.2e} (tol={tol:.0e}) [{status}]")
    
    if all_pass:
        print("\nAll tests PASSED!")
    else:
        print("\nSome tests FAILED - investigation needed")
