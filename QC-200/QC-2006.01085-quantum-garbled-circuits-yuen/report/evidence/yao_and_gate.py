"""
Classical Yao Garbled Circuit for a 2-bit AND gate.

Reproduces the baseline that Yuen (Brakerski-Yuen 2020) generalizes to the
quantum setting. Point-and-permute is skipped for clarity; we use raw label
encryption + a permuted table + try-all-4 decode (correctness via keyed AES-
GCM authentication tag — only the correct key/nonce combo decrypts cleanly).

This is the *classical* half of the QGC construction (the fˆ_corr classical
randomized encoding building block).
"""
import os, json, secrets, itertools
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def gen_label():
    """32-byte AES-256 key = one wire label."""
    return secrets.token_bytes(32)


def enc(key_a, key_b, plaintext):
    """Double-encrypt: E_a(E_b(m)). AES-GCM gives us authenticated decryption."""
    n2 = secrets.token_bytes(12)
    inner = AESGCM(key_b).encrypt(n2, plaintext, None)
    n1 = secrets.token_bytes(12)
    outer = AESGCM(key_a).encrypt(n1, inner, None)
    return (n1, n2, outer)


def dec(key_a, key_b, ct):
    """Decrypt E_a(E_b(m)); raises on wrong keys thanks to GCM tag."""
    n1, n2, outer = ct
    inner = AESGCM(key_a).decrypt(n1, outer, None)
    plain = AESGCM(key_b).decrypt(n2, inner, None)
    return plain


def garble_and_gate():
    """Return (garbled_table, wire_labels).  wire_labels[wire][bit] = 32B key."""
    # 3 wires: A, B (inputs), C (output)
    labels = {w: {0: gen_label(), 1: gen_label()} for w in ("A", "B", "C")}
    truth = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}  # AND
    rows = []
    for a, b in itertools.product([0, 1], [0, 1]):
        c = truth[(a, b)]
        rows.append(enc(labels["A"][a], labels["B"][b], labels["C"][c]))
    # Random-permute the table so it doesn't leak input bits
    order = list(range(4))
    secrets.SystemRandom().shuffle(order)
    return [rows[i] for i in order], labels


def evaluate_garbled(table, la, lb):
    """Try all 4 rows; exactly one decrypts to a valid label."""
    for row in table:
        try:
            return dec(la, lb, row)
        except Exception:
            continue
    raise RuntimeError("no row decrypted -- garbling broken")


def main():
    results = []
    for a, b in itertools.product([0, 1], [0, 1]):
        table, labels = garble_and_gate()
        la = labels["A"][a]
        lb = labels["B"][b]
        out_label = evaluate_garbled(table, la, lb)
        # Decode: which output-wire label did we get?
        if out_label == labels["C"][0]:
            c = 0
        elif out_label == labels["C"][1]:
            c = 1
        else:
            c = -1
        expected = a & b
        results.append({
            "a": a, "b": b, "garbled_out": c, "expected": expected,
            "match": c == expected,
        })
    return results


if __name__ == "__main__":
    res = main()
    ok = all(r["match"] for r in res)
    print(json.dumps({"yao_and_gate": res, "all_correct": ok}, indent=2))
