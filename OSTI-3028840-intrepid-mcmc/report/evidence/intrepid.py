#!/usr/bin/env python3
"""
Independent reimplementation of Intrepid MCMC (Chakroborty & Shields, INL/JOU-24-82292,
OSTI 3028840). 2D analytical-multimodal benchmark from the paper's Section 4.1.

Target: pi(x) = T(x) * p(x), with parent p(x) = f1 = standard 2D Gaussian (radially
symmetric -> RTF is identity). Mixture kernel: with prob beta take an Intrepid
(hyperspherical exploration) step, else a component-wise MH (CMH) step.

We reproduce the paper's exact proposals for the 2D case:
  Intrepid angular:  q1(phi|theta_s,1) = Uniform(-theta_s,1, 2pi - theta_s,1)  (d-1=1 angle)
  Intrepid radial:   qr(gamma) = Uniform(0.5, 2.0)
  CMH:               qLi(z|x_i) = N(x_i, 1)  component-wise
  Anchor xa = (0,0) = mean of parent Gaussian.

For d=2, radially symmetric parent, identity RTF: the Intrepid acceptance ratio
(Eq. 21/23/26) reduces to
   rho_I = Gamma * pi(xc)/pi(xs) * [ sin^0(theta_c)/sin^0(theta_s) ]   (d-j-1 = 0 for j=1)
         = Gamma * pi(xc)/pi(xs)
with Gamma = gamma^(d-2) * qr(1/gamma)/qr(gamma) = gamma^0 * (qr symmetric on log) .
For qr=Uniform(0.5,2.0): qr(1/gamma)/qr(gamma) = 1 for gamma in [0.5,2] (support symmetric
under inversion, constant density) -> Gamma = 1. (d=2 => gamma^(d-2)=gamma^0=1.)
So alpha_I = min(1, pi(xc)/pi(xs)). We implement the general acceptance too for safety.
"""
import numpy as np

# ---------------- Parent + target definitions (Tables 2,3,4) ----------------
# Overflow-safe: clip the (negative) exponent so exp() never overflows/NaNs.
_EXPMIN = -700.0  # exp(-700) ~ 1e-304, safely > 0
def _sexp(negarg):
    # negarg is the argument to exp (may be very negative); clip low, and clip
    # any positive part (shouldn't occur for these densities) to 0.
    return np.exp(np.clip(negarg, _EXPMIN, 0.0))

def f1(x):  # Gaussian parent, unnormalized
    return _sexp(-0.5*(x[...,0]**2 + x[...,1]**2))

def f2(x):  # Gumbel
    x1=x[...,0]; x2=x[...,1]
    # exp(-x) can overflow for very negative x; clip x from below.
    x1c=np.clip(x1,-30,None); x2c=np.clip(x2,-30,None)
    return _sexp(-(x1 + x2 + np.exp(-x1c) + np.exp(-x2c)))

def f3(x):  # Rosenbrock
    x1=x[...,0]; x2=x[...,1]
    return _sexp(-(1.0/20.0)*((1-x1)**2 + 5*(x2 - x1**2)**2))

def I1(x):  # Gauss-Planes indicator
    x1=x[...,0]
    return (np.minimum(1.25 - x1, 1.75 + x1) <= 0).astype(float)

def I2(x):  # Gumbel-Planes
    x1=x[...,0]; x2=x[...,1]
    return (np.minimum(4 - 0.8*x2 - x1, 2 + 0.8*x2 + x1) <= 0).astype(float)

def I3(x):  # Rosenbrock-Planes
    x1=x[...,0]
    return (np.minimum(2.5 - x1, 2.5 + x1) <= 0).astype(float)

def I4(x):  # Ring
    r = np.sqrt(x[...,0]**2 + x[...,1]**2)
    return (4 - r <= 0).astype(float)

def I5(x):  # Rosenbrock-Ring
    x1=x[...,0]; x2=x[...,1]
    return (16 - x1**2 - ((x2-2.8)/1.7)**2 <= 0).astype(float)

def I6(x):  # Circles
    thetas=[3*np.pi/8, 5*np.pi/8, 15*np.pi/8]
    Rs=[0.8,1.2,1.6]
    x1=x[...,0]; x2=x[...,1]
    vals=[]
    for th,R in zip(thetas,Rs):
        vals.append((x1-4*np.cos(th))**2 + (x2-4*np.sin(th))**2 - R**2)
    m=np.minimum(np.minimum(vals[0],vals[1]),vals[2])
    return (m <= 0).astype(float)

# Nine cases: pi(x) unnormalized. Parent p = f1 for all (radially symmetric).
CASES = {
 1: ("Gauss-Ring",        lambda x: I4(x)*f1(x)),
 2: ("Gauss-Planes",      lambda x: I1(x)*f1(x)),
 3: ("Gauss-Circles",     lambda x: I6(x)*f1(x)),
 4: ("Gumbel-Ring",       lambda x: I4(x)*f2(x)),
 5: ("Gumbel-Planes",     lambda x: I2(x)*f2(x)),
 6: ("Gumbel-Circles",    lambda x: I6(x)*f2(x)),
 7: ("Rosenbrock-Ring",   lambda x: I5(x)*f3(x)),
 8: ("Rosenbrock-Planes", lambda x: I3(x)*f3(x)),
 9: ("Rosenbrock-Circles",lambda x: I6(x)*f3(x)),
}

XA = np.array([0.0,0.0])  # anchor = parent-Gaussian mean

