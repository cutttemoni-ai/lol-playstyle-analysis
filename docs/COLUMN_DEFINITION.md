# 94개 컬럼 정의서

`league_data` 시트는 아래 이름과 순서를 정확히 유지합니다. API에서 제공하지 않는 값은 빈칸으로 두며, `flex_*`는 호환용으로 항상 비어 있습니다. `baron_kills`와 `dragon_kills`는 참가자 응답의 개인 필드가 있을 때만 기록합니다.

| No. | 컬럼명 | 분류 | 설명 | 출처 | API 필드 |
|---:|---|---|---|---|---|
| 1 | game_id | 경기 | 경기 메타데이터 game_id | MATCH-V5 | `metadata.matchId` |
| 2 | game_start_utc | 경기 | 경기 메타데이터 game_start_utc | MATCH-V5 | `info.gameStartTimestamp` |
| 3 | game_duration | 경기 | 경기 메타데이터 game_duration | MATCH-V5 | `info.gameDuration` |
| 4 | game_mode | 경기 | 경기 메타데이터 game_mode | MATCH-V5 | `info.gameMode` |
| 5 | game_type | 경기 | 경기 메타데이터 game_type | MATCH-V5 | `info.gameType` |
| 6 | game_version | 경기 | 경기 메타데이터 game_version | MATCH-V5 | `info.gameVersion` |
| 7 | map_id | 경기 | 경기 메타데이터 map_id | MATCH-V5 | `info.mapId` |
| 8 | platform_id | 경기 | 경기 메타데이터 platform_id | MATCH-V5 | `info.platformId` |
| 9 | queue_id | 경기 | 경기 메타데이터 queue_id | MATCH-V5 | `info.queueId` |
| 10 | participant_id | 참가자 | 참가자 participant_id | MATCH-V5 | `info.participants[].participantId` |
| 11 | puuid | 참가자 | 참가자 puuid | MATCH-V5 | `info.participants[].puuid` |
| 12 | summoner_name | 참가자 | Riot ID 게임 이름, 없으면 소환사 이름 | MATCH-V5 | `info.participants[].riotIdGameName / summonerName` |
| 13 | summoner_id | 참가자 | 참가자 summoner_id | MATCH-V5 | `info.participants[].summonerId` |
| 14 | summoner_level | 참가자 | 참가자 summoner_level | MATCH-V5 | `info.participants[].summonerLevel` |
| 15 | champion_id | 참가자 | 참가자 champion_id | MATCH-V5 | `info.participants[].championId` |
| 16 | champion_name | 참가자 | 참가자 champion_name | MATCH-V5 | `info.participants[].championName` |
| 17 | team_id | 참가자 | 참가자 team_id | MATCH-V5 | `info.participants[].teamId` |
| 18 | win | 참가자 | 참가자 win | MATCH-V5 | `info.participants[].win` |
| 19 | individual_position | 참가자 | 참가자 individual_position | MATCH-V5 | `info.participants[].individualPosition` |
| 20 | team_position | 참가자 | 참가자 team_position | MATCH-V5 | `info.participants[].teamPosition` |
| 21 | lane | 참가자 | 참가자 lane | MATCH-V5 | `info.participants[].lane` |
| 22 | role | 참가자 | 참가자 role | MATCH-V5 | `info.participants[].role` |
| 23 | kills | 참가자 | 참가자 kills | MATCH-V5 | `info.participants[].kills` |
| 24 | deaths | 참가자 | 참가자 deaths | MATCH-V5 | `info.participants[].deaths` |
| 25 | assists | 참가자 | 참가자 assists | MATCH-V5 | `info.participants[].assists` |
| 26 | baron_kills | 참가자 | 참가자 baron_kills | MATCH-V5 | `info.participants[].baronKills` |
| 27 | dragon_kills | 참가자 | 참가자 dragon_kills | MATCH-V5 | `info.participants[].dragonKills` |
| 28 | gold_earned | 참가자 | 참가자 gold_earned | MATCH-V5 | `info.participants[].goldEarned` |
| 29 | gold_spent | 참가자 | 참가자 gold_spent | MATCH-V5 | `info.participants[].goldSpent` |
| 30 | total_damage_dealt | 참가자 | 참가자 total_damage_dealt | MATCH-V5 | `info.participants[].totalDamageDealt` |
| 31 | total_damage_dealt_to_champions | 참가자 | 참가자 total_damage_dealt_to_champions | MATCH-V5 | `info.participants[].totalDamageDealtToChampions` |
| 32 | physical_damage_dealt_to_champions | 참가자 | 참가자 physical_damage_dealt_to_champions | MATCH-V5 | `info.participants[].physicalDamageDealtToChampions` |
| 33 | magic_damage_dealt_to_champions | 참가자 | 참가자 magic_damage_dealt_to_champions | MATCH-V5 | `info.participants[].magicDamageDealtToChampions` |
| 34 | true_damage_dealt_to_champions | 참가자 | 참가자 true_damage_dealt_to_champions | MATCH-V5 | `info.participants[].trueDamageDealtToChampions` |
| 35 | damage_dealt_to_objectives | 참가자 | 참가자 damage_dealt_to_objectives | MATCH-V5 | `info.participants[].damageDealtToObjectives` |
| 36 | damage_dealt_to_turrets | 참가자 | 참가자 damage_dealt_to_turrets | MATCH-V5 | `info.participants[].damageDealtToTurrets` |
| 37 | total_damage_taken | 참가자 | 참가자 total_damage_taken | MATCH-V5 | `info.participants[].totalDamageTaken` |
| 38 | physical_damage_taken | 참가자 | 참가자 physical_damage_taken | MATCH-V5 | `info.participants[].physicalDamageTaken` |
| 39 | magic_damage_taken | 참가자 | 참가자 magic_damage_taken | MATCH-V5 | `info.participants[].magicDamageTaken` |
| 40 | true_damage_taken | 참가자 | 참가자 true_damage_taken | MATCH-V5 | `info.participants[].trueDamageTaken` |
| 41 | time_ccing_others | 참가자 | 참가자 time_ccing_others | MATCH-V5 | `info.participants[].timeCCingOthers` |
| 42 | vision_score | 참가자 | 참가자 vision_score | MATCH-V5 | `info.participants[].visionScore` |
| 43 | wards_placed | 참가자 | 참가자 wards_placed | MATCH-V5 | `info.participants[].wardsPlaced` |
| 44 | wards_killed | 참가자 | 참가자 wards_killed | MATCH-V5 | `info.participants[].wardsKilled` |
| 45 | vision_wards_bought_in_game | 참가자 | 참가자 vision_wards_bought_in_game | MATCH-V5 | `info.participants[].visionWardsBoughtInGame` |
| 46 | item0 | 참가자 | 참가자 item0 | MATCH-V5 | `info.participants[].item0` |
| 47 | item1 | 참가자 | 참가자 item1 | MATCH-V5 | `info.participants[].item1` |
| 48 | item2 | 참가자 | 참가자 item2 | MATCH-V5 | `info.participants[].item2` |
| 49 | item3 | 참가자 | 참가자 item3 | MATCH-V5 | `info.participants[].item3` |
| 50 | item4 | 참가자 | 참가자 item4 | MATCH-V5 | `info.participants[].item4` |
| 51 | item5 | 참가자 | 참가자 item5 | MATCH-V5 | `info.participants[].item5` |
| 52 | item6 | 참가자 | 참가자 item6 | MATCH-V5 | `info.participants[].item6` |
| 53 | solo_tier | 솔로랭크 | 현재 솔로랭크 정보 | LEAGUE-V4 | `tier` |
| 54 | solo_rank | 솔로랭크 | 현재 솔로랭크 정보 | LEAGUE-V4 | `rank` |
| 55 | solo_lp | 솔로랭크 | 현재 솔로랭크 정보 | LEAGUE-V4 | `leaguePoints` |
| 56 | solo_wins | 솔로랭크 | 현재 솔로랭크 정보 | LEAGUE-V4 | `wins` |
| 57 | solo_losses | 솔로랭크 | 현재 솔로랭크 정보 | LEAGUE-V4 | `losses` |
| 58 | flex_tier | 호환 | 스키마 호환용 빈 컬럼 | 미수집 | `` |
| 59 | flex_rank | 호환 | 스키마 호환용 빈 컬럼 | 미수집 | `` |
| 60 | flex_lp | 호환 | 스키마 호환용 빈 컬럼 | 미수집 | `` |
| 61 | flex_wins | 호환 | 스키마 호환용 빈 컬럼 | 미수집 | `` |
| 62 | flex_losses | 호환 | 스키마 호환용 빈 컬럼 | 미수집 | `` |
| 63 | champion_mastery_level | 숙련도 | 챔피언 숙련도 정보 | CHAMPION-MASTERY-V4 | `championLevel` |
| 64 | champion_mastery_points | 숙련도 | 챔피언 숙련도 정보 | CHAMPION-MASTERY-V4 | `championPoints` |
| 65 | champion_mastery_lastPlayTime | 숙련도 | 챔피언 숙련도 정보 | CHAMPION-MASTERY-V4 | `lastPlayTime` |
| 66 | champion_mastery_lastPlayTime_utc | 숙련도 | lastPlayTime의 UTC 변환값 | CHAMPION-MASTERY-V4 | `lastPlayTime` |
| 67 | champion_mastery_pointsSinceLastLevel | 숙련도 | 챔피언 숙련도 정보 | CHAMPION-MASTERY-V4 | `championPointsSinceLastLevel` |
| 68 | champion_mastery_pointsUntilNextLevel | 숙련도 | 챔피언 숙련도 정보 | CHAMPION-MASTERY-V4 | `championPointsUntilNextLevel` |
| 69 | champion_mastery_tokensEarned | 숙련도 | 챔피언 숙련도 정보 | CHAMPION-MASTERY-V4 | `tokensEarned` |
| 70 | final_abilityHaste | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.abilityHaste` |
| 71 | final_abilityPower | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.abilityPower` |
| 72 | final_armor | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.armor` |
| 73 | final_armorPen | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.armorPen` |
| 74 | final_armorPenPercent | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.armorPenPercent` |
| 75 | final_attackDamage | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.attackDamage` |
| 76 | final_attackSpeed | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.attackSpeed` |
| 77 | final_bonusArmorPenPercent | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.bonusArmorPenPercent` |
| 78 | final_bonusMagicPenPercent | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.bonusMagicPenPercent` |
| 79 | final_ccReduction | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.ccReduction` |
| 80 | final_cooldownReduction | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.cooldownReduction` |
| 81 | final_health | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.health` |
| 82 | final_healthMax | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.healthMax` |
| 83 | final_healthRegen | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.healthRegen` |
| 84 | final_lifesteal | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.lifesteal` |
| 85 | final_magicPen | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.magicPen` |
| 86 | final_magicPenPercent | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.magicPenPercent` |
| 87 | final_magicResist | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.magicResist` |
| 88 | final_movementSpeed | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.movementSpeed` |
| 89 | final_omnivamp | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.omnivamp` |
| 90 | final_physicalVamp | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.physicalVamp` |
| 91 | final_power | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.power` |
| 92 | final_powerMax | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.powerMax` |
| 93 | final_powerRegen | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.powerRegen` |
| 94 | final_spellVamp | 최종스탯 | 타임라인 마지막 유효 프레임의 최종 스탯 | MATCH-V5 Timeline | `championStats.spellVamp` |
