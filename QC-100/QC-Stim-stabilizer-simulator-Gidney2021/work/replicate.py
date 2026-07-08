#!/usr/bin/env python3
"""
Independent replication of Gidney 2021, "Stim: a fast stabilizer circuit simulator"
(Quantum 5, 497; arXiv:2103.02202).

Testable claims exercised here:
  C1  Headline: a distance-100 surface code circuit (~20k qubits, ~8M gates,
      ~1M measurements) can be *analyzed* (first sample) in ~15 s, then sampled
      at ~1 kHz thereafter.
  C2  Deterministic-measurement complexity is (near) LINEAR in Stim, vs the
      quadratic Theta(n^2) of Aaronson-Gottesman CHP. Test: measure first-sample
      time on unrotated surface-code memory circuits of growing distance and
      fit the growth exponent (Fig 5 setup).
  C3  Bulk sampling amortizes: after the reference sample, per-shot cost is tiny
      (Pauli-frame batches). Test: time first sample vs marginal per-shot cost
      when collecting many shots (Fig 1 setup).
  C4  Correctness: Stim reproduces known stabilizer results (GHZ parity,
      Bell correlations, deterministic stabilizer measurements).
  C5  Surface-code decoding with PyMatching yields logical-error curves showing
      a threshold (~1%) -- the canonical downstream use of Stim + PyMatching.

Free/local compute only. No fabricated numbers.
"""
import json, time, math, sys
import numpy as np
import stim, pymatching

OUT = {}
def log(*a):
    print(*a, flush=True)

# --------------------------------------------------------------------------
# C4: CORRECTNESS -- known stabilizer results
# --------------------------------------------------------------------------
def c4_correctness():
    log("\n=== C4 correctness ===")
    res = {}

    # Bell state: measuring both qubits in Z always agrees (perfect correlation)
    c = stim.Circuit()
    c.append("H", [0]); c.append("CNOT", [0, 1])
    c.append("M", [0, 1])
    s = c.compile_sampler().sample(shots=100000)
    agree = np.mean(s[:, 0] == s[:, 1])
    res["bell_zz_correlation"] = float(agree)  # expect 1.0

    # GHZ over 5 qubits: all measurements equal (parity even)
    n = 5
    c = stim.Circuit()
    c.append("H", [0])
    for q in range(1, n):
        c.append("CNOT", [0, q])
    c.append("M", list(range(n)))
    s = c.compile_sampler().sample(shots=100000)
    alleq = np.mean((s.sum(axis=1) == 0) | (s.sum(axis=1) == n))
    res["ghz5_all_equal_frac"] = float(alleq)  # expect 1.0
    p_allzero = float(np.mean(s.sum(axis=1) == 0))
    res["ghz5_p_allzero"] = p_allzero  # expect ~0.5

    # Deterministic measurement: |0>, apply nothing, M -> always 0
    c = stim.Circuit("M 0")
    s = c.compile_sampler().sample(shots=1000)
    res["m_ground_all_zero"] = bool(np.all(s == 0))

    # X on |0> then M -> always 1 (deterministic 1)
    c = stim.Circuit("X 0\nM 0")
    s = c.compile_sampler().sample(shots=1000)
    res["x_then_m_all_one"] = bool(np.all(s == 1))

    # Repetition-code detector determinism (no noise): all detectors silent
    c = stim.Circuit.generated(
        "repetition_code:memory", rounds=10, distance=5,
        before_round_data_depolarization=0.0)
    dets = c.compile_detector_sampler().sample(shots=1000)
    res["rep_code_noiseless_detectors_all_zero"] = bool(np.all(dets == 0))

    log(json.dumps(res, indent=2))
    OUT["C4_correctness"] = res
    return res

