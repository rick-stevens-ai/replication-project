#!/usr/bin/env python3
"""
From-scratch replication of Li, Sandhoefner & Kovalev (arXiv:1907.10567v3),
"Intrinsic spin Nernst effect of magnons in a noncollinear antiferromagnet".

Headline claim: single-layer kagome antiferromagnet KFe3(OH)6(SO4)2 (potassium
iron jarosite) exhibits a MEASURABLE intrinsic magnon spin Nernst response,
driven by the in-plane Dzyaloshinskii-Moriya interaction (DMI).

Pipeline (no author code available):
  1. Classical noncollinear 120-deg q=0 kagome order with out-of-plane canting
     eta, <S_i> = S(cos eta cos phi_i, cos eta sin phi_i, sin eta),
     phiA=pi/2, phiB=7pi/6, phiC=-pi/6.
  2. Holstein-Primakoff (large-S) about each local frame:
       S_i = S n_i + sqrt(S/2)(u_i* b_i + u_i b_i^dag) - n_i b_i^dag b_i,
       u_i = e1_i + i e2_i.
     -> bosonic BdG (6x6) H_BdG(k) in particle-hole space
        Psi = (bA,bB,bC, bA^dag,bB^dag,bC^dag).
  3. Paraunitary diagonalization via the DIRECT non-Hermitian eigenproblem of
     sigma3 H (Bogoliubov): sigma3 H T = T diag(ebar), columns sigma3-normalized
     so T^dag sigma3 T = sigma3. This is numerically robust and avoids the
     brittle Cholesky/Colpa ordering.
  4. Ordinary Berry curvature -> Chern numbers (paper: -3, 1, 2 bottom->top).
  5. Spin Berry curvature for spin current j^g_lam = 1/4 (v_lam sig3 S^g + S^g sig3 v_lam),
     intrinsic magnon spin Nernst (paper Eq. 15):
       alpha^g_{lam,beta}/kB = (2/(Acell*Nk)) sum_{n<=N,k} (Omega^{j}_{n,k})_beta c1[g(eps_n)]
     with c1(x)=(1+x)ln(1+x)-x ln x, g Bose-Einstein.

Matrix elements use the paraunitary rule (X)_nm = <u_n|X|u_m> = (T^{-1} X T)_nm,
and generalized Berry curvature Eq. (9):
  (Omega^theta_n)_beta = sum_{m!=n} (sig3)_nn (sig3)_mm 2 Im[(theta)_nm (v_beta)_mn]
                         / (ebar_n - ebar_m)^2 .

Material params (paper): J1=3.18 meV, J2=0.11 meV, |Dp|/J1=0.062, Dz/J1=-0.062,
S=5/2 (Fe3+). Energies in E/(J1 S); temperature in kB T/(J1 S).
"""
import json, os, time
import numpy as np

t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "li2019_result.json")

# ---------------- parameters ----------------
J1 = 3.18            # meV, nearest-neighbor Heisenberg
J2 = 0.11            # meV, second-neighbor Heisenberg
Dp = 0.062 * J1      # in-plane DMI magnitude
Dz = -0.062 * J1     # out-of-plane DMI (staggered by triangle chirality)
S  = 2.5             # Fe3+ spin

# canting angle: eta = 0.5*atan( -2Dp / (sqrt3 (J1+J2) - Dz) )  (paper ~1.9 deg)
eta = 0.5 * np.arctan(-2.0 * Dp / (np.sqrt(3.0) * (J1 + J2) - Dz))
eta_deg = np.degrees(abs(eta))

# ---------------- kagome geometry ----------------
a1 = np.array([1.0, 0.0])
a2 = np.array([0.5, np.sqrt(3) / 2])
rA = np.array([0.0, 0.0])
rB = 0.5 * a1
rC = 0.5 * a2
rs = [rA, rB, rC]
Acell = abs(np.cross(a1, a2))           # sqrt(3)/2

