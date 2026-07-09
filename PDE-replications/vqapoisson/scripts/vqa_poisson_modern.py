"""
Modernized port of ToyotaCRDL/VQAPoisson `vqa_poisson.py` (Apache-2.0)
to Qiskit 2.x / Aer 0.17+. The algorithm and circuit constructions are
unchanged; only the backend/execute scaffolding is replaced.

Original: https://github.com/ToyotaCRDL/VQAPoisson
Paper: Sato, Kondo, Koide, Takamatsu, Imoto, Phys. Rev. A 104, 052409 (2021).
"""

import warnings

import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector


class _StatevectorQI:
    """Minimal stand-in for qiskit.aqua.QuantumInstance that the original
    module reaches into. We only support the `is_statevector` branch and
    expose .execute(qc) -> a result-like wrapper with .get_statevector().
    """

    is_statevector = True

    class _Result:
        def __init__(self, sv: np.ndarray):
            self._sv = sv

        def get_statevector(self, _qc=None):
            return self._sv

    def execute(self, qc: QuantumCircuit):
        # Strip measurements just in case; Statevector.from_instruction needs
        # a unitary circuit. The original code only measures when running on
        # a non-statevector backend, so this is a safety net.
        clean = qc.remove_final_measurements(inplace=False)
        if clean is None:
            clean = qc
        sv = Statevector.from_instruction(clean).data
        return _StatevectorQI._Result(sv)


def _sv_from_circuit(qc: QuantumCircuit) -> np.ndarray:
    clean = qc.remove_final_measurements(inplace=False)
    if clean is None:
        clean = qc
    return Statevector.from_instruction(clean).data


