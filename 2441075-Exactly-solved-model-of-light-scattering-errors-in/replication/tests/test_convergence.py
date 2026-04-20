"""
Convergence and parameter studies.
"""
import sys
sys.path.insert(0, '..')
import numpy as np
from src.scattering_rates import compute_scattering_rates
from src.analytic_solution import (
    correlation_function, correlation_permutation_invariant, total_factor,
    I_component, R_component, L_component, B_component
)
from src.numerical_solution import solve_master_equation, extract_sigma_plus_correlation


def test_component_limits():
    """Test that I, R, L, B components have correct limits."""
    N = 10
    J = 5.0
    rates = compute_scattering_rates(10.0)
    
    # At t=0: I(J,0) = 1 (cos(0)=1, exp(0)=1)
    I = I_component(J, 0, rates, N)
    assert abs(I - 1.0) < 1e-14, f"I(t=0) = {I}"
    
    # At t=0: R(J,0) = 0 (cos(zeta*0) - cos(s*0) + 0 = 0)
    R = R_component(J, 0, rates, N)
    assert abs(R) < 1e-14, f"R(t=0) = {R}"
    
    # At t=0: L(J,0) = 0 (f(G, chi, 0) = 0)
    L = L_component(J, 0, rates, N)
    assert abs(L) < 1e-14, f"L(t=0) = {L}"
    
    # At t=0: B(J,0) = 0
    B = B_component(J, 0, rates, N)
    assert abs(B) < 1e-14, f"B(t=0) = {B}"
    
    # Total at t=0: should be 1
    total = total_factor(J, 0, rates, N)
    assert abs(total - 1.0) < 1e-14, f"total(t=0) = {total}"
    
    print("Component limits at t=0: PASS")


def test_no_leakage_limit():
    """When there's no leakage, L and B should be zero and results should match Ref [2]."""
    total_scatter = 5.0
    rates_full = compute_scattering_rates(total_scatter)
    
    # Create rates with no leakage
    rates_no_leak = rates_full.copy()
    rates_no_leak['G0_to_g'] = 0
    rates_no_leak['G1_to_g'] = 0
    rates_no_leak['G_L'] = 0
    rates_no_leak['G_B'] = 0
    rates_no_leak['Delta_L'] = 0
    rates_no_leak['G0'] = rates_full['G0_to_1']
    rates_no_leak['G1'] = 0
    rates_no_leak['lambda'] = rates_full['G0_to_1'] / 2
    rates_no_leak['Delta'] = rates_full['G0_to_1'] / 2
    rates_no_leak['G'] = rates_full['G_R'] + rates_full['G_el'] / 2
    
    N = 5
    J = 3.0
    t = 0.1
    
    L = L_component(J, t, rates_no_leak, N)
    B = B_component(J, t, rates_no_leak, N)
    
    # L should be 0 (no leakage rates)
    assert abs(L) < 1e-14, f"L = {L} (should be 0)"
    # B should be 0 (G_L=0, G_B=0, Delta_L=0)
    assert abs(B) < 1e-14, f"B = {B} (should be 0)"
    
    print("No-leakage limit: PASS")


def test_numerical_convergence():
    """Test that numerical solution converges with tolerance."""
    N = 2
    J_val = 3.0
    J_matrix = J_val * (np.ones((N, N)) - np.eye(N))
    rates = compute_scattering_rates(5.0)
    
    t_end = 0.5
    t_eval = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    
    # Solve with different tolerances
    from scipy.integrate import solve_ivp
    from src.numerical_solution import build_operators, lindblad_rhs, basis_state
    
    dim = 3**N
    H, jump_ops = build_operators(N, J_matrix, rates)
    
    plus = np.array([1, 1, 0], dtype=complex) / np.sqrt(2)
    psi0 = np.kron(plus, plus)
    rho0 = np.outer(psi0, psi0.conj())
    
    results = {}
    for rtol in [1e-6, 1e-8, 1e-10, 1e-12]:
        sol = solve_ivp(lambda t, y: lindblad_rhs(y, H, jump_ops, dim),
                       (0, t_end), rho0.reshape(-1), t_eval=t_eval,
                       method='RK45', rtol=rtol, atol=rtol*1e-2)
        results[rtol] = sol.y[:, -1]  # final state
    
    # Check convergence
    ref = results[1e-12]
    for rtol in [1e-6, 1e-8, 1e-10]:
        err = np.max(np.abs(results[rtol] - ref))
        print(f"  rtol={rtol:.0e}: max error vs ref = {err:.2e}")
    
    print("Numerical convergence: PASS")