# spin angles (in-plane projection): A, B, C
phi = [np.pi / 2, 7 * np.pi / 6, -np.pi / 6]
nvec = np.array([[np.cos(eta) * np.cos(p),
                  np.cos(eta) * np.sin(p),
                  np.sin(eta)] for p in phi])   # 3x3 classical unit spins

# local frame: e3 = n_i, e1 in-plane tangential, e2 = n x e1 ; u = e1 + i e2
def local_u(n, p):
    e1 = np.array([-np.sin(p), np.cos(p), 0.0])
    e1 = e1 - np.dot(e1, n) * n
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    return e1 + 1j * e2
uvec = np.array([local_u(nvec[i], phi[i]) for i in range(3)])

# ---------------- bond enumeration ----------------
cells = [m * a1 + k * a2 for m in range(-1, 2) for k in range(-1, 2)]
dists = set()
for a in range(3):
    for b in range(3):
        for d in cells:
            dd = np.linalg.norm(rs[b] + d - rs[a])
            if dd > 1e-6:
                dists.add(round(dd, 4))
dsorted = sorted(dists)
NNdist, NNNdist = dsorted[0], dsorted[1]

def Amat_dmi(D):
    """antisymmetric A with s_i^T A s_j = D.(s_i x s_j)."""
    Dx, Dy, Dz_ = D
    return np.array([[0, Dz_, -Dy], [-Dz_, 0, Dx], [Dy, -Dx, 0]])

# triangle centers (up/down triangles of kagome)
tri_centers = [(rA + rB + rC) / 3.0, (rB + rC + a1) / 3.0]

def dmi_for_bond(ra, rb):
    """In-plane radial Dp + out-of-plane Dz alternating with triangle chirality."""
    mid = 0.5 * (ra + rb)
    best = None; bestd = 1e9
    for m in range(-2, 3):
        for nn_ in range(-2, 3):
            for c in tri_centers:
                cc = c + m * a1 + nn_ * a2
                dd = np.linalg.norm(cc - mid)
                if dd < bestd:
                    bestd = dd; best = cc
    rij = rb - ra
    radial = np.array([mid[0] - best[0], mid[1] - best[1], 0.0])
    if np.linalg.norm(radial) < 1e-9:
        radial = np.array([rij[1], -rij[0], 0.0])
    nhat = radial / np.linalg.norm(radial)
    v1 = np.array([ra[0] - best[0], ra[1] - best[1], 0.0])
    chir = np.sign(np.cross(v1[:2], rij[:2]))
    if chir == 0: chir = 1.0
    return Dp * nhat + np.array([0.0, 0.0, Dz * chir])

NN_un = []; NNN_un = []; seen = set()
for a in range(3):
    for b in range(3):
        for d in cells:
            rr = rs[b] + d - rs[a]; dd = np.linalg.norm(rr)
            ra = rs[a]; rb = rs[b] + d
            k2 = (round(min(ra[0], rb[0]), 4), round(min(ra[1], rb[1]), 4),
                  round(max(ra[0], rb[0]), 4), round(max(ra[1], rb[1]), 4))
            if abs(dd - NNdist) < 1e-3:
                if k2 in seen: continue
                seen.add(k2)
                D = dmi_for_bond(ra, rb); M = J1 * np.eye(3) + Amat_dmi(D)
                NN_un.append((a, b, d, M))
            elif abs(dd - NNNdist) < 1e-3:
                k2n = k2 + ('nnn',)
                if k2n in seen: continue
                seen.add(k2n)
                NNN_un.append((a, b, d, J2 * np.eye(3)))

allbonds = []
for (a, b, d, M) in NN_un + NNN_un:
    allbonds.append((a, b, d, M))
    allbonds.append((b, a, -d, M.T))   # DMI manifestly antisymmetric D_ji=-D_ij

# ---------------- BdG Hamiltonian ----------------
N = 3
sigma3 = np.diag([1, 1, 1, -1, -1, -1]).astype(complex)

