from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from export_recent_matches import parse_args  # noqa: E402


def test_timeline_compatibility_option_is_accepted():
    args = parse_args(["--game-name", "Hide on bush", "--tag-line", "KR1", "--timeline"])
    assert args.timeline is True
