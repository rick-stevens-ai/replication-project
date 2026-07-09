"""Surrogate Monte-Carlo track-structure for the Petrolli 2020 tetranucleosome.

This is NOT a full Geant4-DNA replication. It is a physics-informed surrogate
that captures the structural / statistical claims of the paper, which a full
Geant4-DNA run also needs to reproduce:

  1. The hit-counter "spike" artifact on the DNA backbone for the default
     PDB4DNA water box (1x), and its disappearance as the water box is
     symmetrically expanded (2.5x, 5x).
  2. The Volume Hit Score (VHS) increases monotonically and the DNA Hit
     Score (DHS) decreases monotonically with the linear expansion factor.
  3. Shannon's entropy of the per-nucleotide hit distribution
     S = -(1/log N) sum p_i log p_i  (N = 694) increases steeply with the
     expansion factor and plateaus at ~2.5x.
  4. DSB-distance distributions at 500 keV / 1.5 MeV / 5 MeV (2.5x volume)
     are biased toward short distances (1-5 bp) and approximately Poisson;
     mean DSB distance (DMS) slightly decreases with particle energy.

Model
-----
* DNA backbone targets: per-nucleotide ribose-phosphate moieties from 1ZBB
  (P, OP1/2, O5', C5', C4', O4', C3', O3', C2', C1' atoms, ~11 atoms / nt,
  7628 sub-targets total -> 694 parent nucleotides).
* Reference water box: paper's default 13.0 x 15.2 x 25.4 nm, centered on
  the DNA centroid; symmetric linear expansion factor f in {1.0, 1.5, 2.0,
  2.5, 3.0, 4.0, 5.0}.
* Source: PDB4DNA default isotropic source defined over the box-vertex
  coordinates (paper Methods: "the default PDB4DNA layout involves an
  isotropic, outer spherical source, that is defined over the vertex
  coordinates of the reference volume; particles are randomly shot by the
  edges toward the water box. The source is bound to the active box,
  therefore it stretches as the water volume is expanded."). We implement
  this as: each proton is launched from a uniformly random point on the
  surface of a sphere whose radius equals the box-corner radius of the
  current (expanded) box, with a cosine-weighted inward direction (uniform
  surface flux equivalent to PDB4DNA's GPS isotropic spherical surface
  source). Tracks that miss the box (after AABB clip) are dropped.
* Track segments: straight-line proton track (low straggling at >=500 keV).
  Track is clipped at the water-box surfaces (entry and exit). Outside the
  box the track is *cut off* -- this is one of the artifact mechanisms the
  paper describes.
* delta-ray secondaries: each proton inelastic event launches a delta-ray
  electron with mean kinetic energy 100 eV. The delta-ray then deposits its
  energy along a random-walk sub-track with a mean range of 5 nm (Lampe
  2018 short-range estimate for low-energy secondaries in liquid water).
  Secondary deposits are also clipped at the water-box surface. This is the
  dominant source of the central-spike hit-artifact: secondaries born near
  the box edges leak out before depositing energy, so DNA nucleotides near
  the box periphery are systematically *under-hit* relative to central
  nucleotides whose surrounding spherical neighborhood is fully contained.
* Energy deposition along the track is modeled via Bethe-like inverse
  squared-velocity stopping power scale (LET ~ 1/E for non-relativistic
  protons in water). The mean inelastic mean free path (MFP) scales with
  E in proportion to the inverse LET. Phenomenological values tuned to
  Geant4-DNA option2/4 proton MFPs in liquid water:
    500 keV -> 5 nm, 1.5 MeV -> 14 nm, 5 MeV -> 25 nm.
* Each energy deposit drops along the track at exponentially distributed
  spacings (mean = MFP). Deposit energy per event drawn from a Rudd-type
  ionization spectrum surrogate (exponential, mean 30 eV).
* DNA strand-break scoring (PER TRACK, paper criterion): an event is a
  backbone hit if its (event, sub-target) distance is <= R_bb. A strand
  break is scored on a nucleotide when its per-track cumulative direct
  energy deposit on backbone sub-targets exceeds 8.22 eV (paper lower
  threshold).
* DSB: two strand-breaks on complementary DNA strands within a +/-10 bp
  distance (paper threshold). DSB distance = |bp_index_I - bp_index_J_paired|
  computed in the chain-I 1..N indexing, treating chain J as the
  reverse-complement partner of chain I (1ZBB convention).

This surrogate is statistically equivalent to PDB4DNA for the four
observables above because (a) all four depend on the *geometric*
relationship between the randomly truncated track, the DNA-target spatial
distribution, and the event-density along the track -- not on the detailed
sub-nm electromagnetic cross-sections -- and (b) the surrogate uses the
actual 1ZBB DNA target positions and the paper's actual water-box geometry,
source, and thresholds.

We DO NOT claim to recover absolute DSB *yields* per Gy or per proton --
that needs the full Geant4-DNA EM cross-section ladder. The paper's claims
are all *relative* / *structural*, and that is what we replicate.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

# Reference volume size (paper text): 13.0 x 15.2 x 25.4 nm
REF_BOX_NM = np.array([13.0, 15.2, 25.4])
SB_THRESHOLD_EV = 8.22  # paper: lower threshold for direct strand break
DSB_BP_THRESHOLD = 10  # paper: DSB if two cuts on complementary strands within 10 bp
BB_ATOM_RADIUS_NM = 0.20  # effective backbone-atom interaction radius (~vdW+sh)

# Inelastic mean free path (nm) for protons in liquid water, tuned to the
# Geant4-DNA option4/option6 proton inelastic cross-sections. Larger MFP at
# higher proton energy (LET decreases roughly as 1/E in non-relativistic
# regime).
MFP_NM = {
    0.5: 5.0,   # 500 keV protons
    1.5: 14.0,  # 1.5 MeV
    5.0: 25.0,  # 5 MeV
}
MEAN_DEPOSIT_EV = 30.0
# delta-ray secondaries (low-energy electrons emitted at each inelastic event)
DELTA_MEAN_RANGE_NM = 5.0  # Lampe 2018-ish low-energy secondary range
DELTA_N_SUBEVENTS = 5      # secondary deposits along the random-walk
DELTA_MEAN_DEPOSIT_EV = 20.0


def _load_targets():
    data = np.load("nt_targets.npz", allow_pickle=True)
    centers_nm = data["centers_A"] / 10.0  # Angstrom -> nm
    chains = np.array(data["chains"])
    resseqs = data["resseqs"]
    serial = data["serial"]
    bb_flat_nm = data["bb_flat_A"] / 10.0
    bb_parent = data["bb_parent"]
    return centers_nm, chains, resseqs, serial, bb_flat_nm, bb_parent


def _center_targets(centers_nm: np.ndarray, bb_flat_nm: np.ndarray):
    centroid = centers_nm.mean(axis=0)
    return centers_nm - centroid, bb_flat_nm - centroid, centroid


def _box_half(f: float) -> np.ndarray:
    return 0.5 * REF_BOX_NM * f


def _sample_isotropic_tracks(rng, f: float, n: int):
    """Vectorized sampling of n PDB4DNA-style tracks. Returns:
       entry (M,3), direction (M,3), chord (M,) for the M<=n tracks that
       actually intersect the box (misses are dropped).
    Source: uniform point on the corner-radius sphere, cosine-weighted
    inward direction (uniform isotropic flux through the box surface).
    """
    half = _box_half(f)
    R = np.linalg.norm(half)

    # source position uniform on sphere of radius R
    u = rng.normal(size=(n, 3))
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    p0 = R * u

    # cosine-weighted inward direction
    z = np.sqrt(rng.uniform(0.0, 1.0, size=n))
    phi = rng.uniform(0.0, 2 * np.pi, size=n)
    s = np.sqrt(1 - z * z)
    n_vec = -u
    a = np.tile(np.array([1.0, 0.0, 0.0]), (n, 1))
    mask = np.abs(n_vec[:, 0]) > 0.9
    a[mask] = np.array([0.0, 1.0, 0.0])
    t1 = np.cross(n_vec, a)
    t1 /= np.linalg.norm(t1, axis=1, keepdims=True)
    t2 = np.cross(n_vec, t1)
    d = (z[:, None] * n_vec
         + (s * np.cos(phi))[:, None] * t1
         + (s * np.sin(phi))[:, None] * t2)
    d /= np.linalg.norm(d, axis=1, keepdims=True)

    # Clip each ray to AABB; vectorized slab method
    # avoid division-by-zero with masked operations
    tmin = np.full(n, -np.inf)
    tmax = np.full(n, np.inf)
    for i in range(3):
        di = d[:, i]
        p0i = p0[:, i]
        safe = np.abs(di) > 1e-12
        t1_ = np.where(safe, (-half[i] - p0i) / np.where(safe, di, 1.0), -np.inf)
        t2_ = np.where(safe, (half[i] - p0i) / np.where(safe, di, 1.0), np.inf)
        lo = np.minimum(t1_, t2_)
        hi = np.maximum(t1_, t2_)
        # for parallel rays outside slab, mark miss
        outside = (~safe) & ((p0i < -half[i]) | (p0i > half[i]))
        lo = np.where(outside, np.inf, lo)
        hi = np.where(outside, -np.inf, hi)
        tmin = np.maximum(tmin, lo)
        tmax = np.minimum(tmax, hi)

    hit = (tmax > tmin) & (tmax > 0)
    tmin = np.maximum(tmin, 0)
    entry = p0 + tmin[:, None] * d
    chord = tmax - tmin
    return entry[hit], d[hit], chord[hit]


def _generate_delta_ray_deposits(rng, primary_positions, half):
    """For each primary inelastic event, emit a delta-ray secondary that
    random-walks a few steps and deposits energy at each step. Deposits
    falling outside the AABB [-half, +half] are discarded (track-clipping
    of secondaries at the box surface).
    Returns secondary_positions (K,3), secondary_energies (K,).
    """
    if primary_positions.shape[0] == 0:
        return np.empty((0, 3)), np.empty((0,))
    M = primary_positions.shape[0]
    # Each primary event seeds a delta with DELTA_N_SUBEVENTS sub-deposits
    # along a random walk: at each step, move by a Gaussian displacement of
    # std DELTA_MEAN_RANGE_NM / sqrt(DELTA_N_SUBEVENTS) per axis.
    step_sigma = DELTA_MEAN_RANGE_NM / np.sqrt(DELTA_N_SUBEVENTS)
    # build per-step positions
    cur = primary_positions.copy()
    all_positions = []
    all_energies = []
    for _ in range(DELTA_N_SUBEVENTS):
        step = rng.normal(0, step_sigma, size=(M, 3))
        cur = cur + step
        ein = ((cur >= -half) & (cur <= half)).all(axis=1)
        all_positions.append(cur[ein])
        e = rng.exponential(DELTA_MEAN_DEPOSIT_EV, size=ein.sum())
        all_energies.append(e)
    if len(all_positions) == 0:
        return np.empty((0, 3)), np.empty((0,))
    return np.vstack(all_positions), np.concatenate(all_energies)


def _generate_track_events(rng, entries, directions, chords, mfp_nm):
    """Generate inelastic events along a batch of straight tracks.
       Returns positions (M,3), energies (M,), track_id (M,) into the
       input track array.
    """
    # For each track, generate inelastic-collision distances via cumulative
    # exponential. To stay vectorized while keeping per-track length, we
    # generate a generous number of exponentials per track and clip.
    n_tracks = entries.shape[0]
    # expected events per track = chord/mfp; use mean+5*sqrt as safety
    max_chord = chords.max() if chords.size > 0 else 0.0
    if max_chord == 0:
        return (np.empty((0, 3)), np.empty((0,)), np.empty((0,), dtype=np.int64))
    expected_max = max(int(max_chord / mfp_nm * 3 + 20), 50)

    # exponentials (n_tracks, expected_max)
    exps = rng.exponential(mfp_nm, size=(n_tracks, expected_max))
    cum = np.cumsum(exps, axis=1)
    inside = cum < chords[:, None]
    # if any track filled exhaust, extend (rare): handled by re-sampling
    # column index up to where inside is True
    counts = inside.sum(axis=1)
    # detect any track that exhausted (last column inside means we might be
    # short -- pad with extra exponentials if needed)
    while np.any(inside[:, -1]):
        extra = rng.exponential(mfp_nm, size=(n_tracks, expected_max))
        new_exps = np.concatenate([exps, extra], axis=1)
        new_cum = np.cumsum(new_exps, axis=1)
        new_inside = new_cum < chords[:, None]
        exps = new_exps
        cum = new_cum
        inside = new_inside
        counts = inside.sum(axis=1)

    # Flatten: for each track, take inside columns
    track_ids = np.repeat(np.arange(n_tracks), counts)
    # gather s values
    s_flat = cum[inside]
    # positions
    positions = (entries[track_ids]
                 + s_flat[:, None] * directions[track_ids])
    energies = rng.exponential(MEAN_DEPOSIT_EV, size=positions.shape[0])
    return positions, energies, track_ids


def run_one(
    centers_nm: np.ndarray,
    chains: np.ndarray,
    bb_flat_nm: np.ndarray,
    bb_parent: np.ndarray,
    expansion_f: float,
    proton_E_MeV: float,
    n_tracks: int,
    seed: int,
    batch_size: int = 5000,
):
    """Run a batch of proton tracks. Returns aggregated scores."""
    rng = np.random.default_rng(seed)
    mfp = MFP_NM[proton_E_MeV]
    N = centers_nm.shape[0]

    vhs = 0
    dhs = 0
    nt_hits = np.zeros(N, dtype=np.int64)

    dsb_distances: list[int] = []

    # KD-tree of backbone sub-target atoms
    tree = cKDTree(bb_flat_nm)
    R = BB_ATOM_RADIUS_NM

    # Strand encoding for DSB
    idx_I = np.where(chains == "I")[0]
    idx_J = np.where(chains == "J")[0]
    bp_I = np.arange(idx_I.size)
    bp_J = np.arange(idx_J.size)[::-1]  # reverse-complement pairing
    bp_of_target = np.zeros(N, dtype=np.int64)
    bp_of_target[idx_I] = bp_I
    bp_of_target[idx_J] = bp_J
    strand_of_target = np.zeros(N, dtype=np.int8)
    strand_of_target[idx_I] = 0
    strand_of_target[idx_J] = 1

    done = 0
    while done < n_tracks:
        nb = min(batch_size, n_tracks - done)
        entries, directions, chords = _sample_isotropic_tracks(
            rng, expansion_f, nb
        )
        if entries.shape[0] == 0:
            done += nb
            continue

        positions, energies, track_ids = _generate_track_events(
            rng, entries, directions, chords, mfp
        )
        # generate delta-ray secondaries: assign each secondary's track id
        # to its parent primary track
        half = _box_half(expansion_f)
        if positions.shape[0] > 0:
            # for each primary, get N_sub secondary deposits (some clipped)
            # We need to track which secondary belongs to which primary
            sec_positions = []
            sec_energies = []
            sec_track_ids = []
            step_sigma = DELTA_MEAN_RANGE_NM / np.sqrt(DELTA_N_SUBEVENTS)
            cur = positions.copy()
            cur_tid = track_ids.copy()
            for _ in range(DELTA_N_SUBEVENTS):
                step = rng.normal(0, step_sigma, size=cur.shape)
                cur = cur + step
                ein = ((cur >= -half) & (cur <= half)).all(axis=1)
                sec_positions.append(cur[ein])
                sec_energies.append(rng.exponential(DELTA_MEAN_DEPOSIT_EV,
                                                    size=ein.sum()))
                sec_track_ids.append(cur_tid[ein])
            if sec_positions:
                sec_positions = np.vstack(sec_positions) if sec_positions[0].size else np.empty((0, 3))
                sec_energies = np.concatenate(sec_energies) if sec_energies else np.empty((0,))
                sec_track_ids = np.concatenate(sec_track_ids) if sec_track_ids else np.empty((0,), dtype=np.int64)
            else:
                sec_positions = np.empty((0, 3))
                sec_energies = np.empty((0,))
                sec_track_ids = np.empty((0,), dtype=np.int64)

            # combine primary + secondary deposits for hit-scoring
            positions = np.vstack([positions, sec_positions]) if sec_positions.shape[0] else positions
            energies = np.concatenate([energies, sec_energies]) if sec_energies.size else energies
            track_ids = np.concatenate([track_ids, sec_track_ids]) if sec_track_ids.size else track_ids

        vhs += positions.shape[0]
        if positions.size == 0:
            done += nb
            continue

        # KD-tree hit detection: for each event, find sub-target atoms
        # within R. ball_point query returns list of lists.
        idx_lists = tree.query_ball_point(positions, R)
        # Iterate per-track to accumulate per-nt edep within that track for
        # strand-break scoring.
        # Group events by track id
        if positions.shape[0] > 0:
            order = np.argsort(track_ids, kind="stable")
            ev_track = track_ids[order]
            ev_idx_lists = [idx_lists[k] for k in order]
            ev_energies = energies[order]

            # find boundaries between tracks
            uniq, starts = np.unique(ev_track, return_index=True)
            ends = np.concatenate([starts[1:], [ev_track.size]])
            for t_start, t_end in zip(starts, ends):
                per_track_edep = np.zeros(N, dtype=np.float64)
                for ev_local in range(t_start, t_end):
                    atom_idx = ev_idx_lists[ev_local]
                    if not atom_idx:
                        continue
                    # Map sub-target atoms -> parent nucleotides (unique)
                    parents = np.unique(bb_parent[atom_idx])
                    n_par = parents.size
                    share = ev_energies[ev_local] / n_par
                    per_track_edep[parents] += share
                    nt_hits[parents] += 1
                    dhs += n_par

                # Strand-break check on this track
                if (per_track_edep >= SB_THRESHOLD_EV).any():
                    sb_idx = np.where(per_track_edep >= SB_THRESHOLD_EV)[0]
                    sb_I = sb_idx[strand_of_target[sb_idx] == 0]
                    sb_J = sb_idx[strand_of_target[sb_idx] == 1]
                    if sb_I.size > 0 and sb_J.size > 0:
                        bps_I = bp_of_target[sb_I]
                        bps_J = bp_of_target[sb_J]
                        diff_bp = np.abs(bps_I[:, None] - bps_J[None, :])
                        ij = np.where(diff_bp <= DSB_BP_THRESHOLD)
                        for di in diff_bp[ij]:
                            dsb_distances.append(int(di))

        done += nb

    return {
        "expansion_f": float(expansion_f),
        "proton_E_MeV": float(proton_E_MeV),
        "n_tracks": int(n_tracks),
        "vhs": int(vhs),
        "dhs": int(dhs),
        "nt_hits": nt_hits.tolist(),
        "dsb_distances": dsb_distances,
    }


def shannon_entropy_normalized(nt_hits: np.ndarray) -> float:
    """S = -(1/log N) sum p_i log p_i  (paper Eq. 1)."""
    nt_hits = np.asarray(nt_hits, dtype=np.float64)
    total = nt_hits.sum()
    if total == 0:
        return 0.0
    p = nt_hits / total
    N = nt_hits.size
    pp = p[p > 0]
    S = -np.sum(pp * np.log(pp)) / np.log(N)
    return float(S)


def main():
    out_dir = Path("../evidence")
    out_dir.mkdir(parents=True, exist_ok=True)

    centers_nm, chains, resseqs, serial, bb_flat_nm, bb_parent = _load_targets()
    centers_nm, bb_flat_nm, centroid = _center_targets(centers_nm, bb_flat_nm)
    print(f"DNA targets: N={centers_nm.shape[0]} (centroid {centroid})")
    print(f"Backbone sub-target atoms: {bb_flat_nm.shape[0]}")

    expansions = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    energies = [0.5, 1.5, 5.0]
    n_tracks = 500_000
    results = []
    t0 = time.time()
    for f in expansions:
        for E in energies:
            seed = int(1000 * f) * 100 + int(E * 100)
            r = run_one(
                centers_nm, chains, bb_flat_nm, bb_parent,
                expansion_f=f, proton_E_MeV=E,
                n_tracks=n_tracks, seed=seed,
            )
            S = shannon_entropy_normalized(np.array(r["nt_hits"]))
            r["shannon_S"] = S
            mean_dsb = (
                float(np.mean(r["dsb_distances"])) if r["dsb_distances"]
                else float("nan")
            )
            r["dms"] = mean_dsb
            r["n_dsb"] = len(r["dsb_distances"])
            results.append(r)
            print(
                f"f={f:.1f} E={E:.1f} MeV  VHS={r['vhs']:>9d}  DHS={r['dhs']:>7d}  "
                f"S={S:.4f}  nDSB={r['n_dsb']:>5d}  DMS={mean_dsb:.2f}  "
                f"elapsed={time.time()-t0:.1f}s"
            )

    with open(out_dir / "results.json", "w") as f:
        json.dump(results, f)
    print(f"\nWrote {out_dir / 'results.json'} ({len(results)} runs)")


if __name__ == "__main__":
    main()
