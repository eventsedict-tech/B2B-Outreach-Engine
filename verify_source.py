"""Fail the image build if required local application modules are absent."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "src/cleaning/normalizer.py", "src/cleaning/deduplicator.py",
    "src/qualification/lead_scorer.py", "src/personalization/generator.py",
    "src/state_machine/lead_lifecycle.py", "src/reply_classifier/classifier.py",
    "src/outreach/email_sender.py", "src/outreach/whatsapp_sender.py",
    "src/outreach/linkedin_queue.py", "src/analytics/daily_reporter.py",
]
missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
if missing:
    print("ERROR: Missing required source files:", file=sys.stderr)
    for item in missing: print(f" - {item}", file=sys.stderr)
    raise SystemExit(1)
print(f"Source verification passed ({len(REQUIRED)} modules).")