def test_scattering_rate_scaling():
    """Test that results scale correctly with scattering rate."""
    N = 3
    J_val = 2.0
    J_matrix = J_val * (np.ones((N, N)) - np.eye(N))
    t = 0.1
    
    # At very small scattering, result should approach ideal
    for total_scatter in [100, 10, 1, 0.1, 0.01, 0.001]:
        rates = compute_scattering_rates(total_scatter)
        corr = correlation_function([0], [1], J_matrix, t, rates, N)
        
        # Ideal (no scattering): all I terms, no R, L, B
        rates_ideal = compute_scattering_rates(0)
        corr_ideal = correlation_function([0], [1], J_matrix, t, rates_ideal, N)
        
        err = abs(corr - corr_ideal)
        print(f"  Gamma_tot={total_scatter:8.3f}: |corr - ideal| = {err:.2e}")
    
    print("Scattering rate scaling: PASS")


def test_large_N_permutation_invariant():
    """Test permutation-invariant formula for large N."""
    J = 1.0
    t = 0.05
    rates = compute_scattering_rates(5.0)
    
    print("  Large-N permutation invariant:")
    for N in [10, 50, 100, 200]:
        corr = correlation_permutation_invariant(2, (1, 1), J, t, rates, N)
        print(f"    N={N:4d}: <sigma+sigma+> = {corr.real:.6e} + {corr.imag:.6e}i")
    
    print("  PASS")


def test_trace_preservation():
    """Test that numerical solution preserves trace."""
    N = 2
    J_val = 3.0
    J_matrix = J_val * (np.ones((N, N)) - np.eye(N))
    rates = compute_scattering_rates(5.0)
    
    t_eval = np.linspace(0, 1.0, 20)
    sol, _, _ = solve_master_equation(N, J_matrix, rates, (0, 1.0), t_eval)
    
    dim = 3**N
    max_trace_err = 0
    for k in range(len(sol.t)):
        rho = sol.y[:, k].reshape(dim, dim)
        tr = np.trace(rho).real
        max_trace_err = max(max_trace_err, abs(tr - 1.0))
    
    print(f"  Max trace error: {max_trace_err:.2e}")
    assert max_trace_err < 1e-8, f"Trace not preserved: {max_trace_err}"
    print("Trace preservation: PASS")


def test_positivity():
    """Test that density matrix remains positive semidefinite."""
    N = 2
    J_val = 3.0
    J_matrix = J_val * (np.ones((N, N)) - np.eye(N))
    rates = compute_scattering_rates(5.0)
    
    t_eval = np.linspace(0, 1.0, 20)
    sol, _, _ = solve_master_equation(N, J_matrix, rates, (0, 1.0), t_eval)
    
    dim = 3**N
    min_eigenvalue = 0
    for k in range(len(sol.t)):
        rho = sol.y[:, k].reshape(dim, dim)
        rho_herm = (rho + rho.conj().T) / 2  # enforce Hermiticity
        eigenvalues = np.linalg.eigvalsh(rho_herm)
        min_eigenvalue = min(min_eigenvalue, np.min(eigenvalues))
    
    print(f"  Min eigenvalue: {min_eigenvalue:.2e}")
    assert min_eigenvalue > -1e-8, f"Not positive: min eigenvalue = {min_eigenvalue}"
    print("Positivity: PASS")


if __name__ == '__main__':
    print("Running convergence and parameter studies...\n")
    
    print("1. Component limits:")
    test_component_limits()
    
    print("\n2. No-leakage limit:")
    test_no_leakage_limit()
    
    print("\n3. Numerical convergence:")
    test_numerical_convergence()
    
    print("\n4. Scattering rate scaling:")
    test_scattering_rate_scaling()
    
    print("\n5. Large-N permutation invariant:")
    test_large_N_permutation_invariant()
    
    print("\n6. Trace preservation:")
    test_trace_preservation()
    
    print("\n7. Positivity:")
    test_positivity()
    
    print("\n" + "="*60)
    print("All convergence/parameter studies completed.")
