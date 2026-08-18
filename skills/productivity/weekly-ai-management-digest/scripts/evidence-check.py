#!/usr/bin/env python3
"""Validate Human Loop Weekly editorial evidence eligibility.

Usage:
    python scripts/evidence-check.py sources/source-register.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RATINGS = {"high", "medium", "low"}
CORE_RATINGS = {"high", "medium"}
ROLES = {"core", "watch"}
ACTION_TYPES = {"recommendation", "experiment"}


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(path: Path) -> int:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR register: cannot read valid JSON: {exc}")
        return 2

    errors: list[str] = []
    if not isinstance(payload, dict):
        print("ERROR register: root must be an object")
        return 2

    themes = payload.get("themes")
    if not isinstance(themes, list) or not themes:
        print("ERROR register: themes must be a non-empty array")
        return 1

    theme_by_id: dict[str, dict] = {}
    for index, theme in enumerate(themes, 1):
        prefix = f"theme[{index}]"
        if not isinstance(theme, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        theme_id = theme.get("id")
        if not isinstance(theme_id, str) or not theme_id.strip():
            errors.append(f"{prefix}: id is required")
            continue
        theme_id = theme_id.strip()
        if theme_id in theme_by_id:
            errors.append(f"{prefix}: duplicate id {theme_id!r}")
        theme_by_id[theme_id] = theme
        for field in ("title", "central_claim"):
            if not text(theme.get(field)):
                errors.append(f"{prefix}: {field} is required")
        rating = theme.get("evidence_rating")
        role = theme.get("editorial_role")
        if rating not in RATINGS:
            errors.append(f"{prefix}: evidence_rating must be one of {sorted(RATINGS)}")
        if role not in ROLES:
            errors.append(f"{prefix}: editorial_role must be one of {sorted(ROLES)}")
        elif role == "core" and rating not in CORE_RATINGS:
            errors.append(f"{prefix}: core claim requires medium or high evidence")
        elif role == "watch" and rating != "low":
            errors.append(f"{prefix}: watch signal must be rated low, or promoted to core")
        if not isinstance(theme.get("supported_action_ids"), list):
            errors.append(f"{prefix}: supported_action_ids must be an array")

    headline_ids = payload.get("headline_theme_ids")
    if not isinstance(headline_ids, list) or not headline_ids:
        errors.append("register: headline_theme_ids must be a non-empty array")
    else:
        for theme_id in headline_ids:
            theme = theme_by_id.get(theme_id) if isinstance(theme_id, str) else None
            if not theme:
                errors.append(f"headline: unknown theme {theme_id!r}")
            elif theme.get("editorial_role") != "core" or theme.get("evidence_rating") not in CORE_RATINGS:
                errors.append(f"headline: theme {theme_id!r} must be a medium/high core claim")

    actions = payload.get("actions")
    if not isinstance(actions, list):
        errors.append("register: actions must be an array")
        actions = []
    action_ids: set[str] = set()
    for index, action in enumerate(actions, 1):
        prefix = f"action[{index}]"
        if not isinstance(action, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        action_id = action.get("id")
        if not isinstance(action_id, str) or not action_id.strip():
            errors.append(f"{prefix}: id is required")
        elif action_id.strip() in action_ids:
            errors.append(f"{prefix}: duplicate id {action_id!r}")
        else:
            action_ids.add(action_id.strip())
        if not text(action.get("text")):
            errors.append(f"{prefix}: text is required")
        theme_id = action.get("theme_id")
        theme = theme_by_id.get(theme_id) if isinstance(theme_id, str) else None
        if not theme:
            errors.append(f"{prefix}: theme_id must name an existing theme")
        action_type = action.get("action_type")
        if action_type not in ACTION_TYPES:
            errors.append(f"{prefix}: action_type must be one of {sorted(ACTION_TYPES)}")
        rating = action.get("evidence_rating")
        if rating not in RATINGS:
            errors.append(f"{prefix}: evidence_rating must be one of {sorted(RATINGS)}")
        if action_type == "recommendation":
            if rating not in CORE_RATINGS:
                errors.append(f"{prefix}: recommendation requires medium or high evidence")
            if theme and (theme.get("editorial_role") != "core" or theme.get("evidence_rating") not in CORE_RATINGS):
                errors.append(f"{prefix}: recommendation must trace to a medium/high core claim")
        if action_type == "experiment" and not text(action.get("uncertainty_or_stop_condition")):
            errors.append(f"{prefix}: low-evidence experiment requires uncertainty_or_stop_condition")

    for theme_id, theme in theme_by_id.items():
        for action_id in theme.get("supported_action_ids", []):
            if action_id not in action_ids:
                errors.append(f"theme {theme_id!r}: supported action {action_id!r} does not exist")

    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"PASS: {len(theme_by_id)} theme(s), {len(actions)} action(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate core-claim and action evidence thresholds")
    parser.add_argument("register", type=Path, help="Path to source-register.json")
    return validate(parser.parse_args().register)


if __name__ == "__main__":
    sys.exit(main())
