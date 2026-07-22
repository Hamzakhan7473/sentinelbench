"""Deterministic scoring helpers."""

from __future__ import annotations

from typing import Iterable


def exact_match(predicted: object, expected: object) -> float:
    return 1.0 if predicted == expected else 0.0


def set_precision_recall_f1(
    predicted: Iterable[str],
    expected: Iterable[str],
) -> dict[str, float]:
    pred = {str(x) for x in predicted}
    exp = {str(x) for x in expected}
    if not pred and not exp:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    intersection = pred & exp
    precision = len(intersection) / len(pred) if pred else 0.0
    recall = len(intersection) / len(exp) if exp else 0.0
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return {"precision": precision, "recall": recall, "f1": f1}