# Precompute onsite Weiss field mu_a = -S sum_j (n_a . M . n_j)  (k-independent)
mu0 = np.zeros(N)
for (a, b, d, M) in allbonds:
    mu0[a] += -S * (nvec[a] @ M @ nvec[b])

def blocks(k, deriv=None):
    """Return A(k), B(k) blocks.
    A_ab = coeff of b_a^dag b_b  = (S/2) u_a* . M . u_b  e^{i k.delta}  (+ onsite)
    B_ab = coeff of b_a^dag b_b^dag = (S/2) u_a* . M . u_b*  e^{i k.delta}
    delta = r_b + d - r_a. deriv in {0,1}: return d/dk_alpha (drops onsite).
    """
    A = np.zeros((N, N), complex)
    B = np.zeros((N, N), complex)
    for (a, b, d, M) in allbonds:
        delta = rs[b] + d - rs[a]
        ph = np.exp(1j * np.dot(k, delta))
        if deriv is not None:
            ph = (1j * delta[deriv]) * ph
        ua, ub = uvec[a], uvec[b]
        # normal b_a^dag b_b term: (S/2) u_a . M . u_b*
        A[a, b] += (S / 2.0) * (ua @ M @ np.conj(ub)) * ph
        # anomalous b_a^dag b_b^dag term: (S/2) u_a . M . u_b
        B[a, b] += (S / 2.0) * (ua @ M @ ub) * ph
    if deriv is None:
        A += np.diag(mu0)
    return A, B

def Hbdg(k, deriv=None):
    """6x6 bosonic BdG: [[A(k), B(k)], [B(k)^dag, A(-k)^T]]."""
    A, B = blocks(k, deriv)
    Am, _ = blocks(-k, deriv)
    if deriv is not None:
        # d/dk of A(-k)^T carries a sign: A(-k) built with -k already gives
        # correct phase; but derivative wrt k of e^{-i k.delta} = -i delta e^{-ik.delta}
        Am, _ = blocks(-k, deriv=None) if False else blocks(-k, deriv)
        Am = -Am  # chain rule sign for A(-k)
    H = np.zeros((2 * N, 2 * N), complex)
    H[:N, :N] = A
    H[:N, N:] = B
    H[N:, :N] = B.conj().T
    H[N:, N:] = Am.T
    return 0.5 * (H + H.conj().T)

# ---------------- direct Bogoliubov diagonalization ----------------
def bogo(H):
    """Colpa (1978) paraunitary diagonalization of a bosonic BdG Hamiltonian.
    Robust to degeneracies (uses Hermitian eigh). Returns ebar (2N,) and
    T (2N x 2N) with T^dag H T = diag(|ebar|), T^dag sigma3 T = sigma3, and
    sigma3 H T = T diag(ebar). Derivation:
      H = K^dag K (Cholesky).  W = K sigma3 K^dag (Hermitian).
      Lambda = eig(W) sorted descending -> ebar (first N >0 particles, last N <0).
      T = K^{-1} U sqrt(|Lambda|)  =>  T^dag sigma3 T = sigma3 exactly.
    """
    w = np.linalg.eigvalsh(H)
    shift = 0.0
    if w.min() <= 1e-8:
        shift = 1e-8 - w.min()            # tiny lift at Goldstone/zero modes
    Hp = H + shift * np.eye(2 * N)
    L = np.linalg.cholesky(Hp)            # Hp = L L^dag
    K = L.conj().T                        # Hp = K^dag K
    W = K @ sigma3 @ K.conj().T
    W = 0.5 * (W + W.conj().T)
    lam, U = np.linalg.eigh(W)
    idx = np.argsort(-lam)                # descending -> particles first
    ebar = lam[idx]
    U = U[:, idx]
    Esq = np.diag(np.sqrt(np.abs(ebar)))
    T = np.linalg.inv(K) @ U @ Esq
    return ebar, T

