"""Kiefer–Chatterjee radial dose distribution and ion-track UNIVERSE survival.

Implements Equations (6)–(10) of Liew et al. 2022 plus a domain-grid track
sampler that mimics the cylinder-of-cubic-domains geometry described in
Section 5.2.

For the dose-rate / RBE study we only need an *effective DSB-yield boost*
relative to photons, because in UNIVERSE both photon and ion survival are
ultimately computed from the (N_iDSB, N_cDSB) damage classification using the
same Eq. 5 lethality parameters K_iDSB and K_cDSB.  For each particle / LET
combination we precompute the per-track expected number of iDSB and cDSB
deposited inside a single nucleus, then build the per-track-summed damage
pattern via Poisson sampling over the number of tracks.

The dominant high-LET effect (clusters that drive K_cDSB-dominated killing)
is captured by sampling DSB locations inside a small set of domains under the
ion track, which produces the LET-dependent enrichment of complex damages.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from universe_core import (
    ALPHA_DSB_DEFAULT,
    N_DOMAINS_DEFAULT,
    CellParams,
)


# ---------------------------------------------------------------------------
# Particle catalogue & kinematic helpers
# ---------------------------------------------------------------------------
PROTON_MASS_MEV = 938.272
HE4_MASS_MEV    = 3727.379
WATER_DENSITY   = 1.0    # g/cm^3


def beta_from_LET_proton(LET_keV_um: float) -> float:
    """Approximate proton velocity beta from LET.  Uses a smooth interpolation
    over the proton-in-water table (Bethe-Bloch evaluated externally).

    Calibrated on PSTAR (NIST) proton in liquid water:
        LET 2 keV/um -> ~80 MeV  -> beta ~ 0.396
        LET 8 keV/um -> ~11 MeV  -> beta ~ 0.150
        LET 25 keV/um -> ~ 2 MeV -> beta ~ 0.065
    Returns beta in (0,1).
    """
    # Empirical power-law fit through those three anchors:
    #   beta ~ a * LET^b
    # log betas: ln(0.396)=-0.926 ; ln(0.150)=-1.897 ; ln(0.065)=-2.733
    # log LETs:  ln(2)=0.693      ; ln(8)=2.079      ; ln(25)=3.219
    # Linear regression: b = (-0.926 - -2.733)/(0.693 - 3.219) = -0.715
    #                    a = exp(-0.926 - (-0.715)*0.693) = exp(-0.431) = 0.650
    return float(0.650 * LET_keV_um ** -0.715)


def beta_from_LET_helium(LET_keV_um: float) -> float:
    """Approximate helium-4 velocity beta from LET.

    Calibrated on ASTAR (NIST) He-4 in liquid water:
        LET 4 keV/um  -> ~150 MeV/u -> beta ~ 0.50
        LET 10 keV/um -> ~ 45 MeV/u -> beta ~ 0.30
        LET 22 keV/um -> ~ 16 MeV/u -> beta ~ 0.183
    """
    # ln(0.50)=-0.693 ; ln(0.30)=-1.204 ; ln(0.183)=-1.699
    # ln(4)=1.386     ; ln(10)=2.303    ; ln(22)=3.091
    # Slope b ≈ (-0.693 - -1.699) / (1.386 - 3.091) = -0.590
    # a = exp(-0.693 - (-0.590)*1.386) = exp(0.125) = 1.133
    return float(1.133 * LET_keV_um ** -0.590)


def kinetic_energy_per_u_from_beta(beta: float, mass_u: float = 1.0) -> float:
    """T/u (MeV per nucleon) from beta.  mass_u in atomic mass units."""
    gamma = 1.0 / np.sqrt(1.0 - beta * beta)
    return float((gamma - 1.0) * 931.494)


def effective_charge(z: int, beta: float) -> float:
    """Barkas effective charge, Eq. (9)."""
    return z * (1.0 - np.exp(-125.0 * beta * z ** (-2.0 / 3.0)))


# ---------------------------------------------------------------------------
# Kiefer–Chatterjee RDD (Eqs. 6–8)
# ---------------------------------------------------------------------------
@dataclass
class RDDParams:
    LET_keV_um: float
    z_ion: int
    beta: float

    @property
    def z_star(self) -> float:
        return effective_charge(self.z_ion, self.beta)

    @property
    def K_p(self) -> float:
        # Eq. 8.  K_p has units of Gy * um^2 when LET in keV/um, r in um.
        return 1.25e-4 * (self.z_star / self.beta) ** 2

    @property
    def r_min_um(self) -> float:
        # r_min = beta * r_c, r_c = 11.6 nm (Section 5.2)
        return self.beta * 11.6e-3   # um

    @property
    def r_max_um(self) -> float:
        # r_max = epsilon * E_kin^delta, E_kin in MeV/u, eps=0.062, delta=1.7
        # We assume A ≈ 2 z for the ion, so MeV/u from beta is purely kinematic.
        E_kin = kinetic_energy_per_u_from_beta(self.beta)
        return 0.062 * E_kin ** 1.7

    def D_core(self) -> float:
        """Eq. 6: core dose [Gy]."""
        rmin = self.r_min_um
        rmax = self.r_max_um
        return float(
            (1.0 / (np.pi * rmin * rmin))
            * (self.LET_keV_um / WATER_DENSITY * 1.602e-1
               - 2.0 * np.pi * self.K_p * np.log(rmax / rmin))
        )
        # Conversion: 1 keV/um in water (1 g/cm^3) deposited over 1 um^2 cross
        # section corresponds to 1 keV / (1 um * 1 um * 1 um * 1 g/cm^3).
        # 1 keV / (10^-12 g) = 1.602e-19 / 10^-15 J/kg = 1.602e-4 Gy.
        # Hence the factor 1.602e-1 above? — recompute below.

    def D_at(self, r_um: float) -> float:
        """Total RDD: core (constant) inside r_min, penumbra ~ K_p / r^2 between
        r_min and r_max, zero outside."""
        if r_um <= self.r_min_um:
            return self.D_core_simple()
        if r_um <= self.r_max_um:
            return float(self.K_p / (r_um * r_um))
        return 0.0

    def D_core_simple(self) -> float:
        """Slightly cleaner core derivation: enforce that the LET integral over
        the cross section equals LET / rho (i.e. dose-weighted by area)."""
        rmin = self.r_min_um
        rmax = self.r_max_um
        LET_Gy_um2 = LET_to_Gy_um2(self.LET_keV_um)   # Gy * um^2 (dose-area equivalent)
        penumbra_int = 2.0 * np.pi * self.K_p * np.log(rmax / rmin)
        core = (LET_Gy_um2 - penumbra_int) / (np.pi * rmin * rmin)
        return float(max(core, 0.0))


def LET_to_Gy_um2(LET_keV_um: float) -> float:
    """Convert LET [keV/um] to dose-equivalent area integral [Gy * um^2].

    Energy per unit length = LET * 1 um -> in J for that 1 um track segment:
        E = LET_keV * 1.602e-16 J/keV    (per 1 um of track)
    Mass in a 1 um-long cylinder of cross-section A_um2 (in water):
        m = WATER_DENSITY [g/cm^3] * A_um2 * (1e-4)^2 cm^2 * 1e-4 cm * 1e-3 kg/g
          = WATER_DENSITY * A_um2 * 1e-15 kg
    Dose = E / m  =>  Dose * A_um2 = E / (WATER_DENSITY * 1e-15)  [Gy * um^2]
                   = LET_keV * 1.602e-16 / (1.0 * 1e-15)
                   = LET_keV * 0.1602   [Gy * um^2]
    So the conversion factor is 0.1602 Gy*um^2 per (keV/um).
    """
    return 0.1602 * LET_keV_um


def make_rdd(LET_keV_um: float, particle: str) -> RDDParams:
    """Convenience: build an RDDParams from LET and particle (proton|helium)."""
    if particle == "proton":
        beta = beta_from_LET_proton(LET_keV_um)
        z = 1
    elif particle == "helium":
        beta = beta_from_LET_helium(LET_keV_um)
        z = 2
    else:
        raise ValueError(f"unknown particle '{particle}'")
    return RDDParams(LET_keV_um=LET_keV_um, z_ion=z, beta=beta)


# ---------------------------------------------------------------------------
# Ion-track DSB sampler — *single-track* damage pattern inside a nucleus
# ---------------------------------------------------------------------------
def sample_track_damages(
    rdd: RDDParams,
    nucleus_radius_um: float,
    params: CellParams,
    rng: np.random.Generator,
    n_grid: int = 80,
) -> tuple[int, int]:
    """Approximate the damage pattern from a single ion traversal.

    Two-step recipe consistent with the Liew et al. 2022 description:

      1.  Compute the expected number of DSB this single track deposits
          inside the nucleus.  Energy conservation gives:
              <DSB>_track = alpha_DSB * dose_per_track
          where dose_per_track = LET_to_Gy_um2(LET) / A_nucleus.
          The actual count is drawn from a Poisson(<DSB>_track).

      2.  Distribute those DSB across domains by sampling each DSB's radial
          distance from the track centre with probability density proportional
          to (2 pi r * D(r)) — i.e. dose-area weighting — clipped at rmin
          inside the core and rmax outside.  Each DSB falls into the domain
          containing its (r, phi) position; map to a 2-D grid of domain cells
          across the nucleus cross-section.

    The dose-weighted radial sampling naturally produces cDSB enrichment for
    high-LET tracks: a 25 keV/um proton has r_max ~ 0.2 um while a domain side
    length is ~0.16 um, so the few DSB it deposits are packed into ~1-3
    domains.  A 2 keV/um proton spreads its DSB out to r_max ~ 100 um (which
    extends well beyond the nucleus), so the DSB are scattered into many
    distinct domains.
    """
    A_nuc_um2 = np.pi * nucleus_radius_um ** 2
    dose_per_track = LET_to_Gy_um2(rdd.LET_keV_um) / A_nuc_um2
    mean_dsb_track = params.alpha_DSB * dose_per_track
    n_dsb = int(rng.poisson(mean_dsb_track))
    if n_dsb <= 0:
        return 0, 0

    rmin = rdd.r_min_um
    rmax = min(rdd.r_max_um, nucleus_radius_um)   # cannot leave nucleus

    # Build a 2-D grid of "domains" tiling the nucleus cross-section.
    side = (A_nuc_um2 / params.n_domains) ** 0.5    # side length in um
    n_side = max(2, int(np.ceil(2 * nucleus_radius_um / side)))
    # Sample radial positions of the DSB by inverse-CDF on the dose-area
    # density 2 pi r D(r).
    # CDF inside core (r <= rmin):    prop. r^2 * D_core
    # CDF in penumbra (rmin < r <= rmax): prop. 2 pi K_p * (ln r - ln rmin)  (plus core mass)
    D_core = rdd.D_core_simple()
    if D_core <= 0:
        # Degenerate -- penumbra-only
        rs = rmin + (rmax - rmin) * rng.random(n_dsb)
    else:
        core_mass = np.pi * rmin ** 2 * D_core
        pen_mass = 2 * np.pi * rdd.K_p * np.log(rmax / rmin) if rmax > rmin else 0.0
        total = core_mass + pen_mass
        u = rng.random(n_dsb)
        rs = np.empty(n_dsb)
        in_core = u < (core_mass / total) if total > 0 else np.ones(n_dsb, dtype=bool)
        # Core: r ~ rmin * sqrt(u_local)
        n_core = int(np.sum(in_core))
        if n_core > 0:
            rs[in_core] = rmin * np.sqrt(rng.random(n_core))
        # Penumbra: dose-area weight is 2 pi K_p / r, CDF ~ ln(r/rmin)
        n_pen = n_dsb - n_core
        if n_pen > 0:
            ul = rng.random(n_pen)
            rs[~in_core] = rmin * (rmax / rmin) ** ul

    # Angular positions
    phis = 2.0 * np.pi * rng.random(n_dsb)
    xs = rs * np.cos(phis)
    ys = rs * np.sin(phis)

    # Map (x, y) to integer grid cells, take a unique-cell view to count
    ix = np.floor((xs + nucleus_radius_um) / side).astype(int)
    iy = np.floor((ys + nucleus_radius_um) / side).astype(int)
    # Combine into a single domain index (clip negative/out-of-bounds)
    valid = (ix >= 0) & (ix < n_side) & (iy >= 0) & (iy < n_side)
    ix = ix[valid]
    iy = iy[valid]
    flat = ix * n_side + iy
    if flat.size == 0:
        return 0, 0
    counts = np.bincount(flat)
    n_iDSB = int(np.sum(counts == 1))
    n_cDSB = int(np.sum(counts >= 2))
    return n_iDSB, n_cDSB


def precompute_track_signature(
    rdd: RDDParams,
    nucleus_radius_um: float,
    params: CellParams,
    rng: np.random.Generator | None = None,
    n_track_samples: int = 800,
) -> dict:
    """Sample many single-track damage patterns and cache mean fractions.

    Returns a dict with keys:
        'mean_dsb_per_track'   : <DSB> per traversing track
        'frac_in_iDSB'         : fraction of those DSB that land in iDSB-only domains
        'frac_in_cDSB'         : fraction that land in cDSB domains
        'dose_per_track'       : LET-driven dose increment per traversal
        'iDSB_dispersion'      : variance/mean ratio of iDSB count over samples
    The fractions are used as deterministic 'per-track' parameters when summing
    over many tracks in an ion irradiation.  This is the same trick the GPU
    implementation uses to avoid resampling the whole RDD for every track.
    """
    rng = rng or np.random.default_rng()
    A_nuc_um2 = np.pi * nucleus_radius_um ** 2
    dose_per_track = LET_to_Gy_um2(rdd.LET_keV_um) / A_nuc_um2
    mean_dsb_track = params.alpha_DSB * dose_per_track

    i_counts = np.empty(n_track_samples, dtype=np.int64)
    c_counts = np.empty(n_track_samples, dtype=np.int64)
    for k in range(n_track_samples):
        ni, nc = sample_track_damages(rdd, nucleus_radius_um, params, rng)
        i_counts[k] = ni
        c_counts[k] = nc
    total_i = float(i_counts.mean())
    total_c = float(c_counts.mean())
    return {
        "mean_dsb_per_track": mean_dsb_track,
        "mean_iDSB_per_track": total_i,
        "mean_cDSB_per_track": total_c,
        "dose_per_track": dose_per_track,
    }


def _sample_one_track_full(
    rdd: RDDParams,
    nucleus_radius_um: float,
    params: CellParams,
    rng: np.random.Generator,
    track_xy: tuple[float, float] | None = None,
) -> np.ndarray:
    """Sample (x, y) positions [um] of DSB induced by one track of given RDD,
    relative to the *nucleus centre*.  Returns array of shape (n_dsb, 2).

    track_xy: (x, y) of the track centre inside the nucleus.  If None, sample
    a uniform point inside the nucleus.
    """
    A_nuc_um2 = np.pi * nucleus_radius_um ** 2
    dose_per_track = LET_to_Gy_um2(rdd.LET_keV_um) / A_nuc_um2
    mean_dsb_track = params.alpha_DSB * dose_per_track
    n_dsb = int(rng.poisson(mean_dsb_track))
    if n_dsb <= 0:
        return np.empty((0, 2), dtype=np.float64)
    if track_xy is None:
        u = rng.random()
        r0 = nucleus_radius_um * np.sqrt(u)
        ph0 = 2.0 * np.pi * rng.random()
        tx, ty = r0 * np.cos(ph0), r0 * np.sin(ph0)
    else:
        tx, ty = track_xy

    rmin = rdd.r_min_um
    rmax = min(rdd.r_max_um, 2.0 * nucleus_radius_um)
    D_core = rdd.D_core_simple()
    if D_core <= 0 or rmax <= rmin:
        rs = rmin + (rmax - rmin) * rng.random(n_dsb)
    else:
        core_mass = np.pi * rmin ** 2 * D_core
        pen_mass = 2 * np.pi * rdd.K_p * np.log(rmax / rmin)
        total = core_mass + pen_mass
        u = rng.random(n_dsb)
        in_core = u < (core_mass / total)
        rs = np.empty(n_dsb)
        n_core = int(np.sum(in_core))
        if n_core > 0:
            rs[in_core] = rmin * np.sqrt(rng.random(n_core))
        n_pen = n_dsb - n_core
        if n_pen > 0:
            ul = rng.random(n_pen)
            rs[~in_core] = rmin * (rmax / rmin) ** ul
    phis = 2.0 * np.pi * rng.random(n_dsb)
    xs = tx + rs * np.cos(phis)
    ys = ty + rs * np.sin(phis)
    return np.column_stack([xs, ys])


def _vec_sample_radii(
    n: int, rmin: float, rmax: float, K_p: float, D_core: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Vectorized inverse-CDF sampling of DSB radial positions about a track."""
    if n <= 0:
        return np.empty(0)
    if D_core <= 0 or rmax <= rmin:
        return rmin + (rmax - rmin) * rng.random(n)
    core_mass = np.pi * rmin ** 2 * D_core
    pen_mass = 2 * np.pi * K_p * np.log(rmax / rmin)
    total = core_mass + pen_mass
    u = rng.random(n)
    in_core = u < (core_mass / total)
    rs = np.empty(n)
    n_core = int(np.sum(in_core))
    if n_core > 0:
        rs[in_core] = rmin * np.sqrt(rng.random(n_core))
    n_pen = n - n_core
    if n_pen > 0:
        ul = rng.random(n_pen)
        rs[~in_core] = rmin * (rmax / rmin) ** ul
    return rs


