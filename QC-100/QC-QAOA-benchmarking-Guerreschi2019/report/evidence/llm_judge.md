# LLM-judge scoring (free Argo endpoints, not regex)

## argo:gpt-5.2
COVERAGE: 9/10
AGREEMENT: 8/10
VERDICT: REPLICATED
JUSTIFICATION: The replication directly verifies the paper's core simulator-testable claims: exact instance transcription and ground energies (C1), the analytic p=1 triangle-free energy formula to machine precision (C2), and the main optimization-by-energy performance trends and near-matching values for 2-SAT and MaxCut at low p (C3–C4). The only notable shortfall is the linear-annealing initialization result for MaxCut-16 at p=10 (76.4% vs ~85.6%), which is directionally consistent but quantitatively off, likely reflecting implementation/optimization details rather than a failure of the underlying claim. Hardware-only comparisons were appropriately excluded and should not count against coverage of the simulator claims.

## argo:gpt-5.1
COVERAGE: 8/10
AGREEMENT: 9/10
VERDICT: REPLICATED
JUSTIFICATION: All core, testable simulator-side claims (C1–C4) are directly checked and match the paper at machine precision or within minor numerical/optimization differences, including exact instance energies, the analytic p=1 formula, and the qualitative and quantitative behavior of success probability and r versus p. The linear-annealing initialization (C5) is also reproduced with high but slightly lower success probabilities, consistent with optimizer/schedule sensitivity rather than a conceptual mismatch. Hardware-dependent claims are appropriately excluded. Overall, the independent implementation robustly confirms the paper's main QAOA benchmarking conclusions on the tested instances.

(Note: argo:claude-opus-4.8 / 4.7 returned HTTP 502 at run time; two independent GPT-5-family judges concurred on REPLICATED.)
