"""
Penning trap ion crystal simulation for computing coupling matrix Jij.

Following Ref. [20]: Wang et al., Phys. Rev. A 87, 013422 (2013).

For a 2D planar crystal in a Penning trap:
- Axial confinement at frequency omega_z
- Rotation at frequency omega_r  
- Ions form a triangular lattice for large N

The coupling matrix is:
  J_{ij} = N * Omega_i * Omega_j * sum_m [eta_{i,m} * eta_{j,m} * omega_m / (mu^2 - omega_m^2)]

For simplicity in replication, we use the key properties:
1. Near COM mode, couplings are approximately uniform: J_{ij} ≈ J
2. Variance sigma^2(J_{ij}) decreases with higher B field
3. The COM mode gives the dominant contribution when delta << delta_{m!=0}
"""
import numpy as np
from scipy.optimize import minimize


def compute_1d_ion_positions(N):
    """
    Compute equilibrium positions of N ions in a 1D harmonic trap.
    Positions in units of the characteristic length scale.
    """
    if N == 1:
        return np.array([0.0])
    
    # Initial guess: spread uniformly
    x0 = np.linspace(-N**(1/3), N**(1/3), N)
    
    def energy(x):
        # Harmonic + Coulomb
        E = 0.5 * np.sum(x**2)
        for i in range(N):
            for j in range(i+1, N):
                E += 1.0 / abs(x[i] - x[j])
        return E
    
    def gradient(x):
        g = x.copy()  # harmonic part
        for i in range(N):
            for j in range(N):
                if i != j:
                    g[i] -= np.sign(x[i] - x[j]) / (x[i] - x[j])**2
        return g
    
    result = minimize(energy, x0, jac=gradient, method='L-BFGS-B')
    return np.sort(result.x)


def compute_normal_modes_1d(positions, omega_z=1.0):
    """
    Compute normal mode frequencies and eigenvectors for 1D ion chain.
    
    Parameters:
        positions: equilibrium positions
        omega_z: axial trap frequency (used as unit)
    
    Returns:
        frequencies: mode frequencies
        eigenvectors: NxN matrix where column m is eigenvector of mode m
    """
    N = len(positions)
    
    # Hessian of the potential
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                d = abs(positions[i] - positions[j])
                A[i, j] = -2.0 / d**3
                A[i, i] += 2.0 / d**3
        A[i, i] += omega_z**2
    
    # Diagonalize
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    frequencies = np.sqrt(np.abs(eigenvalues))
    
    # Sort by frequency
    idx = np.argsort(frequencies)
    frequencies = frequencies[idx]
    eigenvectors = eigenvectors[:, idx]
    
    return frequencies, eigenvectors


def compute_coupling_matrix(N, omega_z, mu, laser_intensity_profile=None):
    """
    Compute the Ising coupling matrix Jij for N ions.
    
    Parameters:
        N: number of ions
        omega_z: axial trap frequency (Hz or rad/s - sets the scale)
        mu: laser beatnote frequency
        laser_intensity_profile: function(position) -> relative intensity
                                 (default: uniform)
    
    Returns:
        J_matrix: NxN coupling matrix
        mode_freqs: normal mode frequencies
    """
    positions = compute_1d_ion_positions(N)
    frequencies, eigenvectors = compute_normal_modes_1d(positions, omega_z)
    
    # Lamb-Dicke parameters: eta_{i,m} = b_{i,m} * eta_0 / sqrt(N)
    # where b_{i,m} is the eigenvector component
    # For simplicity, eta_0 is absorbed into the overall coupling scale
    
    if laser_intensity_profile is None:
        Omega = np.ones(N)  # uniform illumination
    else:
        Omega = np.array([laser_intensity_profile(p) for p in positions])
    
    J = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            for m in range(N):
                J[i, j] += (Omega[i] * Omega[j] * 
                           eigenvectors[i, m] * eigenvectors[j, m] * 
                           frequencies[m] / (mu**2 - frequencies[m]**2))
    J *= N  # Factor of N from the definition
    
    return J, frequencies


def compute_uniform_coupling(N, delta, omega_z=1.0):
    """
    Compute approximate uniform coupling J when detuning delta << mode spacing.
    
    Near the COM mode (mode 0, all ions in phase):
    J_{ij} ≈ J = N * eta^2 * omega_COM / (2*delta*omega_COM)
            ≈ N * eta^2 / (2*delta)
    
    Returns J/N (the coupling per pair normalized by N).
    """
    # COM mode frequency
    positions = compute_1d_ion_positions(N)
    freqs, _ = compute_normal_modes_1d(positions, omega_z)
    omega_COM = freqs[0]
    
    # mu = omega_COM + delta
    mu = omega_COM + delta
    
    # J/N ≈ omega_COM / (mu^2 - omega_COM^2) ≈ 1/(2*delta) for small delta
    J_over_N = omega_COM / (mu**2 - omega_COM**2)
    
    return J_over_N


def compute_Jij_variance(N, omega_z, delta):
    """
    Compute variance of Jij/N for given parameters.
    Used for F_unequal estimate.
    """
    positions = compute_1d_ion_positions(N)
    freqs, eigvecs = compute_normal_modes_1d(positions, omega_z)
    
    mu = freqs[0] + delta  # detune from COM
    
    J, _ = compute_coupling_matrix(N, omega_z, mu)
    J_normalized = J / N
    
    # Extract unique off-diagonal elements
    J_pairs = []
    for i in range(N):
        for j in range(i+1, N):
            J_pairs.append(J_normalized[i, j])
    J_pairs = np.array(J_pairs)
    
    J_avg = np.mean(J_pairs)
    J_var = np.var(J_pairs)
    
    return J_avg, J_var, J_pairs
