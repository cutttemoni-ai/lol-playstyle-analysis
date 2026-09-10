from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class CollectionError:
    stage: str
    puuid: str | None = None
    match_id: str | None = None
    champion_id: int | None = None
    api_type: str | None = None
    status_code: int | None = None
    message: str = ""
    retries: int = 0


@dataclass(slots=True)
class CollectionResult:
    account: dict[str, Any]
    summoner: dict[str, Any]
    matches: list[dict[str, Any]] = field(default_factory=list)
    timelines: dict[str, dict[str, Any]] = field(default_factory=dict)
    ranks: dict[str, dict[str, Any]] = field(default_factory=dict)
    masteries: dict[tuple[str, int], dict[str, Any]] = field(default_factory=dict)
    errors: list[CollectionError] = field(default_factory=list)
    requested_count: int = 20
    started_at: datetime | None = None
    completed_at: datetime | None = None
