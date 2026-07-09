"""Generate response-function plot: for a range of x in [-1,1], plot the
Im[U[0,0]] channel of the QSVT unitary (which realises P(x)) and compare to
target sign(x) plus its polynomial approximation."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.special
from numpy.polynomial.chebyshev import chebval
from pyqsp.angle_sequence import QuantumSignalProcessingPhases
from pyqsp.poly import PolyTaylorSeries

def build_be(x):
    return np.array([[x, 1j*np.sqrt(1-x**2)],
                     [1j*np.sqrt(1-x**2), x]], dtype=complex)

def qsvt(phases, x):
    def R(phi):
        return np.diag([np.exp(1j*phi), np.exp(-1j*phi)])
    U = R(phases[0])
    W = build_be(x)
    for k in range(1, len(phases)):
        U = U @ W @ R(phases[k])
    return U

fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

for ax, deg in zip(axes, [11, 21, 41]):
    delta = 0.2
    kappa = 2.0/delta
    cheb = PolyTaylorSeries().taylor_series(
        func=lambda x: scipy.special.erf(kappa*x),
        degree=deg, max_scale=0.9, chebyshev_basis=True, cheb_samples=2*deg)
    coeffs = np.asarray(cheb.coef if hasattr(cheb,'coef') else cheb)
    coeffs[0::2] = 0.0
    phiset,_,_ = QuantumSignalProcessingPhases(coeffs, signal_operator="Wx",
                                               method="sym_qsp", chebyshev_basis=True)
    xs = np.linspace(-1, 1, 401)
    poly_vals = chebval(xs, coeffs)
    qsvt_vals = np.array([qsvt(np.array(phiset), x)[0,0].imag for x in xs])
    ax.plot(xs, np.sign(xs), 'k--', lw=1, label='ideal sign(x)')
    ax.plot(xs, poly_vals, 'b-', lw=1.5, alpha=0.7, label=f'poly (deg {deg})')
    ax.plot(xs, qsvt_vals, 'r:', lw=2, label='Im[U₀₀] via QSVT')
    ax.axvline(delta, color='gray', ls=':', alpha=0.5)
    ax.axvline(-delta, color='gray', ls=':', alpha=0.5)
    ax.set_xlabel('x (eigenvalue)')
    ax.set_ylabel('polynomial value')
    ax.set_title(f'Sign approx via QSVT, deg={deg}, δ={delta}')
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(alpha=0.3)

plt.suptitle('Replication of QSVT/QEVT sign-function eigenvalue transformation\n(arXiv:2401.06240, Low & Su)')
plt.tight_layout()
plt.savefig('/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-200/QC-2401.06240-quantum-eigenvalue-processing-low-su/report/evidence/qsvt_sign_response.png', dpi=120)
print("saved qsvt_sign_response.png")