# --------------------------------------------------------------------------
# C1: HEADLINE d=100 surface code
# --------------------------------------------------------------------------
def c1_headline(distance=100, rounds=None):
    log(f"\n=== C1 headline d={distance} surface code ===")
    if rounds is None:
        rounds = distance  # d rounds is standard for a memory experiment
    t0 = time.monotonic()
    circ = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        rounds=rounds, distance=distance,
        after_clifford_depolarization=0.001,
        before_measure_flip_probability=0.001,
        after_reset_flip_probability=0.001,
        before_round_data_depolarization=0.001,
    )
    t_build = time.monotonic() - t0

    n_qubits = circ.num_qubits
    n_meas = circ.num_measurements
    n_dets = circ.num_detectors
    # 'gates': count total individual gate applications cheaply.
    # circ.flattened() unrolls REPEAT loops; each instruction carries a
    # target list, so total gate-applications = sum of (targets / gate_arity).
    # We approximate 'operations' as total number of targets across all
    # single/two-qubit instructions -- fast because it's C-level per instruction.
    t0c = time.monotonic()
    flat = circ.flattened()
    n_ops = len(flat)                                  # instruction count
    n_gate_apps = 0
    for inst in flat:
        n_gate_apps += len(inst.targets_copy())
    t_count = time.monotonic() - t0c

    log(f"  built circuit in {t_build:.2f}s: qubits={n_qubits} measurements={n_meas} "
        f"detectors={n_dets} instructions={n_ops} target_slots(~gates)={n_gate_apps} "
        f"(count took {t_count:.2f}s)")

    # "Analyze + take first sample" == compile the detector sampler and pull 1 shot.
    t0 = time.monotonic()
    samp = circ.compile_detector_sampler()
    first = samp.sample(shots=1)
    t_first = time.monotonic() - t0
    log(f"  compile + FIRST detector sample: {t_first:.2f}s")

    # Sustained bulk sampling rate: take a batch and compute shots/sec
    batch = 1000
    t0 = time.monotonic()
    _ = samp.sample(shots=batch)
    t_bulk = time.monotonic() - t0
    rate = batch / t_bulk
    log(f"  bulk {batch} shots in {t_bulk:.3f}s -> {rate:,.0f} shots/s ({rate/1000:.2f} kHz)")

    OUT["C1_headline"] = {
        "distance": distance, "rounds": rounds,
        "num_qubits": n_qubits, "num_measurements": n_meas,
        "num_detectors": n_dets, "flattened_instructions": n_ops,
        "target_slots_approx_gates": n_gate_apps,
        "build_seconds": t_build,
        "compile_plus_first_sample_seconds": t_first,
        "bulk_batch_shots": batch,
        "bulk_seconds": t_bulk,
        "bulk_shots_per_second": rate,
        "bulk_kHz": rate / 1000.0,
    }
    return OUT["C1_headline"]

# --------------------------------------------------------------------------
# C2: scaling of first-sample time vs distance (linear-ish, Fig 5)
# --------------------------------------------------------------------------
def c2_scaling(distances=(3, 5, 7, 11, 15, 21, 31, 45)):
    log("\n=== C2 first-sample scaling vs distance (Fig 5) ===")
    rows = []
    for d in distances:
        rounds = d
        circ = stim.Circuit.generated(
            "surface_code:unrotated_memory_z",
            rounds=rounds, distance=d,
            before_round_data_depolarization=0.001,
        )
        nq = circ.num_qubits
        # first sample = compile detector sampler + 1 shot (dominant one-time cost)
        t0 = time.monotonic()
        samp = circ.compile_detector_sampler()
        samp.sample(shots=1)
        dt = time.monotonic() - t0
        rows.append({"distance": d, "rounds": rounds, "num_qubits": nq, "first_sample_s": dt})
        log(f"  d={d:>3} qubits={nq:>6} first_sample={dt*1000:8.2f} ms")
    # fit log-log slope of first_sample_s vs num_qubits
    xs = np.log(np.array([r["num_qubits"] for r in rows]))
    ys = np.log(np.array([max(r["first_sample_s"], 1e-6) for r in rows]))
    slope, intercept = np.polyfit(xs, ys, 1)
    log(f"  log-log slope (time vs #qubits): {slope:.3f}  (quadratic-in-qubits ~2.0; CHP det-meas is O(n^2) overall)")
    OUT["C2_scaling"] = {"rows": rows, "loglog_slope_time_vs_qubits": float(slope)}
    return OUT["C2_scaling"]

