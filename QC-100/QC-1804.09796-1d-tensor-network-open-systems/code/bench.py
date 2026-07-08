"""Quick benchmark of mesolve+mcsolve on tiny problem."""
import time
import numpy as np
import qutip as qt

N = 4
sx, sz, sm = qt.sigmax(), qt.sigmaz(), qt.sigmam()
I2 = qt.qeye(2)

def op_at(op, k, N):
    return qt.tensor([op if i == k else I2 for i in range(N)])

H = sum(-op_at(sx, k, N) * op_at(sx, k+1, N) for k in range(N-1)) + sum(-op_at(sz, k, N) for k in range(N))
c_ops = [np.sqrt(0.1) * op_at(sm, k, N) for k in range(N)]
psi0 = qt.tensor([qt.basis(2, 0)] * N)
tlist = np.linspace(0, 5, 11)
e_ops = [op_at(sz, k, N) for k in range(N)]

print("Starting mesolve...", flush=True)
t0 = time.time()
me = qt.mesolve(H, psi0, tlist, c_ops=c_ops, e_ops=e_ops, options={"progress_bar": False})
print(f"mesolve: {time.time()-t0:.2f}s", flush=True)

print("Starting mcsolve (ntraj=20)...", flush=True)
t0 = time.time()
mc = qt.mcsolve(H, psi0, tlist, c_ops=c_ops, e_ops=e_ops, ntraj=20, seeds=1,
                options={"progress_bar": False, "map": "serial"})
print(f"mcsolve ntraj=20: {time.time()-t0:.2f}s", flush=True)

print("mesolve final <sz_0>:", me.expect[0][-1])
print("mcsolve final <sz_0>:", mc.expect[0][-1])
