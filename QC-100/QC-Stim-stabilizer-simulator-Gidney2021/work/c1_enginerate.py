import time, json, stim
# Isolate the Pauli-frame ENGINE rate on the d=100 circuit by sampling to a FILE
# sink (stim can write directly, avoiding python array materialization) OR by
# measuring incremental cost. Here: compare small vs medium batch to see if the
# per-shot ENGINE cost (not python) is ~1ms (=1kHz). Use bit_packed to cut IO.
d=100
circ = stim.Circuit.generated("surface_code:rotated_memory_z", rounds=d, distance=d,
    after_clifford_depolarization=0.001, before_measure_flip_probability=0.001,
    after_reset_flip_probability=0.001, before_round_data_depolarization=0.001)
ms=circ.compile_sampler()
ms.sample(shots=1)  # warm
# marginal cost method: time(N=201) - time(N=1) gives 200 shots' marginal engine cost
def t(N):
    t0=time.monotonic(); ms.sample(shots=N, bit_packed=True); return time.monotonic()-t0
t1=t(1); t201=t(201)
marginal_per_shot = (t201 - t1)/200.0
print(f"t(1)={t1:.3f}s t(201)={t201:.3f}s marginal/shot={marginal_per_shot*1000:.3f} ms -> {1/marginal_per_shot:,.0f} shots/s ({1/marginal_per_shot/1000:.3f} kHz)", flush=True)
out={"t1_s":t1,"t201_s":t201,"marginal_per_shot_s":marginal_per_shot,
     "marginal_shots_per_s":1/marginal_per_shot,"marginal_kHz":1/marginal_per_shot/1000}
json.dump(out, open("results_c1_enginerate.json","w"), indent=2)
print("done", flush=True)
