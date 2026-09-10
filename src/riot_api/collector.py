from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote

from .client import RiotAPIClient, RiotAPIError
from .models import CollectionError, CollectionResult
from .parser import filter_match_ids

ASIA = "https://asia.api.riotgames.com"
KR = "https://kr.api.riotgames.com"


class RiotMatchCollector:
    def __init__(self, client: RiotAPIClient) -> None:
        self.client = client
        self.rank_cache: dict[str, dict[str, Any]] = {}
        self.mastery_cache: dict[tuple[str, int], dict[str, Any]] = {}
        self.match_cache: dict[str, dict[str, Any]] = {}
        self.timeline_cache: dict[str, dict[str, Any]] = {}

    def collect(self, game_name: str, tag_line: str, count: int = 20) -> CollectionResult:
        started_at = datetime.now(UTC)
        encoded_game_name = quote(game_name, safe="")
        encoded_tag_line = quote(tag_line, safe="")
        account = self.client.get_json(
            f"{ASIA}/riot/account/v1/accounts/by-riot-id/{encoded_game_name}/{encoded_tag_line}"
        )
        puuid = account.get("puuid")
        if not puuid:
            raise RiotAPIError("계정 응답에 PUUID가 없어 수집을 계속할 수 없습니다.")
        try:
            summoner = self.client.get_json(
                f"{KR}/lol/summoner/v4/summoners/by-puuid/{quote(puuid, safe='')}"
            )
        except RiotAPIError as exc:
            if exc.status_code == 404:
                raise RiotAPIError(
                    "해당 Riot ID를 한국 서버 계정으로 확인할 수 없습니다.", 404, exc.retries
                ) from exc
            raise

        raw_ids = self.client.get_json(
            f"{ASIA}/lol/match/v5/matches/by-puuid/{quote(puuid, safe='')}/ids",
            params={"queue": 420, "start": 0, "count": min(max(count, 1), 20)},
        )
        match_ids = filter_match_ids(raw_ids if isinstance(raw_ids, list) else [], count)
        result = CollectionResult(
            account=account, summoner=summoner, requested_count=count, started_at=started_at
        )
        if len(match_ids) < count:
            print(
                f"경고: 요청한 {count}경기 중 {len(match_ids)}개의 KR 솔로랭크 경기만 확인했습니다."
            )

        for index, match_id in enumerate(match_ids, 1):
            try:
                match = self.get_match(match_id)
                info = match.get("info", {})
                participants = info.get("participants", [])
                if info.get("queueId") != 420 or str(info.get("platformId", "")).upper() != "KR":
                    continue
                if match.get("metadata", {}).get("matchId") != match_id:
                    continue
                if not any(p.get("puuid") == puuid for p in participants):
                    continue
                result.matches.append(match)
            except RiotAPIError as exc:
                result.errors.append(
                    self._error("경기 상세", exc, match_id=match_id, api_type="MATCH-V5")
                )
                print(f"{index}/{len(match_ids)} 경기 수집 실패")
                continue

            try:
                result.timelines[match_id] = self.get_timeline(match_id)
            except RiotAPIError as exc:
                result.errors.append(
                    self._error("타임라인", exc, match_id=match_id, api_type="MATCH-V5")
                )
            print(f"{index}/{len(match_ids)} 경기 수집 완료")

        unique_puuids: set[str] = set()
        mastery_keys: set[tuple[str, int]] = set()
        for match in result.matches:
            for participant in match.get("info", {}).get("participants", []):
                participant_puuid = participant.get("puuid")
                champion_id = participant.get("championId")
                if isinstance(participant_puuid, str) and participant_puuid:
                    unique_puuids.add(participant_puuid)
                    if isinstance(champion_id, int):
                        mastery_keys.add((participant_puuid, champion_id))

        for participant_puuid in unique_puuids:
            result.ranks[participant_puuid] = self.get_solo_rank(participant_puuid, result.errors)
        for participant_puuid, champion_id in mastery_keys:
            result.masteries[(participant_puuid, champion_id)] = self.get_mastery(
                participant_puuid, champion_id, result.errors
            )
        result.completed_at = datetime.now(UTC)
        return result

    def get_solo_rank(self, puuid: str, errors: list[CollectionError]) -> dict[str, Any]:
        if puuid in self.rank_cache:
            return self.rank_cache[puuid]
        result: dict[str, Any] = {}
        try:
            entries = self.client.get_json(
                f"{KR}/lol/league/v4/entries/by-puuid/{quote(puuid, safe='')}"
            )
            result = next(
                (entry for entry in entries if entry.get("queueType") == "RANKED_SOLO_5x5"), {}
            )
        except RiotAPIError as exc:
            errors.append(self._error("랭크", exc, puuid=puuid, api_type="SUMMONER-V4/LEAGUE-V4"))
        self.rank_cache[puuid] = result
        return result

    def get_mastery(
        self, puuid: str, champion_id: int, errors: list[CollectionError]
    ) -> dict[str, Any]:
        key = (puuid, champion_id)
        if key in self.mastery_cache:
            return self.mastery_cache[key]
        result: dict[str, Any] = {}
        try:
            result = self.client.get_json(
                f"{KR}/lol/champion-mastery/v4/champion-masteries/by-puuid/"
                f"{quote(puuid, safe='')}/by-champion/{champion_id}"
            )
        except RiotAPIError as exc:
            errors.append(
                self._error(
                    "챔피언 숙련도",
                    exc,
                    puuid=puuid,
                    champion_id=champion_id,
                    api_type="CHAMPION-MASTERY-V4",
                )
            )
        self.mastery_cache[key] = result
        return result

    def get_match(self, match_id: str) -> dict[str, Any]:
        if match_id not in self.match_cache:
            self.match_cache[match_id] = self.client.get_json(
                f"{ASIA}/lol/match/v5/matches/{quote(match_id, safe='')}"
            )
        return self.match_cache[match_id]

    def get_timeline(self, match_id: str) -> dict[str, Any]:
        if match_id not in self.timeline_cache:
            self.timeline_cache[match_id] = self.client.get_json(
                f"{ASIA}/lol/match/v5/matches/{quote(match_id, safe='')}/timeline"
            )
        return self.timeline_cache[match_id]

    @staticmethod
    def _error(stage: str, exc: RiotAPIError, **kwargs: Any) -> CollectionError:
        return CollectionError(
            stage=stage,
            status_code=exc.status_code,
            message=str(exc),
            retries=exc.retries,
            **kwargs,
        )
