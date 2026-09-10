from __future__ import annotations

import pytest
from pydantic import ValidationError

from riot_api.parser import LEAGUE_DATA_COLUMNS
from riot_api.schemas import LeagueRowSchema


def test_schema_accepts_exact_94_columns():
    row = {column: None for column in LEAGUE_DATA_COLUMNS}
    assert list(LeagueRowSchema.model_validate(row).root) == LEAGUE_DATA_COLUMNS


@pytest.mark.parametrize("mutation", ["missing", "added", "reordered"])
def test_schema_rejects_any_column_change(mutation):
    row = {column: None for column in LEAGUE_DATA_COLUMNS}
    if mutation == "missing":
        row.pop("game_id")
    elif mutation == "added":
        row["unexpected"] = None
    else:
        row = dict(reversed(list(row.items())))
    with pytest.raises(ValidationError):
        LeagueRowSchema.model_validate(row)