class VQAforPoisson:
    """Variational quantum algorithm for the 1D Poisson equation, faithful
    port of ToyotaCRDL/VQAPoisson with a modern Qiskit backend.
    """

    def __init__(self, num_qubits, num_layers, bc, *, qinstance=None,
                 oracle_f=None, c=1e-3, use_mct_ancilla=False):
        self.num_qubits = num_qubits
        self.num_layers = num_layers
        self.bc = bc
        self.c = c
        self.use_mct_ancilla = use_mct_ancilla

        if self.num_qubits <= 3 and self.use_mct_ancilla:
            warnings.warn("mcx with ancillas valid for num_qubits>3; disabling.")
            self.use_mct_ancilla = False
        self.num_mct_ancilla = self.num_qubits - 3 if use_mct_ancilla else 0

        self.num_params_per_layer = 2*(num_qubits//2) + 2*((num_qubits-1)//2)
        self.num_params = num_qubits + num_layers*self.num_params_per_layer
        self.circuit_counts = 0

        self.qreg = QuantumRegister(num_qubits, 'q')
        self.qreg_ancilla = QuantumRegister(1, 'q_ancilla')

        if oracle_f is not None:
            self.qc_f_vec = oracle_f
        else:
            self.qc_f_vec = QuantumCircuit(self.qreg)

        self.qinstance = qinstance or _StatevectorQI()

    # ---- public API -------------------------------------------------------

    def objective(self, params):
        obj = self.evaluate(params)[0]
        self.current_objective = obj
        return obj

    def evaluate(self, params):
        A0_X = self._calc_Xn(params, is_shift=False)
        A1_X = self._calc_Xn(params, is_shift=True)
        if self.bc == 'Periodic':
            B = 0
            c = self.c
        elif self.bc == 'Dirichlet':
            B_X = self._calc_for_bc(params, is_identity=False)
            B = -B_X
            c = self.c
        elif self.bc == 'Neumann':
            B_I = self._calc_for_bc(params, is_identity=True)
            B_X = self._calc_for_bc(params, is_identity=False)
            B = B_I - B_X
            c = self.c
        else:
            raise ValueError('bc must be Periodic|Dirichlet|Neumann')

        A = 2 - A0_X - A1_X - B + c
        X_In = self._calc_X0(params)
        r = X_In / A
        obj = -0.5*X_In**2 / A
        return obj, r, A, X_In

    def ansatz(self, qc, params, *, control=None):
        params = [params[:self.num_qubits]] + [
            params[self.num_qubits + i*self.num_params_per_layer:
                   self.num_qubits + (i+1)*self.num_params_per_layer]
            for i in range(self.num_layers)
        ]
        if control is None:
            for i in range(self.num_qubits):
                qc.ry(params[0][i], self.qreg[i])
            for i_layer in range(self.num_layers):
                for i in range(self.num_qubits//2):
                    qc.cz(self.qreg[2*i], self.qreg[2*i+1])
                    qc.ry(params[i_layer+1][2*i], self.qreg[2*i])
                    qc.ry(params[i_layer+1][2*i+1], self.qreg[2*i+1])
                for i in range((self.num_qubits-1)//2):
                    qc.cz(self.qreg[2*i+1], self.qreg[2*i+2])
                    qc.ry(params[i_layer+1][2*(self.num_qubits//2)+2*i], self.qreg[2*i+1])
                    qc.ry(params[i_layer+1][2*(self.num_qubits//2)+2*i+1], self.qreg[2*i+2])
        else:
            for i in range(self.num_qubits):
                qc.cry(params[0][i], control, self.qreg[i])
            for i_layer in range(self.num_layers):
                for i in range(self.num_qubits//2):
                    qc.mcp(np.pi, control + [self.qreg[2*i]], self.qreg[2*i+1])
                    qc.cry(params[i_layer+1][2*i], control, self.qreg[2*i])
                    qc.cry(params[i_layer+1][2*i+1], control, self.qreg[2*i+1])
                for i in range((self.num_qubits-1)//2):
                    qc.mcp(np.pi, control + [self.qreg[2*i+1]], self.qreg[(2*i+2) % self.num_qubits])
                    qc.cry(params[i_layer+1][2*(self.num_qubits//2)+2*i], control, self.qreg[2*i+1])
                    qc.cry(params[i_layer+1][2*(self.num_qubits//2)+2*i+1], control, self.qreg[2*i+2])
        return qc

    def state_preparation(self, qc, *, zero_state='f_vec', one_state='ansatz',
                          params=None, dparams=None):
        assert zero_state in ['ansatz', 'grad_ansatz', 'f_vec']
        assert one_state in ['ansatz', 'grad_ansatz', 'f_vec']

        qc.h(self.qreg_ancilla)
        if zero_state == 'ansatz':
            self.ansatz(qc, params, control=list(self.qreg_ancilla))
        elif zero_state == 'grad_ansatz':
            self.ansatz(qc, dparams, control=list(self.qreg_ancilla))
        elif zero_state == 'f_vec':
            qc.compose(self.qc_f_vec.control(1),
                       list(self.qreg_ancilla) + list(self.qreg), inplace=True)

        qc.x(self.qreg_ancilla)
        if one_state == 'ansatz':
            self.ansatz(qc, params, control=list(self.qreg_ancilla))
        elif one_state == 'grad_ansatz':
            self.ansatz(qc, dparams, control=list(self.qreg_ancilla))
        elif one_state == 'f_vec':
            qc.compose(self.qc_f_vec.control(1),
                       list(self.qreg_ancilla) + list(self.qreg), inplace=True)
        return qc

    def shift_add(self, qc):
        if not self.use_mct_ancilla:
            for i in reversed(range(1, self.num_qubits)):
                qc.mcx(self.qreg[:i], self.qreg[i])
            qc.x(self.qreg[0])
        else:
            qreg_anc = QuantumRegister(self.num_qubits-3, 'q_shift_ancilla')
            qc.add_register(qreg_anc)
            for i in reversed(range(1, self.num_qubits)):
                # qiskit 2.x mcx: signature mcx(controls, target, ancilla_qubits=None, mode='basic')
                qc.mcx(self.qreg[:i], self.qreg[i], ancilla_qubits=list(qreg_anc), mode='v-chain')
            qc.x(self.qreg[0])
        return qc

    # ---- gradient ---------------------------------------------------------

    def grad(self, params):
        _, _, A, X_In = self.evaluate(params)
        dobj = []
        for idx in range(len(params)):
            dparams = list(params).copy()
            dparams[idx] += np.pi

            dA0_X = self._calc_grad_A(params, dparams, is_shift=False)
            dA1_X = self._calc_grad_A(params, dparams, is_shift=True)
            if self.bc == 'Periodic':
                dB = 0
            elif self.bc == 'Neumann':
                dB_I = self._calc_grad_for_bc(params, dparams, is_identity=True)
                dB_X = self._calc_grad_for_bc(params, dparams, is_identity=False)
                dB = dB_I - dB_X
            elif self.bc == 'Dirichlet':
                dB_X = self._calc_grad_for_bc(params, dparams, is_identity=False)
                dB = -dB_X
            else:
                raise ValueError('bad bc')
            dA = 0.5*(-dA0_X - dA1_X - dB)
            dX_In = 0.5*self._calc_X0(dparams)
            dobj.append(-X_In*dX_In/A + (X_In**2)*dA/A**2)
        return np.array(dobj)

    # ---- circuit-evaluation helpers --------------------------------------

    def _calc_Xn(self, params, *, is_shift=False):
        qc = QuantumCircuit(self.qreg)
        self.ansatz(qc, params)
        if is_shift:
            self.shift_add(qc)
        qc.h(self.qreg[0])
        sv = _sv_from_circuit(qc)
        val = 0.0
        for l in range(len(sv)):
            bits = bin(l)[2:].zfill(qc.num_qubits)
            if bits[-1] == '0':
                val += np.real(sv[l]*sv[l].conjugate())
            else:
                val -= np.real(sv[l]*sv[l].conjugate())
        self.circuit_counts += 1
        return val

    def _calc_for_bc(self, params, *, is_identity=False):
        qc = QuantumCircuit(self.qreg)
        self.ansatz(qc, params)
        self.shift_add(qc)
        if not is_identity:
            qc.h(self.qreg[0])
        sv = _sv_from_circuit(qc)
        val = 0.0
        for l in range(len(sv)):
            bits = bin(l)[2:].zfill(qc.num_qubits)
            if not np.array([int(bits[i]) for i in range(len(bits)-1)]).any():
                if is_identity:
                    val += np.real(sv[l]*sv[l].conjugate())
                else:
                    if bits[-1] == '0':
                        val += np.real(sv[l]*sv[l].conjugate())
                    else:
                        val -= np.real(sv[l]*sv[l].conjugate())
        self.circuit_counts += 1
        return val

    def _calc_X0(self, params):
        qc = QuantumCircuit(self.qreg, self.qreg_ancilla)
        self.state_preparation(qc, zero_state='f_vec', one_state='ansatz', params=params)
        qc.h(self.qreg_ancilla[0])
        sv = _sv_from_circuit(qc)
        val = 0.0
        for l in range(len(sv)):
            bits = bin(l)[2:].zfill(qc.num_qubits)
            if bits[0] == '0':
                val += np.real(sv[l]*sv[l].conjugate())
            else:
                val -= np.real(sv[l]*sv[l].conjugate())
        self.circuit_counts += 1
        return val

    def _calc_grad_A(self, params, dparams, *, is_shift=False):
        qc = QuantumCircuit(self.qreg, self.qreg_ancilla)
        self.state_preparation(qc, zero_state='grad_ansatz', one_state='ansatz',
                               params=params, dparams=dparams)
        if is_shift:
            self.shift_add(qc)
        qc.h(self.qreg_ancilla)
        qc.h(self.qreg[0])
        sv = _sv_from_circuit(qc)
        val = 0.0
        for l in range(len(sv)):
            bits = bin(l)[2:].zfill(qc.num_qubits)
            if bits[self.num_mct_ancilla] == '0' and bits[-1] == '0':
                val += np.real(sv[l]*sv[l].conjugate())
            elif bits[self.num_mct_ancilla] == '1' and bits[-1] == '0':
                val -= np.real(sv[l]*sv[l].conjugate())
            elif bits[self.num_mct_ancilla] == '0' and bits[-1] == '1':
                val -= np.real(sv[l]*sv[l].conjugate())
            else:
                val += np.real(sv[l]*sv[l].conjugate())
        self.circuit_counts += 1
        return val

    def _calc_grad_for_bc(self, params, dparams, *, is_identity=False):
        qc = QuantumCircuit(self.qreg, self.qreg_ancilla)
        self.state_preparation(qc, zero_state='grad_ansatz', one_state='ansatz',
                               params=params, dparams=dparams)
        self.shift_add(qc)
        qc.h(self.qreg_ancilla)
        if not is_identity:
            qc.h(self.qreg[0])
        sv = _sv_from_circuit(qc)
        val = 0.0
        for l in range(len(sv)):
            bits = bin(l)[2:].zfill(qc.num_qubits)
            if is_identity:
                if bits[self.num_mct_ancilla] == '0' and not np.array(
                        [int(bits[i]) for i in range(self.num_mct_ancilla+1, len(bits)-1)]).any():
                    val += np.real(sv[l]*sv[l].conjugate())
                elif bits[self.num_mct_ancilla] == '1' and not np.array(
                        [int(bits[i]) for i in range(self.num_mct_ancilla+1, len(bits)-1)]).any():
                    val -= np.real(sv[l]*sv[l].conjugate())
            else:
                if not np.array([int(bits[i]) for i in range(self.num_mct_ancilla+1, len(bits)-1)]).any():
                    if bits[self.num_mct_ancilla] == '0' and bits[-1] == '0':
                        val += np.real(sv[l]*sv[l].conjugate())
                    elif bits[self.num_mct_ancilla] == '0' and bits[-1] == '1':
                        val -= np.real(sv[l]*sv[l].conjugate())
                    elif bits[self.num_mct_ancilla] == '1' and bits[-1] == '0':
                        val -= np.real(sv[l]*sv[l].conjugate())
                    else:
                        val += np.real(sv[l]*sv[l].conjugate())
        self.circuit_counts += 1
        return val

    # ---- classical reference ---------------------------------------------

    def get_A_matrix(self):
        I0 = np.array([[1, 0], [0, 0]])
        I = np.array([[1, 0], [0, 1]])
        X = np.array([[0, 1], [1, 0]])
        n = 2**self.num_qubits
        P = np.zeros((n, n))
        for i in range(n):
            P[(i+1) % n, i] = 1
        A0 = I - X
        for _ in range(self.num_qubits-1):
            A0 = np.kron(I, A0)
        A1 = P.T @ A0 @ P
        if self.bc == 'Periodic':
            B = 0; c = self.c
        elif self.bc == 'Neumann':
            B0 = I - X
            for _ in range(self.num_qubits-1):
                B0 = np.kron(I0, B0)
            B = P.T @ B0 @ P; c = self.c
        elif self.bc == 'Dirichlet':
            B0 = -X
            for _ in range(self.num_qubits-1):
                B0 = np.kron(I0, B0)
            B = P.T @ B0 @ P; c = 0
        else:
            raise ValueError('bad bc')
        return A0 + A1 - B + c*np.eye(n)

    def get_f_vec(self):
        return _sv_from_circuit(self.qc_f_vec)

    def get_cl_sol(self):
        return np.linalg.inv(self.get_A_matrix()) @ self.get_f_vec()

    # ---- optimization driver ---------------------------------------------

    def minimize(self, x0, *, method=None, bounds=None, constraints=(), tol=None,
                 options=None, use_grad=True, save_logs=False):
        self.objective_counts = 0
        self.circuit_counts = 0
        self.objective_logs = []
        self.error_logs = {}
        self.objective_count_logs = []
        self.circuit_count_logs = []
        self.sol_logs = []

        jac = self.grad if use_grad else None
        callback = self._callback if save_logs else None

        # wrap objective to count iterations
        def obj_wrapper(x):
            self.objective_counts += 1
            return self.objective(x)

        res = minimize(obj_wrapper, x0, method=method, jac=jac, bounds=bounds,
                       constraints=constraints, tol=tol, callback=callback, options=options)
        self.res = res
        return res

    def _callback(self, xk):
        self.objective_logs.append(self.current_objective)
        self.objective_count_logs.append(self.objective_counts)
        self.circuit_count_logs.append(self.circuit_counts)
        self.sol_logs.append(np.array(xk))
        err = self.get_errors(xk)
        for k, v in err.items():
            self.error_logs.setdefault(k, []).append(v)
        print(f'It.: {len(self.objective_logs):05d}  Obj.: {self.current_objective:.6e}  '
              f'rel: {err["relative"]:.3e}  trace: {err["trace"]:.3e}')

    def get_statevec(self, x):
        qc = QuantumCircuit(self.qreg)
        self.ansatz(qc, x)
        return _sv_from_circuit(qc)

    def get_errors(self, x):
        statevec = self.get_statevec(x)
        r = self.evaluate(x)[1]
        solvec = r * statevec
        cl_sol = self.get_cl_sol()
        cl_sol_normalized = cl_sol / np.linalg.norm(cl_sol)
        cl_dot_state = np.vdot(cl_sol_normalized, statevec)
        return {
            'trace': float(np.sqrt(max(0.0, 1 - np.real(cl_dot_state.conjugate()*cl_dot_state)))),
            'relative': float(np.linalg.norm(cl_sol - solvec) / np.linalg.norm(cl_sol)),
        }

    def get_sol(self, x):
        return self.evaluate(x)[1] * self.get_statevec(x)
