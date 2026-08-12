#!/usr/bin/env python3
"""Validate source freshness for the weekly AI management digest.

Usage:
    python scripts/freshness-check.py sources/source-register.json
    python scripts/freshness-check.py sources/source-register.json --publication
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

DAY = 86400
ALLOWED_ROLES = {"weekly_signal", "supporting", "major_research"}
ALLOWED_CHANGES = {
    "new_research",
    "new_dataset",
    "new_result",
    "follow_up",
    "methodology_update",
    "correction",
    "revised_conclusion",
    "article_publication",
}
MAJOR_TYPES = {
    "randomized_study",
    "longitudinal_study",
    "systematic_review",
    "large_independent_survey",
    "major_dataset",
    "recurring_research_report",
    "independent_research",
}


def parse_dt(value: object, field: str, default_tz) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is missing")
    raw = value.strip().replace("Z", "+00:00")
    try:
        result = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO-8601, got {value!r}") from exc
    if result.tzinfo is None:
        result = result.replace(tzinfo=default_tz)
    return result


def age_days(window_end: datetime, value: datetime) -> float:
    return (window_end - value.astimezone(window_end.tzinfo)).total_seconds() / DAY


def nonempty(source: dict, field: str) -> bool:
    value = source.get(field)
    return isinstance(value, str) and bool(value.strip())


def validate(path: Path, publication: bool, supersession_max_age: float) -> int:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR register: cannot read valid JSON: {exc}")
        return 2

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        print("ERROR register: root must be an object")
        return 2

    raw_window_end = payload.get("window_end")
    try:
        provisional = datetime.fromisoformat(str(raw_window_end).replace("Z", "+00:00"))
        if provisional.tzinfo is None:
            raise ValueError("timezone offset required")
        window_end = provisional
    except (TypeError, ValueError):
        print("ERROR register: window_end must be ISO-8601 with timezone offset")
        return 2

    if publication and payload.get("publication_recheck_completed") is not True:
        errors.append("register: publication_recheck_completed must be true for --publication")

    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("register: sources must be a non-empty array")
        sources = []

    seen_ids: set[str] = set()
    weekly_count = 0

    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            errors.append(f"source[{index}]: must be an object")
            continue

        sid = str(source.get("id") or f"source[{index}]")
        prefix = sid
        if sid in seen_ids:
            errors.append(f"{prefix}: duplicate id")
        seen_ids.add(sid)

        role = source.get("role")
        if role not in ALLOWED_ROLES:
            errors.append(f"{prefix}: role must be one of {sorted(ALLOWED_ROLES)}")
            continue
        if role == "weekly_signal":
            weekly_count += 1

        for field in ("title", "canonical_url", "source_type", "change_summary", "claim", "methodology_summary", "supersession_query"):
            if not nonempty(source, field):
                errors.append(f"{prefix}: {field} is required")

        url = source.get("canonical_url")
        if isinstance(url, str):
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{prefix}: canonical_url must be an absolute HTTP(S) URL")

        change_type = source.get("change_type")
        if change_type not in ALLOWED_CHANGES:
            errors.append(f"{prefix}: change_type must be one of {sorted(ALLOWED_CHANGES)}")

        parsed_dates: dict[str, datetime] = {}
        for field in ("published_at", "event_at", "evidence_date", "supersession_checked_at"):
            try:
                parsed_dates[field] = parse_dt(source.get(field), field, window_end.tzinfo)
            except ValueError as exc:
                errors.append(f"{prefix}: {exc}")

        updated = source.get("updated_at")
        if updated not in (None, ""):
            try:
                parsed_dates["updated_at"] = parse_dt(updated, "updated_at", window_end.tzinfo)
            except ValueError as exc:
                errors.append(f"{prefix}: {exc}")

        if "published_at" in parsed_dates and "updated_at" in parsed_dates:
            if parsed_dates["updated_at"] < parsed_dates["published_at"]:
                errors.append(f"{prefix}: updated_at cannot precede published_at")

        if "evidence_date" in parsed_dates:
            evidence_age = age_days(window_end, parsed_dates["evidence_date"])
            if evidence_age < -1:
                errors.append(f"{prefix}: evidence_date is in the future")
            if role == "supporting" and evidence_age > 60:
                errors.append(f"{prefix}: supporting evidence is {evidence_age:.1f} days old; maximum is 60")
            elif role == "major_research" and evidence_age > 180:
                errors.append(f"{prefix}: major research is {evidence_age:.1f} days old; maximum is 180")
            elif role == "weekly_signal":
                limit = 180 if source.get("is_major") is True else 60
                if evidence_age > limit:
                    errors.append(f"{prefix}: weekly signal uses evidence {evidence_age:.1f} days old; maximum is {limit}")

        if role == "weekly_signal" and "event_at" in parsed_dates:
            event_age = age_days(window_end, parsed_dates["event_at"])
            if event_age < -0.05 or event_age > 7:
                errors.append(f"{prefix}: weekly event is {event_age:.1f} days old; must be within 0–7 days")

        if "supersession_checked_at" in parsed_dates:
            check_age = age_days(window_end, parsed_dates["supersession_checked_at"])
            if check_age < -0.05:
                errors.append(f"{prefix}: supersession_checked_at is in the future")
            elif check_age > supersession_max_age:
                errors.append(
                    f"{prefix}: supersession check is {check_age:.1f} days old; maximum is {supersession_max_age:g}"
                )

        if source.get("superseded_by") not in (None, ""):
            errors.append(f"{prefix}: source is superseded by {source.get('superseded_by')!r}; rebuild the claim")

        if source.get("is_primary") is not True:
            warnings.append(f"{prefix}: source is not marked primary; verify and prefer the canonical origin")

        if role == "major_research" or source.get("is_major") is True:
            if source.get("is_major") is not True:
                errors.append(f"{prefix}: major_research requires is_major=true")
            if source.get("source_type") not in MAJOR_TYPES:
                errors.append(f"{prefix}: source_type does not qualify for the 180-day major-research exception")
            if not nonempty(source, "sample_size"):
                errors.append(f"{prefix}: major research requires sample_size or dataset coverage")

        if change_type in {"follow_up", "methodology_update", "correction", "revised_conclusion"}:
            if "updated_at" not in parsed_dates:
                errors.append(f"{prefix}: {change_type} requires updated_at")

    if weekly_count == 0:
        errors.append("register: at least one weekly_signal is required")

    for item in warnings:
        print(f"WARN  {item}")
    for item in errors:
        print(f"ERROR {item}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"PASS: {len(sources)} source(s), {weekly_count} weekly signal(s), {len(warnings)} warning(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate 7/60/180-day source freshness gates")
    parser.add_argument("register", type=Path, help="Path to source-register.json")
    parser.add_argument("--publication", action="store_true", help="Require publication-day recheck completion")
    parser.add_argument(
        "--supersession-max-age",
        type=float,
        default=2.0,
        help="Maximum age in days for the supersession check (default: 2)",
    )
    args = parser.parse_args()
    return validate(args.register, args.publication, args.supersession_max_age)


if __name__ == "__main__":
    sys.exit(main())
