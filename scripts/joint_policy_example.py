#!/usr/bin/env python3
"""Exact reproducible policy enumeration for the finite JLC example.

Requires only Python 3. This is an illustrative exhaustive checker, not a
scalable LDINF implementation. Every event corresponds to one protocol step.
"""
from dataclasses import dataclass
from itertools import product
from typing import Tuple


@dataclass(frozen=True)
class Policy:
    source_cutoff: int
    mental_autonomy: int
    practical_autonomy: int


def run(policy: Policy) -> Tuple[bool, bool, int, int, Tuple[str, ...]]:
    # Trusts: source=3, junior mental=2, senior mental=4,
    # junior practical=2, senior practical=4.
    events = []
    junior_committed_without_review = False
    junior_executed = False
    reviews = 0
    delegations = 0

    if policy.source_cutoff > 3:
        events.append("source_rejected")
        return False, True, len(events), 0, tuple(events)

    if policy.mental_autonomy <= 2:
        events.append("junior_autonomous_admission")
        junior_committed_without_review = True
    else:
        events.extend(["review_request", "senior_validation_commit"])
        reviews = 1

    if policy.practical_autonomy <= 2:
        events.append("junior_executed_isolation")
        junior_executed = True
    else:
        events.extend(["delegated_to_senior", "senior_executed_isolation"])
        delegations = 1

    completed = True
    safe = not junior_committed_without_review and not junior_executed
    return completed, safe, len(events), 2 * reviews + delegations, tuple(events)


def study(horizon: int):
    policies = [Policy(s, m, p)
                for s, m, p in product(range(5), range(1, 5), range(1, 5))]
    feasible = [x for x in policies
                if (lambda r: r[0] and r[1] and r[2] <= horizon)(run(x))]
    signatures = {(
        x.source_cutoff <= 3,
        x.mental_autonomy <= 2,
        x.practical_autonomy <= 2)
        for x in policies}
    optimum = min((run(x)[3] for x in feasible), default=None)
    return len(policies), len(feasible), len(signatures), optimum


if __name__ == '__main__':
    for horizon in (3, 4, 5):
        count, feasible, signatures, optimum = study(horizon)
        print(f'h={horizon}: candidates={count}, feasible={feasible}, '
              f'signatures={signatures}, min_overhead={optimum}')
    example = Policy(3, 3, 3)
    print('example', example, '->', run(example))
    assert study(3) == (80, 0, 8, None)
    assert study(4) == (80, 16, 8, 3)
    assert study(5) == (80, 16, 8, 3)