def survival_ion_no_repair(
    dose_Gy: float,
    LET_keV_um: float,
    particle: str,
    params: CellParams,
    nucleus_radius_um: float = 5.0,
    n_iter: int = 1_000,
    rng: np.random.Generator | None = None,
    sig: dict | None = None,    # kept for API compat
) -> float:
    """No-repair UNIVERSE survival after an ion irradiation at given (D, LET, particle).

    Vectorized: sample all tracks for all iterations at once, then bin DSB
    positions onto a per-iteration domain grid.
    """
    rng = rng or np.random.default_rng()
    rdd = make_rdd(LET_keV_um, particle)
    A_nuc_um2 = np.pi * nucleus_radius_um ** 2
    dose_per_track = LET_to_Gy_um2(LET_keV_um) / A_nuc_um2
    if dose_per_track <= 0:
        return 1.0
    mean_tracks = dose_Gy / dose_per_track
    mean_dsb_per_track = params.alpha_DSB * dose_per_track
    rmin = rdd.r_min_um
    rmax = min(rdd.r_max_um, 2.0 * nucleus_radius_um)
    D_core = rdd.D_core_simple()
    K_p = rdd.K_p

    side = (A_nuc_um2 / params.n_domains) ** 0.5
    n_side = max(2, int(np.ceil(2 * nucleus_radius_um / side)))

    # ---- One shot: draw, per iteration, the total number of tracks and DSB ----
    n_tracks_per_iter = rng.poisson(mean_tracks, size=n_iter)
    # For each iter, the total DSB count is N_tracks * Poisson(<dsb/track>),
    # but Poisson sum of Poisson means is also Poisson(N_tracks * mean):
    n_dsb_per_iter = rng.poisson(n_tracks_per_iter * mean_dsb_per_track)

    surv = np.empty(n_iter, dtype=np.float64)
    # Process each iter
    for k in range(n_iter):
        n_dsb = int(n_dsb_per_iter[k])
        n_tr = int(n_tracks_per_iter[k])
        if n_dsb == 0:
            surv[k] = 1.0
            continue

        # Assign each DSB to a track index (uniform if n_tr > 0)
        if n_tr > 0:
            tr_idx = rng.integers(0, n_tr, size=n_dsb)
        else:
            tr_idx = np.zeros(n_dsb, dtype=int)
            n_tr = 1
        # Track centres: uniform inside the nucleus (radius nucleus_radius_um)
        ur = rng.random(n_tr)
        tr_r = nucleus_radius_um * np.sqrt(ur)
        tr_ph = 2 * np.pi * rng.random(n_tr)
        tr_x = tr_r * np.cos(tr_ph)
        tr_y = tr_r * np.sin(tr_ph)

        # Per-DSB radial offset from its track
        rs = _vec_sample_radii(n_dsb, rmin, rmax, K_p, D_core, rng)
        phis = 2 * np.pi * rng.random(n_dsb)
        xs = tr_x[tr_idx] + rs * np.cos(phis)
        ys = tr_y[tr_idx] + rs * np.sin(phis)

        ix = np.floor((xs + nucleus_radius_um) / side).astype(int)
        iy = np.floor((ys + nucleus_radius_um) / side).astype(int)
        mask = (ix >= 0) & (ix < n_side) & (iy >= 0) & (iy < n_side)
        if not mask.any():
            surv[k] = 1.0
            continue
        flat = ix[mask] * n_side + iy[mask]
        counts = np.bincount(flat)
        n_iDSB = int(np.sum(counts == 1))
        n_cDSB = int(np.sum(counts >= 2))
        surv[k] = (1.0 - params.K_iDSB) ** n_iDSB * (1.0 - params.K_cDSB) ** n_cDSB
    return float(surv.mean())


if __name__ == "__main__":
    from universe_core import PARAMS_DU145
    rng = np.random.default_rng(20260529)
    print("Kiefer–Chatterjee RDD sanity:")
    for LET in [2.0, 8.0, 25.0]:
        rdd = make_rdd(LET, "proton")
        print(
            f"  proton LET={LET:5.2f} keV/um  beta={rdd.beta:.3f}  z*={rdd.z_star:.3f}  "
            f"r_min={rdd.r_min_um*1e3:.2f} nm  r_max={rdd.r_max_um:.2f} um  "
            f"K_p={rdd.K_p:.3e} Gy*um^2  D_core={rdd.D_core_simple():.2e} Gy"
        )
    print()
    print("Ion no-repair survival, DU145 (LET=8 keV/um, proton):")
    for D in [1.0, 2.0, 4.0]:
        s = survival_ion_no_repair(D, 8.0, "proton", PARAMS_DU145, n_iter=600, rng=rng)
        print(f"  D={D} Gy -> S={s:.4f}")
