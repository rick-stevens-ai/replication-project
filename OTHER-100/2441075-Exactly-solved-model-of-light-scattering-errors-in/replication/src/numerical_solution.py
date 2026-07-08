"""
Numerical solution of the Lindblad master equation using scipy ODE integration.

Implements direct numerical integration of:
  drho/dt = -i[H, rho] + sum_alpha (J_alpha rho J_alpha^dag - {J_alpha^dag J_alpha, rho}/2)

For validation against the analytic solution.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm


def basis_state(label, N):
    """
    Create computational basis state vector for N qubits.
    Each qubit has 3 levels: |0>, |1>, |g>
    label: string of length N with characters '0', '1', 'g'
    """
    dim = 3**N
    idx = 0
    for i, c in enumerate(label):
        if c == '0':
            idx += 0 * 3**(N - 1 - i)
        elif c == '1':
            idx += 1 * 3**(N - 1 - i)
        elif c == 'g':
            idx += 2 * 3**(N - 1 - i)
    state = np.zeros(dim, dtype=complex)
    state[idx] = 1.0
    return state


def single_ion_op(op_matrix, ion_idx, N):
    """
    Create N-ion operator from single-ion 3x3 matrix acting on ion ion_idx.
    """
    result = np.eye(1)
    for i in range(N):
        if i == ion_idx:
            result = np.kron(result, op_matrix)
        else:
            result = np.kron(result, np.eye(3))
    return result


def build_operators(N, J_matrix, rates):
    """
    Build Hamiltonian and jump operators for N ions with 3 levels each.
    
    Qubit levels: |0> (index 0), |1> (index 1), |g> (index 2)
    
    Parameters:
        N: number of ions
        J_matrix: NxN coupling matrix
        rates: scattering rates dict
    
    Returns:
        H: Hamiltonian matrix
        jump_ops: list of jump operators
    """
    dim = 3**N
    
    # Single-ion operators (3x3 matrices)
    proj_0 = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=complex)  # |0><0|
    proj_1 = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=complex)  # |1><1|
    proj_g = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]], dtype=complex)  # |g><g|
    sigma_z = proj_0 - proj_1  # |0><0| - |1><1|
    
    # Transition operators
    op_0to1 = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)  # |1><0|
    op_1to0 = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]], dtype=complex)  # |0><1|
    op_0tog = np.array([[0, 0, 0], [0, 0, 0], [1, 0, 0]], dtype=complex)  # |g><0|
    op_1tog = np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0]], dtype=complex)  # |g><1|
    
    # Build Hamiltonian: H = (1/N) sum_{i<j} J_{ij} sigma_z^i sigma_z^j
    # But the paper uses H_arm = N^{-1} sum_{i<j} J_{ij} |0_i 0_j><0_i 0_j|
    # For spin-echo, this becomes the Ising Hamiltonian
    # Use sigma_z formulation: H = (1/N) sum_{i<j} J_{ij} sigma_z^i sigma_z^j
    H = np.zeros((dim, dim), dtype=complex)
    for i in range(N):
        for j in range(i + 1, N):
            sz_i = single_ion_op(sigma_z, i, N)
            sz_j = single_ion_op(sigma_z, j, N)
            H += J_matrix[i, j] / N * sz_i @ sz_j
    
    # Build jump operators
    jump_ops = []
    G_el = rates['G_el']
    G0_to_1 = rates['G0_to_1']
    G1_to_0 = rates['G1_to_0']
    G0_to_g = rates['G0_to_g']
    G1_to_g = rates['G1_to_g']
    
    # Paper convention: D(rho) = 2 * sum J rho J^dag with J^(el) = sqrt(G_el/8)*sigma_z
    # Standard Lindblad: sum L rho L^dag - {L^dag L, rho}/2
    # Relationship: L_k = sqrt(2) * J_k
    # So: L^(el) = sqrt(G_el/4)*sigma_z, L^(a->b) = sqrt(G^(a->b))*|b><a|
    
    for j in range(N):
        # Elastic scattering
        if G_el > 0:
            jump_ops.append(np.sqrt(G_el / 4.0) * single_ion_op(sigma_z, j, N))
        
        # Raman: |0> -> |1>
        if G0_to_1 > 0:
            jump_ops.append(np.sqrt(G0_to_1) * single_ion_op(op_0to1, j, N))
        
        # Raman: |1> -> |0>
        if G1_to_0 > 0:
            jump_ops.append(np.sqrt(G1_to_0) * single_ion_op(op_1to0, j, N))
        
        # Leakage: |0> -> |g>
        if G0_to_g > 0:
            jump_ops.append(np.sqrt(G0_to_g) * single_ion_op(op_0tog, j, N))
        
        # Leakage: |1> -> |g>
        if G1_to_g > 0:
            jump_ops.append(np.sqrt(G1_to_g) * single_ion_op(op_1tog, j, N))
    
    return H, jump_ops


def lindblad_rhs(rho, H, jump_ops, dim):
    """
    Compute drho/dt = -i[H, rho] + sum_k (L_k rho L_k^dag - {L_k^dag L_k, rho}/2)
    """
    rho = rho.reshape(dim, dim)
    drho = -1j * (H @ rho - rho @ H)
    
    for L in jump_ops:
        Ld = L.conj().T
        LdL = Ld @ L
        drho += L @ rho @ Ld - 0.5 * (LdL @ rho + rho @ LdL)
    
    return drho.reshape(-1)


def solve_master_equation(N, J_matrix, rates, t_span, t_eval=None, initial_state=None):
    """
    Numerically solve the Lindblad master equation.
    
    Parameters:
        N: number of ions
        J_matrix: NxN coupling matrix
        rates: scattering rates dict
        t_span: (t_start, t_end) tuple
        t_eval: times at which to evaluate solution
        initial_state: initial density matrix (default: |+>^N)
    
    Returns:
        sol: solution object with sol.t and sol.y (density matrices)
    """
    dim = 3**N
    H, jump_ops = build_operators(N, J_matrix, rates)
    
    if initial_state is None:
        # |+> = (|0> + |1>) / sqrt(2) for each ion
        plus = np.array([1, 1, 0], dtype=complex) / np.sqrt(2)
        psi0 = plus
        for i in range(N - 1):
            psi0 = np.kron(psi0, plus)
        rho0 = np.outer(psi0, psi0.conj())
    else:
        rho0 = initial_state
    
    def rhs(t, y):
        return lindblad_rhs(y, H, jump_ops, dim)
    
    y0 = rho0.reshape(-1)
    
    sol = solve_ivp(rhs, t_span, y0, t_eval=t_eval, 
                    method='RK45', rtol=1e-10, atol=1e-12)
    
    return sol, H, jump_ops


def extract_correlation_numerical(sol, N, m, direction='x'):
    """
    Extract m-body correlation <sigma_direction^{otimes m}> from numerical solution.
    
    Parameters:
        sol: solution from solve_master_equation
        N: number of ions
        m: number of ions in correlation
        direction: 'x', 'y', or 'z'
    """
    dim = 3**N
    
    # Build the m-body operator
    if direction == 'x':
        single_op = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    elif direction == 'y':
        single_op = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    elif direction == 'z':
        single_op = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
    
    # Build tensor product of m copies on first m ions, identity on rest
    op = np.eye(1, dtype=complex)
    for i in range(N):
        if i < m:
            op = np.kron(op, single_op)
        else:
            op = np.kron(op, np.eye(3))
    
    # Compute Tr(op * rho(t)) for each time
    n_times = len(sol.t)
    correlations = np.zeros(n_times, dtype=complex)
    for k in range(n_times):
        rho_k = sol.y[:, k].reshape(dim, dim)
        correlations[k] = np.trace(op @ rho_k)
    
    return correlations


def extract_sigma_plus_correlation(sol, N, M_indices):
    """
    Extract <prod_{j in M} sigma_j^+> from numerical solution.
    
    sigma^+ = |0><1| in our convention
    """
    dim = 3**N
    sigma_plus_3 = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]], dtype=complex)
    
    op = np.eye(1, dtype=complex)
    for i in range(N):
        if i in M_indices:
            op = np.kron(op, sigma_plus_3)
        else:
            op = np.kron(op, np.eye(3))
    
    n_times = len(sol.t)
    correlations = np.zeros(n_times, dtype=complex)
    for k in range(n_times):
        rho_k = sol.y[:, k].reshape(dim, dim)
        correlations[k] = np.trace(op @ rho_k)
    
    return correlations
