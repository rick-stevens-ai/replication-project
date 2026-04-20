# Replication: Integer Sequences from Configurations in the Hausdorff Metric Geometry via Edge Covers of Bipartite Graphs

**Paper:** Bobrowski, Elpers, Helmkamp, Ovsyannikov, Xique (2021)
**OSTI ID:** 1997354
**DOI:** (from OSTI)

## Overview

The paper establishes a connection between:
1. **Configurations** in Hausdorff metric geometry — pairs of sets [A,B] where every point achieves the Hausdorff distance
2. **Edge covers** of bipartite graphs — subsets of edges covering all vertices
3. **Integer sequences** — counting how many "between sets" exist for a configuration

The key result: **#([A,B]) = number of edge covers of G_{[A,B]}**, the bipartite graph where edges connect points at distance h(A,B).

## What to Replicate

### Core Formulas (5 levels)

**Level 0: Complete bipartite graph K_{m,n}** (Theorem 8)
```
E(m,n) = Σ_{j=0}^{m} C(m,j)·(-1)^j·(2^{m-j} - 1)^n
```
This is the number of {0,1} m×n matrices with no all-zero rows or columns.
OEIS: A048291 (n×n case)

**Level 1: K_{m,n} minus 1 edge** (Theorem 10)
```
E₁(m,n) = ½[E(m,n) - E(m-1,n) - E(m,n-1) - E(m-1,n-1)]
```
OEIS: A335608-A335611

**Level 2: K_{m,n} minus 2 edges** (Theorem 11) — 3 cases by edge topology
- E_{2_1}: both edges share a vertex in V₁
- E_{2_2}: both edges share a vertex in V₂  
- E_{2_3}: no shared vertices
OEIS: A335612-A335613, A337416-A337418, A340173-A340175, A340199-A340201, A340897

**Level 3: K_{m,n} minus 3 edges** (Theorem 12) — 6 cases
OEIS: A340898-A340899, A342580, A342796 (and more)

**Level 4: General enumeration** — brute-force edge cover counting for arbitrary bipartite graphs

### Tables to Reproduce
- Table 1: E₁(m,n) closed forms and first terms for m=2..6
- Table 2: E_{2_k}(m,n) closed forms for all 3 cases, m=2..6
- Table 3: E_{3_k}(m,n) closed forms for all 6 cases, m=2..6

### Key Claims to Verify
1. Every integer 1-18 is achievable as #([A,B])
2. 19 is NOT achievable (Blackburn et al.)
3. Every integer 20-36 is achievable
4. 37 is NOT achievable (Honigs)
5. 41, 59, 67 are NOT achievable (Ovsyannikov)
6. All Fibonacci numbers are achievable
7. All even-indexed Lucas numbers are achievable

### OEIS Sequences to Verify (at least 25 new sequences)
A335608, A335609, A335610, A335611,
A335612, A335613, A337416, A337417, A337418,
A340173, A340174, A340175, A340199, A340200, A340201, A340897,
A340898, A340899, A342580, A342796, and more from Table 3

## Approach

### Phase 1: Implement Core Formulas
- Implement E(m,n) from the inclusion-exclusion formula
- Implement E₁(m,n) via Theorem 10
- Implement E_{2_k}(m,n) via Theorem 11 (3 cases)
- Implement E_{3_k}(m,n) via Theorem 12 (6 cases)
- Generate first 10+ terms for each sequence
- Cross-check against OEIS

### Phase 2: Brute-Force Verification
- Enumerate ALL edge covers of small bipartite graphs (K_{m,n} minus k edges)
- Verify formula results match brute-force counts exactly
- Use NetworkX for graph construction, itertools for subset enumeration

### Phase 3: Closed-Form Verification
- Verify that each closed-form expression in Tables 1-3 matches the recursive formulas
- Use SymPy for symbolic verification where possible

### Phase 4: Achievability Analysis
- For each integer 1-100, determine if it's achievable as #([A,B])
- Enumerate edge cover counts for all bipartite graphs up to reasonable size
- Verify the gaps at 19, 37, 41, 59, 67

### Phase 5: Extended Results
- Extend all sequences beyond what the paper reports
- Verify Fibonacci/Lucas achievability claims
- Generate the "achievable integers" sequence

## Tools Required

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.11+ | Primary language | Available |
| NetworkX | Graph construction/analysis | pip install networkx |
| SymPy | Symbolic math, closed-form verification | pip install sympy |
| NumPy | Numerical operations | pip install numpy |
| itertools | Combinatorial enumeration | stdlib |
| math | Binomial coefficients | stdlib |
| requests | OEIS API access | pip install requests |

No GPU needed. No large datasets. Pure computation.
Estimated time: a few hours of development, seconds of runtime for all formulas.

## Verification Strategy

1. **Formula vs brute-force**: Every formula result checked against exhaustive enumeration for small (m,n)
2. **OEIS cross-reference**: Every named sequence verified against OEIS database
3. **Closed-form vs recursive**: Symbolic verification that closed forms satisfy the recurrences
4. **Extension**: Generate terms beyond the paper's tables; verify they satisfy recurrences

## Files

```
src/
  edge_covers.py       — Core E(m,n), E₁, E_{2_k}, E_{3_k} formulas
  brute_force.py       — Exhaustive edge cover enumeration
  oeis_verify.py       — OEIS lookup and cross-checking
  achievability.py     — Which integers are achievable as #([A,B])
  tables.py            — Reproduce all paper tables
  closed_forms.py      — Symbolic closed-form verification
tests/
  test_formulas.py     — Unit tests for all formulas
  test_brute_force.py  — Verify formula vs exhaustive counts
results/
  table1.csv           — Reproduced Table 1
  table2.csv           — Reproduced Table 2
  table3.csv           — Reproduced Table 3
  achievable.csv       — Achievable integers analysis
  oeis_matches.json    — OEIS verification results
docs/
  paper.pdf            — Original paper (symlink)
```