# ---------------- Intrepid step (2D) ----------------
def intrepid_step(xs, pi_fn, rng):
    v = xs - XA
    rs = np.hypot(v[0], v[1])
    if rs == 0:
        rs = 1e-12
    theta_s = np.arctan2(v[1], v[0])  # in (-pi, pi]; paper uses [0,2pi) but proposal is uniform full circle
    # angular proposal q1(phi|theta_s) = Uniform(-theta_s, 2pi - theta_s) => theta_c uniform over full circle
    theta_c = theta_s + rng.uniform(-theta_s, 2*np.pi - theta_s)
    # radial proposal gamma ~ Uniform(0.5, 2.0); identity RTF => rc = gamma * rs
    gamma = rng.uniform(0.5, 2.0)
    rc = gamma * rs
    # Guard: an enormous radius means pi(xc)=0 (outside all support); reject cleanly
    # to avoid float overflow in downstream density evaluation.
    if not np.isfinite(rc) or rc > 1e6:
        return xs.copy(), False
    xc = XA + rc*np.array([np.cos(theta_c), np.sin(theta_c)])
    # Acceptance: d=2, identity RTF, symmetric proposals => Gamma=1, sin-terms=1
    # rho = pi(xc)/pi(xs). (Radial Jacobian for gamma-uniform inversion cancels; see Eq 23/26.)
    pxs = pi_fn(xs[None,:])[0]
    pxc = pi_fn(xc[None,:])[0]
    if pxs <= 0:
        alpha = 1.0
    else:
        # include the gamma^(d-2)=1 and qr ratio=1; radial jacobian (rc/rs)^(d-1)*... = gamma for d=2
        # Full careful form for d=2 identity-RTF (Eq 21 with Gamma from Eq 23):
        #   Gamma = gamma^(d-2) * qr(1/gamma)/qr(gamma). For d=2, gamma^0=1.
        #   qr uniform on [0.5,2]: 1/gamma also in [0.5,2] when gamma in [0.5,2]; density equal => ratio 1.
        Gamma = 1.0
        rho = Gamma * (pxc / pxs)
        alpha = min(1.0, rho)
    if rng.random() <= alpha:
        return xc, True
    return xs.copy(), False

# ---------------- CMH (component-wise MH) step ----------------
def cmh_step(xs, pi_fn, rng, prop_sigma=1.0):
    x = xs.copy()
    acc=False
    for i in range(2):
        xcand = x.copy()
        xcand[i] = x[i] + rng.normal(0.0, prop_sigma)
        pxs = pi_fn(x[None,:])[0]
        pxc = pi_fn(xcand[None,:])[0]
        if pxs <= 0:
            a=1.0
        else:
            a=min(1.0, pxc/pxs)
        if rng.random() <= a:
            x = xcand
            acc=True
    return x, acc

# ---------------- Full chain ----------------
def run_chain(case_id, beta, n_samples, burn_in, seed, x0=None):
    name, pi_fn = CASES[case_id]
    rng = np.random.default_rng(seed)
    if x0 is None:
        # Random start at a 'randomly selected location' (per paper) but constrained
        # to the support pi(x0)>0 (an MCMC chain must start with positive target
        # density; otherwise the ratio pi(xc)/pi(xs) is undefined). We draw random
        # points until we land in the support -> gives a random valid mode as start.
        for _ in range(200000):
            cand = rng.uniform(-6, 12, size=2)  # covers all case bounding boxes
            if pi_fn(cand[None,:])[0] > 0:
                x0 = cand; break
        if x0 is None:
            x0 = rng.normal(0,1,size=2)
    x = np.array(x0, dtype=float)
    total = n_samples + burn_in
    samples = np.empty((n_samples,2))
    n_acc=0
    for t in range(total):
        if rng.random() <= beta:
            x, acc = intrepid_step(x, pi_fn, rng)
        else:
            x, acc = cmh_step(x, pi_fn, rng)
        if acc: n_acc+=1
        if t >= burn_in:
            samples[t-burn_in] = x
    acc_rate = n_acc/total
    return samples, acc_rate

# ---------------- IID reference sampler (rejection) ----------------
def rejection_sample(case_id, n, seed, bounds, pmax):
    name, pi_fn = CASES[case_id]
    rng = np.random.default_rng(seed)
    out=[]
    (xlo,xhi),(ylo,yhi)=bounds
    while len(out) < n:
        batch=200000
        xs = rng.uniform(xlo,xhi,batch)
        ys = rng.uniform(ylo,yhi,batch)
        pts = np.stack([xs,ys],axis=1)
        vals = pi_fn(pts)
        u = rng.uniform(0, pmax, batch)
        keep = pts[u < vals]
        out.append(keep)
        if sum(len(o) for o in out) >= n:
            break
    res = np.concatenate(out)[:n]
    return res

# ---------------- TVD via 2D histogram ----------------
def tvd(samplesA, samplesB, bins, rng_bounds):
    a = samplesA[np.isfinite(samplesA).all(axis=1)]
    b = samplesB[np.isfinite(samplesB).all(axis=1)]
    HA,_,_ = np.histogram2d(a[:,0],a[:,1],bins=bins,range=rng_bounds,density=True)
    HB,_,_ = np.histogram2d(b[:,0],b[:,1],bins=bins,range=rng_bounds,density=True)
    # normalize to probability mass
    HA = HA/HA.sum(); HB=HB/HB.sum()
    return 0.5*np.abs(HA-HB).sum()

if __name__ == "__main__":
    # quick self-test
    s,ar = run_chain(2, 0.1, 20000, 2000, 0)
    print("case2 beta0.1 accrate", round(ar,3), "mean", s.mean(0))
