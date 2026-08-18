#!/usr/bin/env python3
"""Validate a cross-issue early-signal register.

Usage:
    python scripts/signal-register-check.py signals/signal-register.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

STATUSES = {"active", "confirmed", "expired", "disproved"}
RATINGS = {"low", "medium", "high"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_date(value: object) -> bool:
    return isinstance(value, str) and bool(DATE_RE.match(value.strip()))


def validate(path: Path) -> int:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR register: cannot read valid JSON: {exc}")
        return 2
    if not isinstance(payload, dict):
        print("ERROR register: root must be an object")
        return 2

    errors: list[str] = []
    signals = payload.get("signals")
    if not isinstance(signals, list):
        errors.append("register: signals must be an array")
        signals = []
    ids: set[str] = set()
    for index, signal in enumerate(signals, 1):
        prefix = f"signal[{index}]"
        if not isinstance(signal, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        signal_id = signal.get("signal_id")
        if not isinstance(signal_id, str) or not signal_id.strip():
            errors.append(f"{prefix}: signal_id is required")
        elif signal_id.strip() in ids:
            errors.append(f"{prefix}: duplicate signal_id {signal_id!r}")
        else:
            ids.add(signal_id.strip())
        for field in ("statement", "scope", "why_it_matters", "first_issue_id"):
            if not nonempty(signal.get(field)):
                errors.append(f"{prefix}: {field} is required")
        for field in ("first_observed_at", "review_after"):
            if not valid_date(signal.get(field)):
                errors.append(f"{prefix}: {field} must start with YYYY-MM-DD")
        status = signal.get("status")
        rating = signal.get("evidence_rating")
        if status not in STATUSES:
            errors.append(f"{prefix}: status must be one of {sorted(STATUSES)}")
        if rating not in RATINGS:
            errors.append(f"{prefix}: evidence_rating must be one of {sorted(RATINGS)}")
        if status == "active" and rating != "low":
            errors.append(f"{prefix}: active signal must be low evidence")
        if status == "confirmed" and rating not in {"medium", "high"}:
            errors.append(f"{prefix}: confirmed signal requires medium or high evidence")
        sources = signal.get("source_refs")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{prefix}: source_refs must be a non-empty array")
        else:
            for source_index, source in enumerate(sources, 1):
                if not isinstance(source, dict) or not nonempty(source.get("url")):
                    errors.append(f"{prefix}.source_refs[{source_index}]: URL is required")
                    continue
                parsed = urlparse(source["url"])
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    errors.append(f"{prefix}.source_refs[{source_index}]: URL must be absolute HTTP(S)")
        log = signal.get("review_log")
        if not isinstance(log, list) or not log:
            errors.append(f"{prefix}: review_log must be a non-empty array")
        else:
            last = log[-1] if isinstance(log[-1], dict) else {}
            if last.get("status") != status:
                errors.append(f"{prefix}: latest review_log status must equal current status")
            for review_index, review in enumerate(log, 1):
                if not isinstance(review, dict):
                    errors.append(f"{prefix}.review_log[{review_index}]: must be an object")
                    continue
                if not valid_date(review.get("reviewed_at")):
                    errors.append(f"{prefix}.review_log[{review_index}]: reviewed_at must start with YYYY-MM-DD")
                if review.get("status") not in STATUSES:
                    errors.append(f"{prefix}.review_log[{review_index}]: invalid status")
                if not nonempty(review.get("reason")):
                    errors.append(f"{prefix}.review_log[{review_index}]: reason is required")

    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"PASS: {len(signals)} signal(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Human Loop Weekly signal register")
    parser.add_argument("register", type=Path)
    return validate(parser.parse_args().register)


if __name__ == "__main__":
    sys.exit(main())
