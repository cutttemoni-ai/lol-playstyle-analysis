from __future__ import annotations

import json
from pathlib import Path

from riot_api.parser import LEAGUE_DATA_COLUMNS, build_league_rows, filter_match_ids

FIXTURES = Path(__file__).parent / "fixtures"

EXPECTED_COLUMNS = """
game_id game_start_utc game_duration game_mode game_type game_version map_id platform_id queue_id
participant_id puuid summoner_name summoner_id summoner_level champion_id champion_name team_id win
individual_position team_position lane role kills deaths assists baron_kills dragon_kills
gold_earned
gold_spent total_damage_dealt total_damage_dealt_to_champions physical_damage_dealt_to_champions
magic_damage_dealt_to_champions true_damage_dealt_to_champions damage_dealt_to_objectives
damage_dealt_to_turrets total_damage_taken physical_damage_taken magic_damage_taken
true_damage_taken time_ccing_others vision_score wards_placed wards_killed
vision_wards_bought_in_game item0 item1 item2 item3 item4 item5 item6 solo_tier solo_rank
solo_lp solo_wins solo_losses flex_tier flex_rank flex_lp
flex_wins flex_losses champion_mastery_level champion_mastery_points champion_mastery_lastPlayTime
champion_mastery_lastPlayTime_utc champion_mastery_pointsSinceLastLevel
champion_mastery_pointsUntilNextLevel champion_mastery_tokensEarned final_abilityHaste
final_abilityPower final_armor final_armorPen final_armorPenPercent final_attackDamage
final_attackSpeed
final_bonusArmorPenPercent final_bonusMagicPenPercent final_ccReduction final_cooldownReduction
final_health final_healthMax final_healthRegen final_lifesteal final_magicPen final_magicPenPercent
final_magicResist final_movementSpeed final_omnivamp final_physicalVamp final_power final_powerMax
final_powerRegen final_spellVamp
""".split()


def fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_columns_are_exactly_94_and_ordered():
    assert len(LEAGUE_DATA_COLUMNS) == 94
    assert LEAGUE_DATA_COLUMNS == EXPECTED_COLUMNS
    assert len(set(LEAGUE_DATA_COLUMNS)) == 94


def test_match_id_filter_keeps_only_kr_and_deduplicates():
    ids = ["KR_1", "NA1_2", "KR_1", "KR_3", None]
    assert filter_match_ids(ids, 20) == ["KR_1", "KR_3"]


def test_non_420_and_non_kr_match_rows_are_removed():
    match = fixture("match.json")
    match["info"]["queueId"] = 440
    assert build_league_rows([match], {}, {}, {}) == []
    match["info"]["queueId"] = 420
    match["metadata"]["matchId"] = "NA1_1"
    assert build_league_rows([match], {}, {}, {}) == []


def test_last_timeline_frame_supplies_final_stats_and_missing_fields_are_blank():
    match = fixture("match.json")
    timeline = fixture("timeline.json")
    rows = build_league_rows([match], {"KR_123456789": timeline}, {}, {})
    assert rows[0]["final_health"] == 1234
    assert rows[0]["final_abilityPower"] == 420
    assert rows[0]["final_spellVamp"] is None


def test_participant_puuid_and_name_priority_are_preserved():
    match = fixture("match.json")
    participant = match["info"]["participants"][0]
    participant["puuid"] = "expected-puuid"
    participant["riotIdGameName"] = "Current Riot Name"
    participant["summonerName"] = "Stale Summoner Name"
    row = build_league_rows([match], {}, {}, {})[0]
    assert row["puuid"] == "expected-puuid"
    assert row["summoner_name"] == "Current Riot Name"


def test_duplicate_game_and_participant_pair_is_removed():
    match = fixture("match.json")
    duplicated = json.loads(json.dumps(match))
    rows = build_league_rows([match, duplicated], {}, {}, {})
    assert len(rows) == len(match["info"]["participants"])
    assert len({(row["game_id"], row["participant_id"]) for row in rows}) == len(rows)


def test_flex_columns_exist_and_remain_blank():
    rows = build_league_rows([fixture("match.json")], {}, {}, {})
    flex_columns = [column for column in LEAGUE_DATA_COLUMNS if column.startswith("flex_")]
    assert flex_columns == ["flex_tier", "flex_rank", "flex_lp", "flex_wins", "flex_losses"]
    assert all(rows[0][column] is None for column in flex_columns)


def test_missing_or_added_column_is_detectable():
    row = build_league_rows([fixture("match.json")], {}, {}, {})[0]
    assert list(row) == LEAGUE_DATA_COLUMNS
    row.pop("game_id")
    assert list(row) != LEAGUE_DATA_COLUMNS
    row["extra"] = None
    assert set(row) != set(LEAGUE_DATA_COLUMNS)


def test_twenty_matches_produce_at_most_200_rows():
    template = fixture("match.json")
    participants = []
    for participant_id in range(1, 11):
        participant = dict(template["info"]["participants"][0])
        participant.update({"participantId": participant_id, "puuid": f"p-{participant_id}"})
        participants.append(participant)
    matches = []
    for match_number in range(20):
        match = json.loads(json.dumps(template))
        match["metadata"]["matchId"] = f"KR_{match_number}"
        match["info"]["participants"] = participants
        matches.append(match)
    assert len(build_league_rows(matches, {}, {}, {})) == 200
