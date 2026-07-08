import time, json, stim
# Faithful reproduction of the paper's 1 kHz claim: MEASUREMENT sampling of the
# full d=100 rotated surface-code memory circuit (paper's headline setup).
d=100
circ = stim.Circuit.generated("surface_code:rotated_memory_z", rounds=d, distance=d,
    after_clifford_depolarization=0.001, before_measure_flip_probability=0.001,
    after_reset_flip_probability=0.001, before_round_data_depolarization=0.001)
print("qubits",circ.num_qubits,"measurements",circ.num_measurements, flush=True)

# measurement sampler (paper's "sampling full circuit shots")
t0=time.monotonic(); ms=circ.compile_sampler(); first=ms.sample(shots=1); t_first=time.monotonic()-t0
print(f"compile+first MEAS sample: {t_first:.3f}s", flush=True)

for N in (100,1000):
    t0=time.monotonic(); ms.sample(shots=N); dt=time.monotonic()-t0
    print(f"  MEAS {N} shots {dt:.3f}s -> {N/dt:,.0f} shots/s ({N/dt/1000:.3f} kHz)", flush=True)

# also bit-packed sampling (paper collects in bulk / packed frames)
t0=time.monotonic(); ms.sample(shots=1000, bit_packed=True); dt=time.monotonic()-t0
print(f"  MEAS 1000 shots bit_packed {dt:.3f}s -> {1000/dt:,.0f} shots/s ({1000/dt/1000:.3f} kHz)", flush=True)

out={"num_qubits":circ.num_qubits,"num_measurements":circ.num_measurements,
     "compile_plus_first_meas_sample_s":t_first}
res={}
for N in (100,1000):
    t0=time.monotonic(); ms.sample(shots=N); dt=time.monotonic()-t0
    res[str(N)]={"total_s":dt,"shots_per_s":N/dt,"kHz":N/dt/1000}
t0=time.monotonic(); ms.sample(shots=1000, bit_packed=True); dt=time.monotonic()-t0
res["1000_bitpacked"]={"total_s":dt,"shots_per_s":1000/dt,"kHz":1000/dt/1000}
out["meas_sampling_rates"]=res
json.dump(out, open("results_c1_measrate.json","w"), indent=2)
print("done", flush=True)
