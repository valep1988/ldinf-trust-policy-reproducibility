# L-DINF finite trust-policy synthesis: reproducibility

Reproducibility code and data for **Guard-Closed Synthesis and Bisimulation Reduction of Trust Policies for Mental and Practical Actions in L-DINF**, by Stefania Costantini and Valentina Pitoni (manuscript for *Journal of Logic and Computation*).

## Scope

These scripts check a finite example, a nonidentity abstraction, and synthetic guard-template benchmark families. **They do not implement unrestricted L-DINF, mechanize theorems, or show industrial scalability.**

## Requirements

Python 3.9 or newer, standard library only. No data download, package installation, or account credentials.

## Execution

From the root of this repository:

```sh
python3 scripts/joint_policy_example.py
python3 scripts/JLC_nonidentity_abstraction_check.py
python3 scripts/JLC_benchmark_extended.py --output regenerated_benchmark.csv
```

Expected outputs: (i) 80 candidate vectors, 8 signatures, 16 feasible policies at horizons 4 and 5 and none at horizon 3, minimum oversight cost 3; (ii) 45 configurations checked, with 11 concrete and 6 abstract reachable states at thresholds (3,3,3); (iii) 27 benchmark rows from favourable, mixed, and distinct families. The distinct family exhibits no reduction.

The benchmark output is compared automatically against `data/JLC_benchmark_extended.csv` by the supplied GitHub Actions workflow. The stable comparison fields are `family`, `n`, `method`, `graph_builds`, `feasible_representatives`, `states_constructed`, and `edges_constructed`; wall-clock times are machine-dependent and excluded from strict equality checks.

## Limitations

The synthetic generator does not include complex dynamic concurrency, stochastic reputation updates, or adversarial scheduling. The numerical results characterize finite-template reduction mechanisms only. Any new concrete L-DINF/RCRA instance must independently discharge observation, guard-closure, and bidirectional coverage conditions.

## Integrity and provenance

`SHA256SUMS.txt` lists SHA-256 digests for source scripts, data, documentation, and the GitHub workflow. A GitHub URL is not an archival DOI. A release can be archived in Zenodo *after* coauthor approval; no DOI is asserted here.

No software or data license has been selected on behalf of the authors. Obtain coauthor approval and choose an appropriate license before public release. The manuscript itself is **not** included in this code-only repository package.
