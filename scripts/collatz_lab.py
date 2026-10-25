#!/usr/bin/env python3
"""Observe one bounded Collatz trajectory; never claim a universal proof."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Observation:
    start: int
    max_steps: int
    status: str
    steps: int
    last: int
    peak: int


def observe(start: int, max_steps: int) -> Observation:
    """Count individual f(n) transitions, keeping exact integer states only."""
    if start < 1:
        raise ValueError("start must be a positive integer")
    if max_steps < 0:
        raise ValueError("max-steps must be a nonnegative integer")

    current = peak = start
    steps = 0
    while current != 1 and steps < max_steps:
        current = current // 2 if current % 2 == 0 else 3 * current + 1
        steps += 1
        peak = max(peak, current)

    return Observation(
        start=start,
        max_steps=max_steps,
        status="reached_1" if current == 1 else "step_limit",
        steps=steps,
        last=current,
        peak=peak,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Observe one finite Collatz trajectory using exact integers."
    )
    parser.add_argument("start", type=int, help="positive starting integer")
    parser.add_argument(
        "--max-steps", type=int, default=1000,
        help="nonnegative transition budget (default: 1000)",
    )
    args = parser.parse_args()
    try:
        observation = observe(args.start, args.max_steps)
    except ValueError as error:
        parser.error(str(error))

    payload = asdict(observation)
    payload["proves_conjecture"] = False
    payload["interpretation"] = (
        "A step limit is unresolved at this budget, not a counterexample. "
        "Reaching 1 for this start is finite evidence, not a proof for all starts."
    )
    try:
        output = json.dumps(payload, indent=2)
    except ValueError:
        parser.error(
            "observation exceeds Python's decimal integer output limit; "
            "try a smaller start or fewer --max-steps"
        )
    print(output)


if __name__ == "__main__":
    main()
