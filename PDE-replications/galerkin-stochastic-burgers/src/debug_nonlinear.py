"""Debug the nonlinear term computation."""

import numpy as np

# Test with simplest case: a = [1, 0, 0, ...] (only first mode)
# u(x) = √2 sin(πx)
# u'(x) = √2 π cos(πx)
# u · u' = 2π sin(πx) cos(πx) = π sin(2πx)
# -60 u u' = -60π sin(2πx)
# F_i = <-60 u u', e_i> = -60π √2 ∫_0^1 sin(2πx) sin(iπx) dx
# Using identity: sin(A)sin(B) = [cos(A-B) - cos(A+B)]/2
# = -60π √2 · (1/2) [∫cos((2-i)πx) dx - ∫cos((2+i)πx) dx]
# For i=2: first integral = ∫cos(0) dx = 1, second = ∫cos(4πx) dx = 0
# F_2 = -60π √2 · (1/2) · 1 = -30π√2

N = 8

# Analytic computation
def nonlinear_analytic(a, N):
    F = np.zeros(N)
    for j in range(1, N + 1):
        for k in range(1, N + 1):
            coeff = a[j-1] * a[k-1] * k * np.pi
            idx = j + k
            if 1 <= idx <= N:
                F[idx - 1] += coeff
            diff = j - k
            if diff > 0 and diff <= N:
                F[diff - 1] += coeff
            elif diff < 0 and -diff <= N:
                F[-diff - 1] -= coeff
    F *= -60.0
    return F

# Test case 1: only first mode
a = np.zeros(N)
a[0] = 1.0

F_expected = np.zeros(N)
F_expected[1] = -30.0 * np.pi * np.sqrt(2.0)

F_analytic = nonlinear_analytic(a, N)

print("Test: a = [1, 0, 0, ...]")
print(f"  Expected F[1] = {F_expected[1]:.6f}")
print(f"  Analytic F[1] = {F_analytic[1]:.6f}")
print(f"  F_analytic = {F_analytic}")
print()

# Let me trace the analytic calculation manually for a=[1,0,...], N=8
# j=1, k=1: coeff = 1*1*1*π = π
#   idx = j+k = 2 → F[1] += π
#   diff = j-k = 0 → skip
# All other terms are 0 since a[j-1]=0 for j>1
# F *= -60 → F[1] = -60π
print(f"  Manual: F[1] should be -60π = {-60*np.pi:.6f}")
print(f"  But expected from integral: -30π√2 = {-30*np.pi*np.sqrt(2):.6f}")
print()

# The discrepancy: the analytic formula in the code doesn't account for basis normalization.
# u(x) = Σ a_k √2 sin(kπx)
# u'(x) = Σ a_k √2 kπ cos(kπx)
# u·u' = 2 Σ_j Σ_k a_j a_k kπ sin(jπx)cos(kπx)
#       = Σ_j Σ_k a_j a_k kπ [sin((j+k)πx) + sin((j-k)πx)]
#
# F_i = <-60 u·u', e_i> = -60 √2 ∫_0^1 [above] sin(iπx) dx
#
# ∫_0^1 sin(mπx) sin(nπx) dx = δ_{mn}/2
#
# So F_i = -60 √2 Σ_{j,k} a_j a_k kπ · [δ_{i,j+k}/2 + δ_{i,|j-k|}sign(j-k)/2]
#
# For a=[1,0,...]: only j=k=1 contributes
# F_2 = -60 √2 · 1 · 1 · π · [δ_{2,2}/2] = -60√2 · π/2 = -30√2π ✓
#
# The code is MISSING the factor of √2 from the e_i projection and the factor of 1/2 
# from the orthogonality integral!

print("ROOT CAUSE: The analytic formula needs √2/2 correction")
print(f"  Code gives -60π (missing √2 * 1/2 factors from projection)")
print(f"  Correct: -60 · √2 · (1/2) · π = {-60 * np.sqrt(2) * 0.5 * np.pi:.6f}")
print(f"  Which = -30√2π = {-30*np.sqrt(2)*np.pi:.6f} ✓")
print()

# Now let me also check the pseudospectral approach
M = 1000
x = np.linspace(0, 1, M + 2)[1:-1]
k_arr = np.arange(1, N + 1)
sin_matrix = np.sin(np.outer(x, k_arr * np.pi))
cos_matrix = np.cos(np.outer(x, k_arr * np.pi))
sqrt2 = np.sqrt(2.0)

u = sqrt2 * sin_matrix @ a
u_x = sqrt2 * cos_matrix @ (a * k_arr * np.pi)
f = -60.0 * u * u_x

dx = 1.0 / (M + 1)
F_pseudo = sqrt2 * (sin_matrix.T @ f) * dx

print(f"Pseudospectral F[1] = {F_pseudo[1]:.6f}")
print(f"Expected         = {-30*np.sqrt(2)*np.pi:.6f}")
print(f"Pseudo is correct: {abs(F_pseudo[1] - (-30*np.sqrt(2)*np.pi)) < 0.1}")
print()

# So the pseudospectral is correct! The analytic needs a √2 * (1/2) factor.
# Let me write the corrected analytic formula.
print("=== Corrected analytic ===")
F_corrected = nonlinear_analytic(a, N) * np.sqrt(2) / 2.0
print(f"F[1] = {F_corrected[1]:.6f}, expected = {-30*np.sqrt(2)*np.pi:.6f}")
print(f"Match: {abs(F_corrected[1] - (-30*np.sqrt(2)*np.pi)) < 0.01}")
