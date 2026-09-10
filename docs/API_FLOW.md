# Riot API 호출 흐름

모든 요청은 API Key를 URL이 아닌 `X-Riot-Token` 헤더로 보냅니다. 한국 플랫폼 API는 `kr.api.riotgames.com`, 아시아 지역 API는 `asia.api.riotgames.com`을 사용합니다.

1. ACCOUNT‑V1 `accounts/by-riot-id/{gameName}/{tagLine}`로 PUUID를 얻습니다.
2. SUMMONER‑V4 `summoners/by-puuid/{puuid}`가 성공하는지 확인해 KR 계정을 검증합니다.
3. MATCH‑V5 `matches/by-puuid/{puuid}/ids?queue=420&start=0&count=20`으로 Match ID를 얻습니다.
4. `KR_` Match ID마다 경기 상세와 Timeline을 한 번씩 수집합니다.
5. 참가자 PUUID마다 LEAGUE‑V4 `entries/by-puuid/{puuid}`를 한 번 호출하고 `RANKED_SOLO_5x5`만 선택합니다.
6. 참가자 PUUID와 championId 조합마다 CHAMPION‑MASTERY‑V4를 한 번 호출합니다.
7. 파서가 참가자별 행을 만들고 Timeline의 마지막 유효 프레임에서 `championStats`를 가져옵니다.
8. 검증된 94개 컬럼을 네 개 시트의 XLSX로 저장합니다.

랭크, 숙련도, 경기 상세, Timeline 결과는 실행 중 메모리 캐시에 저장됩니다. 부분 호출 실패는 `수집오류` 시트에 남기고 가능한 데이터의 수집을 계속합니다. 단, 최초 Riot ID 조회나 KR 계정 확인 실패는 대상 자체를 확정할 수 없어 실행을 중단합니다.
