"""
OEIS cross-verification for sequences from the paper.

Fetches sequences from OEIS and compares with our computed values.
"""
import json
import time
from typing import List, Optional, Dict

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from edge_covers import (E, E1, E2_1, E2_2, E2_3, 
                          E3_1, E3_2, E3_3, E3_4, E3_5, E3_6,
                          sequence)


# OEIS sequence IDs from the paper
PAPER_SEQUENCES = {
    # Table 1: E₁(m,n)
    "A335608": ("E1", 3, 3),   # E₁(3,n) for n≥3
    "A335609": ("E1", 4, 4),   # E₁(4,n) for n≥4
    "A335610": ("E1", 5, 5),   # E₁(5,n) for n≥5
    "A335611": ("E1", 6, 6),   # E₁(6,n) for n≥6
    
    # Table 2: E_{2_k}(m,n)
    "A335612": ("E2_1", 3, 3),
    "A335613": ("E2_1", 4, 4),
    "A337416": ("E2_1", 5, 5),
    "A337417": ("E2_1", 6, 6),
    "A337418": ("E2_2", 3, 3),
    "A340173": ("E2_2", 4, 4),
    "A340174": ("E2_2", 5, 5),
    "A340175": ("E2_2", 6, 6),
    "A340199": ("E2_3", 3, 3),
    "A340200": ("E2_3", 4, 4),
    "A340201": ("E2_3", 5, 5),
    "A340897": ("E2_3", 6, 6),
    
    # Table 3: E_{3_k}(m,n)
    "A340898": ("E3_1", 3, 3),
    "A340899": ("E3_1", 4, 4),
    "A342580": ("E3_1", 5, 5),
    "A342796": ("E3_1", 6, 6),
    
    # A048291: E(n,n) — square case
    "A048291": ("E_square", 1, 1),
}

# Map function names to functions
FUNC_MAP = {
    "E1": E1,
    "E2_1": E2_1,
    "E2_2": E2_2,
    "E2_3": E2_3,
    "E3_1": E3_1,
    "E3_2": E3_2,
    "E3_3": E3_3,
    "E3_4": E3_4,
    "E3_5": E3_5,
    "E3_6": E3_6,
}


def compute_sequence(name: str, m: int, n_start: int, n_terms: int = 10) -> List[int]:
    """Compute a sequence from the paper."""
    if name == "E_square":
        return [E(n, n) for n in range(n_start, n_start + n_terms)]
    func = FUNC_MAP[name]
    return [func(m, n) for n in range(n_start, n_start + n_terms)]


def fetch_oeis(seq_id: str) -> Optional[List[int]]:
    """Fetch a sequence from OEIS. Returns list of terms or None."""
    if not HAS_REQUESTS:
        print(f"  [SKIP] requests not installed, can't fetch {seq_id}")
        return None
    
    url = f"https://oeis.org/search?q=id:{seq_id}&fmt=json"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            print(f"  [WARN] HTTP {resp.status_code} for {seq_id}")
            return None
        data = resp.json()
        # OEIS returns a list of result objects directly
        if isinstance(data, list):
            if len(data) == 0:
                print(f"  [WARN] No results for {seq_id}")
                return None
            result = data[0]
        elif isinstance(data, dict):
            if data.get("count", 0) == 0:
                print(f"  [WARN] No results for {seq_id}")
                return None
            result = data["results"][0]
        else:
            print(f"  [WARN] Unexpected response type for {seq_id}")
            return None
        terms_str = result.get("data", "")
        if terms_str:
            return [int(x) for x in terms_str.split(",")]
        return None
    except Exception as e:
        print(f"  [ERROR] {seq_id}: {e}")
        return None


def verify_all(fetch_from_oeis: bool = True, n_terms: int = 10) -> Dict:
    """
    Verify all sequences from the paper.
    
    Returns dict with results per sequence.
    """
    results = {}
    
    for seq_id, (func_name, m, n_start) in PAPER_SEQUENCES.items():
        print(f"\n{seq_id}: {func_name}({m}, n) for n≥{n_start}")
        
        computed = compute_sequence(func_name, m, n_start, n_terms)
        print(f"  Computed: {computed[:8]}...")
        
        if fetch_from_oeis:
            oeis_terms = fetch_oeis(seq_id)
            time.sleep(1)  # Be polite to OEIS
            
            if oeis_terms:
                # Find overlap and compare
                n_compare = min(len(computed), len(oeis_terms))
                match = computed[:n_compare] == oeis_terms[:n_compare]
                if not match:
                    # OEIS might have different offset; try matching subsequence
                    found = False
                    for offset in range(len(oeis_terms)):
                        n_cmp = min(len(computed), len(oeis_terms) - offset)
                        if n_cmp > 0 and computed[:n_cmp] == oeis_terms[offset:offset+n_cmp]:
                            print(f"  OEIS:     {oeis_terms[offset:offset+min(8,n_cmp)]}... (offset {offset})")
                            print(f"  ✅ MATCH (with offset {offset})")
                            found = True
                            break
                    if not found:
                        print(f"  OEIS:     {oeis_terms[:8]}...")
                        print(f"  ❌ MISMATCH")
                else:
                    print(f"  OEIS:     {oeis_terms[:8]}...")
                    print(f"  ✅ MATCH")
                
                results[seq_id] = {
                    "func": func_name, "m": m, "n_start": n_start,
                    "computed": computed, "oeis": oeis_terms,
                    "match": match
                }
            else:
                results[seq_id] = {
                    "func": func_name, "m": m, "n_start": n_start,
                    "computed": computed, "oeis": None,
                    "match": None
                }
        else:
            results[seq_id] = {
                "func": func_name, "m": m, "n_start": n_start,
                "computed": computed, "oeis": None,
                "match": None
            }
    
    return results


if __name__ == "__main__":
    print("=== OEIS Verification ===")
    print("Computing all sequences from the paper...\n")
    
    # First just compute everything (no OEIS fetch)
    results = verify_all(fetch_from_oeis=False, n_terms=10)
    
    print("\n\n=== Summary ===")
    for seq_id, info in sorted(results.items()):
        terms = info["computed"][:6]
        print(f"  {seq_id}: {info['func']}({info['m']},n) = {terms}...")
