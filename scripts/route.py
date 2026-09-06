#!/usr/bin/env python3
"""Deterministic FK Router v0.4.0 recommendation.

The caller supplies the already-assessed complexity and risk. This script
selects the worker, initial reasoning, leadership need, review tier and hard
process budget. It does not launch models or claim that a requested model ran.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


ROUTES = {
    "efficient": (
        (0, 4, "gpt-5.6-luna"),
        (5, 7, "gpt-5.6-terra"),
        (8, 9, "gpt-5.6-sol"),
        (10, 10, "gpt-6-astra"),
    ),
    "balanced": (
        (0, 3, "gpt-5.6-luna"),
        (4, 6, "gpt-5.6-terra"),
        (7, 9, "gpt-5.6-sol"),
        (10, 10, "gpt-6-astra"),
    ),
    "quality": (
        (0, 2, "gpt-5.6-luna"),
        (3, 5, "gpt-5.6-terra"),
        (6, 8, "gpt-5.6-sol"),
        (9, 10, "gpt-6-astra"),
    ),
}

PROCESS_BUDGET = {
    "work_units": 1,
    "implementation_workers": 1,
    "independent_reviewers": 1,
    "implementation_attempts": 2,
    "full_review_passes": 1,
    "focused_review_rechecks": 1,
    "baseline_validation_rounds": 1,
    "focused_validation_reruns": 1,
}


@dataclass(frozen=True)
class Recommendation:
    router_version: str
    complexity: int
    risk: int
    mode: str
    task_kind: str
    worker_model: str | None
    worker_reasoning: str | None
    worker_approval_required: bool
    astra_leadership_required: bool
    review_required: bool
    review_model: str | None
    review_reasoning: str | None
    execution_hint: str
    process_budget: dict[str, int]


def _score(value: int, name: str) -> int:
    if not 0 <= value <= 10:
        raise ValueError(f"{name} must be between 0 and 10")
    return value


def select_worker(complexity: int, mode: str, astra: str) -> tuple[str, bool]:
    for start, end, model in ROUTES[mode]:
        if start <= complexity <= end:
            if model == "gpt-6-astra" and astra == "disabled":
                return "gpt-5.6-sol", False
            return model, model == "gpt-6-astra" and astra == "ask"
    raise AssertionError("routing table does not cover complexity")


def reasoning_for(model: str, complexity: int) -> str:
    if model == "gpt-5.6-luna":
        return "high"
    if model == "gpt-5.6-terra":
        return "high" if complexity >= 6 else "medium"
    if model == "gpt-5.6-sol":
        return "high" if complexity >= 8 else "medium"
    return "high"


def leadership_required(task_kind: str, complexity: int, risk: int, leadership: str) -> bool:
    if leadership == "astra":
        return True
    if task_kind in {"audit", "architecture"}:
        return True
    if task_kind == "diagnosis":
        return complexity >= 8
    return task_kind == "planning" and (complexity >= 8 or risk >= 8)


def review_route(task_kind: str, risk: int, deterministic_validation: bool, review: str) -> tuple[bool, str | None]:
    if task_kind == "audit":
        return False, None
    if risk <= 3 and deterministic_validation:
        return False, None
    model = "gpt-5.6-sol" if risk <= 6 else "gpt-6-astra"
    if review == "astra":
        model = "gpt-6-astra"
    return True, model


def recommend(
    complexity: int,
    risk: int,
    *,
    mode: str = "balanced",
    task_kind: str = "implementation",
    deterministic_validation: bool = True,
    leadership: str = "adaptive",
    review: str = "proportional",
    astra: str = "auto",
) -> Recommendation:
    complexity = _score(complexity, "complexity")
    risk = _score(risk, "risk")

    if task_kind == "plan_only":
        return Recommendation(
            "0.4.0", complexity, risk, mode, task_kind,
            None, None, False,
            leadership == "astra",
            False, None, None,
            "plan_only", dict(PROCESS_BUDGET),
        )

    needs_astra_leadership = leadership_required(
        task_kind, complexity, risk, leadership
    )
    worker, approval = select_worker(complexity, mode, astra)
    if (
        leadership == "adaptive"
        and needs_astra_leadership
        and task_kind in {"audit", "architecture", "diagnosis", "planning"}
    ):
        worker, approval = "gpt-6-astra", False
    needs_review, reviewer = review_route(
        task_kind, risk, deterministic_validation, review
    )
    return Recommendation(
        "0.4.0",
        complexity,
        risk,
        mode,
        task_kind,
        worker,
        reasoning_for(worker, complexity),
        approval,
        needs_astra_leadership,
        needs_review,
        reviewer,
        "high" if reviewer else None,
        "plan_only" if task_kind in {"audit", "architecture", "planning"} else "direct_or_delegated",
        dict(PROCESS_BUDGET),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("complexity", type=int)
    parser.add_argument("risk", type=int)
    parser.add_argument("--mode", choices=ROUTES, default="balanced")
    parser.add_argument(
        "--task-kind",
        choices=("implementation", "diagnosis", "audit", "architecture", "planning", "plan_only"),
        default="implementation",
    )
    parser.add_argument(
        "--validation",
        choices=("deterministic", "partial"),
        default="deterministic",
    )
    parser.add_argument("--leadership", choices=("adaptive", "astra"), default="adaptive")
    parser.add_argument("--review", choices=("proportional", "astra"), default="proportional")
    parser.add_argument("--astra", choices=("auto", "ask", "disabled"), default="auto")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = recommend(
        args.complexity,
        args.risk,
        mode=args.mode,
        task_kind=args.task_kind,
        deterministic_validation=args.validation == "deterministic",
        leadership=args.leadership,
        review=args.review,
        astra=args.astra,
    )
    print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
