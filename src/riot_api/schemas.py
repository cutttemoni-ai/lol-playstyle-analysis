from __future__ import annotations

from typing import Any

from pydantic import RootModel, model_validator

from .parser import LEAGUE_DATA_COLUMNS


class LeagueRowSchema(RootModel[dict[str, Any]]):
    """94개 컬럼의 이름과 순서를 모두 고정하는 행 스키마."""

    @model_validator(mode="after")
    def exact_columns(self) -> LeagueRowSchema:
        if list(self.root) != LEAGUE_DATA_COLUMNS:
            raise ValueError("league_data 행은 지정된 94개 컬럼과 순서가 정확히 같아야 합니다.")
        return self
