from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

LEAGUE_DATA_COLUMNS = [
    "game_id",
    "game_start_utc",
    "game_duration",
    "game_mode",
    "game_type",
    "game_version",
    "map_id",
    "platform_id",
    "queue_id",
    "participant_id",
    "puuid",
    "summoner_name",
    "summoner_id",
    "summoner_level",
    "champion_id",
    "champion_name",
    "team_id",
    "win",
    "individual_position",
    "team_position",
    "lane",
    "role",
    "kills",
    "deaths",
    "assists",
    "baron_kills",
    "dragon_kills",
    "gold_earned",
    "gold_spent",
    "total_damage_dealt",
    "total_damage_dealt_to_champions",
    "physical_damage_dealt_to_champions",
    "magic_damage_dealt_to_champions",
    "true_damage_dealt_to_champions",
    "damage_dealt_to_objectives",
    "damage_dealt_to_turrets",
    "total_damage_taken",
    "physical_damage_taken",
    "magic_damage_taken",
    "true_damage_taken",
    "time_ccing_others",
    "vision_score",
    "wards_placed",
    "wards_killed",
    "vision_wards_bought_in_game",
    "item0",
    "item1",
    "item2",
    "item3",
    "item4",
    "item5",
    "item6",
    "solo_tier",
    "solo_rank",
    "solo_lp",
    "solo_wins",
    "solo_losses",
    "flex_tier",
    "flex_rank",
    "flex_lp",
    "flex_wins",
    "flex_losses",
    "champion_mastery_level",
    "champion_mastery_points",
    "champion_mastery_lastPlayTime",
    "champion_mastery_lastPlayTime_utc",
    "champion_mastery_pointsSinceLastLevel",
    "champion_mastery_pointsUntilNextLevel",
    "champion_mastery_tokensEarned",
    "final_abilityHaste",
    "final_abilityPower",
    "final_armor",
    "final_armorPen",
    "final_armorPenPercent",
    "final_attackDamage",
    "final_attackSpeed",
    "final_bonusArmorPenPercent",
    "final_bonusMagicPenPercent",
    "final_ccReduction",
    "final_cooldownReduction",
    "final_health",
    "final_healthMax",
    "final_healthRegen",
    "final_lifesteal",
    "final_magicPen",
    "final_magicPenPercent",
    "final_magicResist",
    "final_movementSpeed",
    "final_omnivamp",
    "final_physicalVamp",
    "final_power",
    "final_powerMax",
    "final_powerRegen",
    "final_spellVamp",
]

PARTICIPANT_FIELDS = {
    "participant_id": "participantId",
    "puuid": "puuid",
    "summoner_id": "summonerId",
    "summoner_level": "summonerLevel",
    "champion_id": "championId",
    "champion_name": "championName",
    "team_id": "teamId",
    "win": "win",
    "individual_position": "individualPosition",
    "team_position": "teamPosition",
    "lane": "lane",
    "role": "role",
    "kills": "kills",
    "deaths": "deaths",
    "assists": "assists",
    "baron_kills": "baronKills",
    "dragon_kills": "dragonKills",
    "gold_earned": "goldEarned",
    "gold_spent": "goldSpent",
    "total_damage_dealt": "totalDamageDealt",
    "total_damage_dealt_to_champions": "totalDamageDealtToChampions",
    "physical_damage_dealt_to_champions": "physicalDamageDealtToChampions",
    "magic_damage_dealt_to_champions": "magicDamageDealtToChampions",
    "true_damage_dealt_to_champions": "trueDamageDealtToChampions",
    "damage_dealt_to_objectives": "damageDealtToObjectives",
    "damage_dealt_to_turrets": "damageDealtToTurrets",
    "total_damage_taken": "totalDamageTaken",
    "physical_damage_taken": "physicalDamageTaken",
    "magic_damage_taken": "magicDamageTaken",
    "true_damage_taken": "trueDamageTaken",
    "time_ccing_others": "timeCCingOthers",
    "vision_score": "visionScore",
    "wards_placed": "wardsPlaced",
    "wards_killed": "wardsKilled",
    "vision_wards_bought_in_game": "visionWardsBoughtInGame",
    **{f"item{i}": f"item{i}" for i in range(7)},
}

MASTERY_FIELDS = {
    "champion_mastery_level": "championLevel",
    "champion_mastery_points": "championPoints",
    "champion_mastery_lastPlayTime": "lastPlayTime",
    "champion_mastery_pointsSinceLastLevel": "championPointsSinceLastLevel",
    "champion_mastery_pointsUntilNextLevel": "championPointsUntilNextLevel",
    "champion_mastery_tokensEarned": "tokensEarned",
}

FINAL_FIELDS = {
    "final_abilityHaste": "abilityHaste",
    "final_abilityPower": "abilityPower",
    "final_armor": "armor",
    "final_armorPen": "armorPen",
    "final_armorPenPercent": "armorPenPercent",
    "final_attackDamage": "attackDamage",
    "final_attackSpeed": "attackSpeed",
    "final_bonusArmorPenPercent": "bonusArmorPenPercent",
    "final_bonusMagicPenPercent": "bonusMagicPenPercent",
    "final_ccReduction": "ccReduction",
    "final_cooldownReduction": "cooldownReduction",
    "final_health": "health",
    "final_healthMax": "healthMax",
    "final_healthRegen": "healthRegen",
    "final_lifesteal": "lifesteal",
    "final_magicPen": "magicPen",
    "final_magicPenPercent": "magicPenPercent",
    "final_magicResist": "magicResist",
    "final_movementSpeed": "movementSpeed",
    "final_omnivamp": "omnivamp",
    "final_physicalVamp": "physicalVamp",
    "final_power": "power",
    "final_powerMax": "powerMax",
    "final_powerRegen": "powerRegen",
    "final_spellVamp": "spellVamp",
}