# --------------------------------------------------------------------------
# C3: bulk-sampling amortization (Fig 1)
# --------------------------------------------------------------------------
def c3_amortization(distance=51, rounds=51):
    log(f"\n=== C3 bulk-sampling amortization d={distance} ===")
    circ = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        rounds=rounds, distance=distance,
        after_clifford_depolarization=0.001,
        before_measure_flip_probability=0.001,
        after_reset_flip_probability=0.001,
        before_round_data_depolarization=0.001,
    )
    samp = circ.compile_detector_sampler()
    # first sample time
    t0 = time.monotonic(); samp.sample(shots=1); t1 = time.monotonic() - t0
    results = {"num_qubits": circ.num_qubits, "first_sample_s": t1}
    per_shot = {}
    for N in (1, 10, 100, 1000, 10000, 100000):
        t0 = time.monotonic()
        samp.sample(shots=N)
        dt = time.monotonic() - t0
        per_shot[str(N)] = {"total_s": dt, "per_shot_us": dt / N * 1e6}
        log(f"  {N:>7} shots: {dt*1000:9.2f} ms total -> {dt/N*1e6:10.3f} us/shot")
    results["per_shot"] = per_shot
    # amortization factor: per-shot cost at N=1 vs N=100000
    amort = per_shot["1"]["per_shot_us"] / per_shot["100000"]["per_shot_us"]
    results["amortization_factor_N1_over_N100k"] = amort
    log(f"  amortization (us/shot at N=1) / (us/shot at N=100k) = {amort:,.0f}x")
    OUT["C3_amortization"] = results
    return results

# --------------------------------------------------------------------------
# C5: surface-code threshold via Stim detectors + PyMatching decoding
# --------------------------------------------------------------------------
def c5_threshold(distances=(3, 5, 7), noises=(0.002, 0.005, 0.008, 0.01, 0.012, 0.015, 0.02), shots=50000):
    log("\n=== C5 surface-code logical error vs physical error (Stim+PyMatching) ===")
    curves = {}
    for d in distances:
        curves[str(d)] = {}
        for p in noises:
            circ = stim.Circuit.generated(
                "surface_code:rotated_memory_z",
                rounds=d, distance=d,
                after_clifford_depolarization=p,
                before_measure_flip_probability=p,
                after_reset_flip_probability=p,
                before_round_data_depolarization=p,
            )
            dem = circ.detector_error_model(decompose_errors=True)
            matcher = pymatching.Matching.from_detector_error_model(dem)
            sampler = circ.compile_detector_sampler()
            det, obs = sampler.sample(shots=shots, separate_observables=True)
            pred = matcher.decode_batch(det)
            errs = int(np.sum(np.any(pred != obs, axis=1)))
            ler = errs / shots
            curves[str(d)][f"{p}"] = {"logical_errors": errs, "shots": shots, "logical_error_rate": ler}
            log(f"  d={d} p={p:<6} LER={ler:.5f} ({errs}/{shots})")
    # estimate threshold: physical p where curves for different d cross
    OUT["C5_threshold"] = {"curves": curves, "shots_per_point": shots,
                           "expected_threshold_pct": "~1% (0.01) for surface code circuit-level depolarizing"}
    return OUT["C5_threshold"]


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "c4"): c4_correctness()
    if which in ("all", "c3"): c3_amortization()
    if which in ("all", "c2"): c2_scaling()
    if which in ("all", "c5"): c5_threshold()
    if which in ("all", "c1"): c1_headline()
    outpath = "results.json" if len(sys.argv) < 3 else sys.argv[2]
    with open(outpath, "w") as f:
        json.dump(OUT, f, indent=2)
    log(f"\nwrote {outpath}")
