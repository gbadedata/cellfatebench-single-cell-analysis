"""Answer validation utilities for CellFateBench."""

from __future__ import annotations

from typing import Any


def normalise_text(value: Any) -> str:
    """Normalise text for lightweight deterministic matching."""

    if isinstance(value, list):
        return " ".join(normalise_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{k} {normalise_text(v)}" for k, v in value.items())

    return str(value).lower().replace("_", " ").replace("-", " ").strip()


def contains_any(text: str, expected_terms: list[str]) -> bool:
    """Return True if text contains at least one expected term."""

    normalised = normalise_text(text)
    return any(normalise_text(term) in normalised for term in expected_terms)


def contains_all_required_terms(answer: dict[str, Any], required_terms: list[str]) -> tuple[int, int]:
    """Count required evidence terms found in a solver answer."""

    answer_text = normalise_text(answer)
    found = 0

    for term in required_terms:
        if normalise_text(term) in answer_text:
            found += 1

    return found, len(required_terms)


def field_value_matches(answer: dict[str, Any], field_candidates: list[str], expected_values: list[str]) -> bool:
    """Check whether any candidate answer field contains any expected value."""

    for field in field_candidates:
        if field not in answer:
            continue

        field_text = normalise_text(answer[field])
        for expected in expected_values:
            if normalise_text(expected) in field_text:
                return True

    return False


def boolean_field_matches(answer: dict[str, Any], field_candidates: list[str], expected_value: bool) -> bool:
    """Check whether a boolean answer field matches the expected value."""

    expected_text = str(expected_value).lower()

    for field in field_candidates:
        if field not in answer:
            continue

        value = answer[field]
        if isinstance(value, bool):
            return value is expected_value

        if normalise_text(value) == expected_text:
            return True

    return False
