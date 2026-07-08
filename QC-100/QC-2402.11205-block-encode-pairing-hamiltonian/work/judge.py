"""LLM-judge scoring of the replication result via Argo (localhost:44497, key=stevens).

Prompts Claude Opus 4.7 with the paper's headline claims and our numerical
results, asks for a categorical verdict (REPLICATED / PARTIAL / SPOT-CHECK /
CONTRADICTED / NO-GO / BLOCKED / FAILED) and 2-3 sentences of justification.
"""
import os, json, sys, urllib.request, urllib.error

def call_argo(system_prompt, user_prompt, model="argo:claude-opus-4.8"):
    url = "http://127.0.0.1:44497/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.0,
        "max_tokens": 800,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer stevens"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = json.loads(resp.read().decode())
    return body["choices"][0]["message"]["content"]


SYSTEM = """You are an impartial technical reviewer scoring an independent replication of a
quantum-computing paper. Judge whether the reported evidence actually reproduces the
paper's central testable claim.

Reply in exactly the following format:

VERDICT: <one of: REPLICATED, PARTIAL, SPOT-CHECK, CONTRADICTED, NO-GO, BLOCKED, FAILED>
JUSTIFICATION: <2-4 sentences>
"""

USER_TEMPLATE = """PAPER: "An Efficient Quantum Circuit for Block Encoding a Pairing Hamiltonian",
arXiv:2402.11205 (Liu, Du, Lin, Vary, Yang, Feb 2024).

PAPER'S CENTRAL CLAIM (Sec 5.2.2, near end of page 18):
The constructed block-encoding circuit U_H is a (16, 5)-block encoding of the pairing
Hamiltonian H_pair for a 3-nucleon system in a 6-single-particle basis, i.e.
    H_pair = 16 * ( <0^5| tensor I ) U_H ( |0^5> tensor I )    exactly (epsilon = 0),
with the H_MJ=+1/2 sub-block matching the explicit 9x9 matrix in Eq. (41).

Additional claims (Sec 4.4):
- Gate complexity O(L log L) two-qubit + T gates, with L the number of pair terms.
- Ancilla count O(log L) selection + O(1) upper ancillas.

INDEPENDENT REPLICATION EVIDENCE (from our run, all pure NumPy/SciPy sparse simulation):

1. Rebuilt H_pair as a 64x64 matrix in the 6-qubit occupation basis via direct
   action of the pair operators (no Jordan-Wigner needed since the pair operators
   are pseudo-one-body per paper Sec 4.1.3). Result: 61 nonzero entries,
   Hermitian, spectrum in [0, 4].
   * The 9x9 MJ=+1/2 sub-block, reordered to the paper's stated basis ordering
     (0,1,3),(0,1,5),(0,3,5),(1,2,3),(1,2,5),(1,3,4),(1,4,5),(2,3,5),(3,4,5),
     MATCHES paper Eq. (41) EXACTLY (Frobenius diff = 0).

2. Constructed U_H as an explicit 8192x8192 sparse matrix on a 13-qubit register:
   1 validation qubit + 2 auxiliary + 4 selection (2 for l1, 2 for l2) + 6 system.
   * Followed paper's algorithm: U_H = D_full . O_C . D_full . X_v with
     O_C = product over l of U_l, each U_l a controlled swap tied to the
     validation qubit.
   * The construction is (globally) an isometry on the encoding-input subspace:
     ||M^T M - I_64||_F = 6.86e-15, where M is the 8192x64 slice of U_H with
     ancilla index = 0.

3. Extracted the top-left 64x64 block ( <0^7| tensor I ) U_H ( |0^7> tensor I )
   and tested various sub-normalization factors alpha:
     alpha =   4: ||alpha*block - H||_F = 6.82e+00
     alpha =   8: ||alpha*block - H||_F = 4.24e+00
     alpha =   9: ||alpha*block - H||_F = 3.76e+00
     alpha =  16: ||alpha*block - H||_F = 6.46e-15   <--- MACHINE PRECISION
     alpha =  32: ||alpha*block - H||_F = 1.70e+01
   * Least-squares optimal alpha (regression of block against H): 16.0000000000
   * Every nonzero H_ij / block_ij ratio: 16.000000 (min=max=mean=median).

4. On the MJ=+1/2 sub-block, 16 * block reproduces paper Eq. (41) to
   ||.||_F = 2.31e-15.

5. Ancilla accounting: our construction uses 7 ancillas total (1 val + 2 aux + 4 sel).
   The paper's "m=5" figure corresponds to 1 val + 4 sel (the 2 uncomputed
   auxiliaries drop out of the encoding projection since they return to |0>).
   Both counts are O(log L) + O(1), matching the paper's asymptotic claim.

6. Gate counts per paper's Sec 4.4 formulas at L=9:
     12 L log L + 23 L = 549 two-qubit gates
     14 L log L + 21 L = 588 T gates
   (We did NOT construct the full Qiskit circuit; we verified the block-encoding
   linear-algebra identity directly. The formula is analytic in L.)

Please judge.
"""

def main():
    models = ["argo:claude-opus-4.8", "argo:gpt-5.2", "argo:gemini-2.5-pro"]
    responses = {}
    for model in models:
        print(f"\n--- Calling {model} ---")
        try:
            r = call_argo(SYSTEM, USER_TEMPLATE, model=model)
            print(r)
            responses[model] = r
        except Exception as e:
            print(f"ERROR calling {model}: {e}", file=sys.stderr)
            responses[model] = f"ERROR: {e}"
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "report", "evidence")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "llm_judge_argo_panel.txt"), "w") as f:
        f.write("Argo endpoint: http://127.0.0.1:44497/v1/chat/completions\n")
        f.write("3-judge panel via Argo (all free).\n\n")
        for m, r in responses.items():
            f.write("="*70 + "\n")
            f.write(f"Model: {m}\n")
            f.write("="*70 + "\n")
            f.write(r + "\n\n")
    return responses

if __name__ == "__main__":
    main()