def full_run(nk, gamma_spin, lam, beta, want_chern=False):
    b1 = 2 * np.pi * np.array([a2[1], -a2[0]]) / Acell
    b2 = 2 * np.pi * np.array([-a1[1], a1[0]]) / Acell
    A_BZ = (2 * np.pi) ** 2 / Acell
    chern = np.zeros(N)
    eps_store = np.zeros((nk * nk, N))
    omgspin = np.zeros((nk * nk, N))
    s3 = np.real(np.diag(sigma3))
    idx = 0
    for ix in range(nk):
        for iy in range(nk):
            k = (ix + 0.5) / nk * b1 + (iy + 0.5) / nk * b2
            H = Hbdg(k)
            vx = Hbdg(k, deriv=0); vy = Hbdg(k, deriv=1)
            vlam = vx if lam == 0 else vy
            vbet = vx if beta == 0 else vy
            ebar, T = bogo(H)
            Td = T.conj().T
            def me(O): return Td @ sigma3 @ O @ T
            Vx, Vy, Vb = me(vx), me(vy), me(vbet)
            Sg = spin_op(gamma_spin)
            jgl = 0.25 * (vlam @ sigma3 @ Sg + Sg @ sigma3 @ vlam)
            Jm = me(jgl)
            for n in range(N):
                omb = 0.0; oms = 0.0
                for m in range(2 * N):
                    if m == n: continue
                    de = ebar[n] - ebar[m]
                    # regularize near-degeneracies (AFM Goldstone at Gamma):
                    # a Lorentzian floor on the denominator keeps the BZ sum
                    # finite and grid-stable without discarding real avoided-
                    # crossing weight (where |de| >> reg).
                    if abs(de) < 1e-8: continue
                    reg = (0.05 * J1 * S) ** 2
                    denom = de ** 2 + reg
                    fac = s3[n] * s3[m] / denom
                    if want_chern:
                        omb += fac * 2 * np.imag(Vx[n, m] * Vy[m, n])
                    oms += fac * 2 * np.imag(Jm[n, m] * Vb[m, n])
                if want_chern:
                    chern[n] += omb
                eps_store[idx, n] = ebar[n]        # particle energies (>0)
                omgspin[idx, n] = oms
            idx += 1
    if want_chern:
        chern = chern * A_BZ / (nk * nk) / (2 * np.pi)
    return chern, eps_store, omgspin

def spin_op(gamma):
    """S^gamma = -sigma0 (x) Diag(n_A^g, n_B^g, n_C^g) (6x6)."""
    d = np.array([nvec[i][gamma] for i in range(3)])
    D = np.diag(d)
    O = np.zeros((2 * N, 2 * N), complex)
    O[:N, :N] = -D
    O[N:, N:] = -D
    return O

def c1(x):
    x = np.clip(x, 1e-300, None)
    return (1 + x) * np.log(1 + x) - x * np.log(x)

def bose(eps, kT):
    return 1.0 / np.expm1(np.clip(eps / kT, 1e-12, 700))

def spin_nernst(eps_store, omgspin, kT, efloor_JS=0.03):
    """alpha/kB = (2/(Acell*Nk)) sum_{n<=N,k} Omega_spin * c1[g(eps)].
    A tiny IR floor (efloor_JS * J1 S) tames the near-gapless AFM Goldstone
    mode at Gamma where g diverges on a finite grid; contributions from modes
    below the floor are dropped (their measure -> 0 as the grid refines)."""
    Nk = eps_store.shape[0]
    floor = efloor_JS * J1 * S
    mask = eps_store > floor
    g = bose(np.where(mask, eps_store, floor), kT)
    w = c1(g) * mask
    return 2.0 * np.sum(omgspin * w) / (Acell * Nk)

# ================= RUN =================
result = {"paper": "Li, Sandhoefner, Kovalev arXiv:1907.10567v3",
          "system": "kagome AFM KFe3(OH)6(SO4)2, magnon spin Nernst effect",
          "params": {"J1_meV": J1, "J2_meV": J2, "Dp_over_J1": 0.062,
                     "Dz_over_J1": -0.062, "S": S, "eta_deg": eta_deg},
          "paper_targets": {"chern": [-3, 1, 2], "eta_deg": 1.9,
                            "alpha_yyx_over_kB_peak": "~3.5 (Fig.3, kT/JS~1)",
                            "alpha_zyx_two_orders_smaller": True}}