def milliseconds_to_utc(value: Any) -> datetime | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value / 1000, tz=UTC).replace(tzinfo=None)


def filter_match_ids(match_ids: list[Any], count: int = 20) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in match_ids:
        if isinstance(value, str) and value.startswith("KR_") and value not in seen:
            result.append(value)
            seen.add(value)
        if len(result) >= count:
            break
    return result


def get_last_participant_frames(timeline: dict[str, Any]) -> dict[str, Any]:
    frames = timeline.get("info", {}).get("frames", [])
    for frame in reversed(frames if isinstance(frames, list) else []):
        participant_frames = frame.get("participantFrames") if isinstance(frame, dict) else None
        if isinstance(participant_frames, dict) and participant_frames:
            return participant_frames
    return {}


def build_league_rows(
    matches: list[dict[str, Any]],
    timelines: dict[str, dict[str, Any]],
    ranks: dict[str, dict[str, Any]],
    masteries: dict[tuple[str, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, Any]] = set()
    for match in matches:
        metadata = match.get("metadata", {})
        info = match.get("info", {})
        game_id = metadata.get("matchId")
        if not isinstance(game_id, str) or not game_id.startswith("KR_"):
            continue
        if info.get("queueId") != 420 or str(info.get("platformId", "")).upper() != "KR":
            continue
        participant_frames = get_last_participant_frames(timelines.get(game_id, {}))
        participants = info.get("participants", [])
        for participant in participants if isinstance(participants, list) else []:
            participant_id = participant.get("participantId")
            key = (game_id, participant_id)
            if key in seen:
                continue
            seen.add(key)
            row = {column: None for column in LEAGUE_DATA_COLUMNS}
            row.update(
                {
                    "game_id": game_id,
                    "game_start_utc": milliseconds_to_utc(info.get("gameStartTimestamp")),
                    "game_duration": info.get("gameDuration"),
                    "game_mode": info.get("gameMode"),
                    "game_type": info.get("gameType"),
                    "game_version": info.get("gameVersion"),
                    "map_id": info.get("mapId"),
                    "platform_id": info.get("platformId"),
                    "queue_id": info.get("queueId"),
                    "summoner_name": participant.get("riotIdGameName")
                    or participant.get("summonerName"),
                }
            )
            for column, api_field in PARTICIPANT_FIELDS.items():
                row[column] = participant.get(api_field)
            puuid = participant.get("puuid")
            rank = ranks.get(puuid, {}) if isinstance(puuid, str) else {}
            row.update(
                {
                    "solo_tier": rank.get("tier"),
                    "solo_rank": rank.get("rank"),
                    "solo_lp": rank.get("leaguePoints"),
                    "solo_wins": rank.get("wins"),
                    "solo_losses": rank.get("losses"),
                }
            )
            champion_id = participant.get("championId")
            mastery = masteries.get((puuid, champion_id), {}) if isinstance(puuid, str) else {}
            for column, api_field in MASTERY_FIELDS.items():
                row[column] = mastery.get(api_field)
            row["champion_mastery_lastPlayTime_utc"] = milliseconds_to_utc(
                mastery.get("lastPlayTime")
            )
            frame = participant_frames.get(str(participant_id), {})
            champion_stats = frame.get("championStats", {}) if isinstance(frame, dict) else {}
            for column, api_field in FINAL_FIELDS.items():
                row[column] = champion_stats.get(api_field)
            rows.append(row)
    return rows


def validate_league_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    expected = set(LEAGUE_DATA_COLUMNS)
    if len(rows) > 200:
        errors.append(f"데이터 행 수가 최대 200행을 초과했습니다({len(rows)}행).")
    keys = [(row.get("game_id"), row.get("participant_id")) for row in rows]
    for index, row in enumerate(rows, 2):
        if list(row) != LEAGUE_DATA_COLUMNS or set(row) != expected:
            errors.append(f"{index}행의 컬럼 구조가 94개 고정 스키마와 다릅니다.")
        if row.get("queue_id") != 420:
            errors.append(f"{index}행 queue_id가 420이 아닙니다.")
        if str(row.get("platform_id", "")).upper() != "KR":
            errors.append(f"{index}행 platform_id가 KR이 아닙니다.")
        if not str(row.get("game_id", "")).startswith("KR_"):
            errors.append(f"{index}행 game_id가 KR_로 시작하지 않습니다.")
        if row.get("win") is not None and not isinstance(row.get("win"), bool):
            errors.append(f"{index}행 win 값이 Boolean이 아닙니다.")
        for utc_column in ("game_start_utc", "champion_mastery_lastPlayTime_utc"):
            if row.get(utc_column) is not None and not isinstance(row.get(utc_column), datetime):
                errors.append(f"{index}행 {utc_column} 값이 날짜·시간 형식이 아닙니다.")
        if any(
            row.get(column) is not None
            for column in LEAGUE_DATA_COLUMNS
            if column.startswith("flex_")
        ):
            errors.append(f"{index}행 flex_* 값은 비어 있어야 합니다.")
    duplicates = [key for key, occurrences in Counter(keys).items() if occurrences > 1]
    if duplicates:
        errors.append("game_id + participant_id 중복이 있습니다.")
    for game_id, count in Counter(row.get("game_id") for row in rows).items():
        if count != 10:
            errors.append(f"{game_id}의 참가자 수가 10명이 아닙니다({count}명).")
    return errors
