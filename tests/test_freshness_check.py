import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/productivity/weekly-ai-management-digest/scripts/freshness-check.py"


def source(**updates):
    item = {
        "id": "S1",
        "role": "weekly_signal",
        "title": "Current primary research",
        "canonical_url": "https://example.org/research",
        "source_type": "independent_research",
        "published_at": "2026-08-08",
        "updated_at": None,
        "event_at": "2026-08-08",
        "evidence_date": "2026-08-08",
        "change_type": "new_research",
        "change_summary": "New measured findings appeared inside the weekly window.",
        "claim": "A measured claim.",
        "is_primary": True,
        "is_major": False,
        "methodology_summary": "Transparent measurement design.",
        "sample_size": "n=100",
        "supersession_checked_at": "2026-08-11T10:00:00+05:00",
        "supersession_query": "Title plus update/follow-up/revised/correction and official index",
        "superseded_by": None,
    }
    item.update(updates)
    return item


class FreshnessCheckTests(unittest.TestCase):
    def run_validator(self, sources, *, publication=False, rechecked=False):
        payload = {
            "window_end": "2026-08-11T12:00:00+05:00",
            "publication_recheck_completed": rechecked,
            "sources": sources,
        }
        with tempfile.TemporaryDirectory() as tmp:
            register = Path(tmp) / "register.json"
            register.write_text(json.dumps(payload), encoding="utf-8")
            command = [sys.executable, str(SCRIPT), str(register)]
            if publication:
                command.append("--publication")
            return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_valid_weekly_signal_passes(self):
        result = self.run_validator([source()])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_stale_weekly_event_fails(self):
        result = self.run_validator([source(event_at="2026-07-01")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("must be within 0–7 days", result.stdout)

    def test_stale_supporting_evidence_fails(self):
        supporting = source(
            role="supporting",
            event_at="2026-06-01",
            evidence_date="2026-01-01",
        )
        result = self.run_validator([source(), supporting])
        self.assertEqual(result.returncode, 1)
        self.assertIn("maximum is 60", result.stdout)

    def test_major_exception_requires_qualification(self):
        major = source(
            role="major_research",
            event_at="2026-04-01",
            evidence_date="2026-04-01",
            is_major=False,
            source_type="vendor_blog",
            sample_size="",
        )
        result = self.run_validator([source(), major])
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires is_major=true", result.stdout)
        self.assertIn("does not qualify", result.stdout)

    def test_superseded_source_fails(self):
        result = self.run_validator([source(superseded_by="https://example.org/revised")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("source is superseded", result.stdout)

    def test_publication_requires_final_recheck(self):
        result = self.run_validator([source()], publication=True, rechecked=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("publication_recheck_completed", result.stdout)

    def test_publication_passes_after_recheck(self):
        result = self.run_validator([source()], publication=True, rechecked=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