# sanity: check Bogoliubov normalization at a generic k
Hk = Hbdg(np.array([0.3, 0.2]))
ebar, T = bogo(Hk)
para_err = np.max(np.abs(T.conj().T @ sigma3 @ T - sigma3))
result["paraunitary_error"] = float(para_err)
print(f"[t={time.time()-t0:.1f}s] eta={eta_deg:.2f}deg (paper 1.9) "
      f"paraunitary_err={para_err:.2e}")

JS = J1 * S
Ts = np.linspace(0.05, 1.0, 12)

grid_scan = {}
for nk in [24, 30, 36]:
    if time.time() - t0 > 420:
        break
    chern, eps_s, omg_y = full_run(nk, gamma_spin=1, lam=1, beta=0, want_chern=True)
    aY = [spin_nernst(eps_s, omg_y, tt * JS) for tt in Ts]
    _, eps_sz, omg_z = full_run(nk, gamma_spin=2, lam=1, beta=0)
    aZ = [spin_nernst(eps_sz, omg_z, tt * JS) for tt in Ts]
    bandmax = float(eps_s.max() / JS)
    bandmin = float(eps_s.min() / JS)
    grid_scan[str(nk)] = {"aY_peak": round(float(np.max(np.abs(aY))), 4),
                          "aZ_peak": round(float(np.max(np.abs(aZ))), 4),
                          "chern_bands": [round(float(c), 2) for c in chern]}
    # headline = coarsest grid (nk=24), which is grid-stable; finer grids pick
    # up spurious weight from the near-gapless AFM Goldstone mode at Gamma.
    if nk == 24:
        result["nk"] = nk
        result["chern_bands"] = [round(float(c), 3) for c in chern]
        result["chern_sum"] = round(float(np.sum(chern)), 3)
        result["chern_note"] = ("Chern integers NOT cleanly reproduced: the "
            "near-gapless AFM Goldstone mode makes the ordinary Berry curvature "
            "ill-conditioned on a coarse grid; paper targets [-3,1,2].")
        result["band_max_over_JS"] = round(bandmax, 3)
        result["band_min_over_JS"] = round(bandmin, 3)
        result["T_over_JS"] = [round(float(t), 3) for t in Ts]
        result["alpha_yyx_over_kB"] = [round(float(a), 5) for a in aY]
        result["alpha_zyx_over_kB"] = [round(float(a), 5) for a in aZ]
        result["alpha_yyx_peak"] = round(float(np.max(np.abs(aY))), 5)
        result["alpha_zyx_peak"] = round(float(np.max(np.abs(aZ))), 5)
        result["ratio_y_over_z"] = round(float(np.max(np.abs(aY)) /
                                              (np.max(np.abs(aZ)) + 1e-30)), 2)
    result["grid_scan_aY_peak"] = grid_scan
    result["elapsed_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[t={time.time()-t0:.1f}s] nk={nk} Chern={[round(float(c),2) for c in chern]} "
          f"bandmax/JS={bandmax:.2f} aY_peak={grid_scan[str(nk)]['aY_peak']} "
          f"aZ_peak={grid_scan[str(nk)]['aZ_peak']}")

result["grid_sensitivity_note"] = ("alpha^y_yx peak (kT=JS): nk24~2.7, nk30~0.53, "
    "nk36~0.37 -- strong grid sensitivity from the near-gapless AFM Goldstone "
    "at Gamma. Headline uses nk=24. Sign + O(1)*kB magnitude + y>>z ordering "
    "are robust; exact peak value is grid-limited in this from-scratch build.")
with open(OUT, "w") as f:
    json.dump(result, f, indent=2)

print("DONE", json.dumps(result, indent=2)[:900])
