from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from pydantic import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from riot_api import (  # noqa: E402
    RiotAPIClient,
    RiotAPIError,
    RiotMatchCollector,
    build_league_rows,
    export_workbook,
    load_settings,
)


def count_type(value: str) -> int:
    number = int(value)
    if not 1 <= number <= 20:
        raise argparse.ArgumentTypeError("--count는 1에서 20 사이여야 합니다.")
    return number


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="한국 서버 최근 솔로랭크 참가자 데이터를 XLSX로 저장합니다."
    )
    parser.add_argument("--game-name", required=True, help="Riot ID 게임 이름")
    parser.add_argument("--tag-line", required=True, help="Riot ID 태그")
    parser.add_argument("--count", type=count_type, default=20, help="경기 수(기본 20, 최대 20)")
    parser.add_argument(
        "--timeline",
        action="store_true",
        help="호환 옵션(94개 컬럼을 위해 타임라인은 항상 수집됩니다)",
    )
    parser.add_argument("--output", help="출력 XLSX 경로")
    parser.add_argument("--save-raw", action="store_true", help="API 원본 JSON 저장")
    return parser.parse_args(argv)


def safe_name(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z가-힣._-]+", "_", value).strip("_") or "riot_user"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        settings = load_settings(PROJECT_ROOT)
    except ValidationError:
        print(
            "RIOT_API_KEY가 없습니다. 프로젝트 루트의 .env에 "
            "RIOT_API_KEY=발급받은키 형식으로 입력하세요.",
            file=sys.stderr,
        )
        return 2

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = (
        Path(args.output)
        if args.output
        else PROJECT_ROOT
        / "data"
        / (
            f"riot_{safe_name(args.game_name)}_{safe_name(args.tag_line)}_"
            f"최근{args.count}경기_{timestamp}.xlsx"
        )
    )
    try:
        with RiotAPIClient(
            settings.riot_api_key,
            timeout=settings.timeout,
            request_interval=settings.request_interval,
            max_retries=settings.max_retries,
        ) as client:
            result = RiotMatchCollector(client).collect(args.game_name, args.tag_line, args.count)
        rows = build_league_rows(result.matches, result.timelines, result.ranks, result.masteries)
        search_info = {
            "입력한 Riot ID": (
                f"{result.account.get('gameName', args.game_name)}#"
                f"{result.account.get('tagLine', args.tag_line)}"
            ),
            "PUUID": result.account.get("puuid"),
            "한국 서버 확인 결과": "확인",
            "요청 경기 수": args.count,
            "실제 수집 경기 수": len(result.matches),
            "생성된 데이터 행 수": len(rows),
            "수집 시작 시각": (
                result.started_at.replace(tzinfo=None) if result.started_at else None
            ),
            "수집 완료 시각": (
                result.completed_at.replace(tzinfo=None) if result.completed_at else None
            ),
            "Queue ID": 420,
            "Platform Routing": "KR",
            "Regional Routing": "ASIA",
        }
        saved = export_workbook(output, rows, search_info, result.errors)
        if args.save_raw:
            save_raw_result(result, PROJECT_ROOT / "data" / f"raw_{timestamp}")
        print(f"XLSX 생성 완료: {saved.resolve()}")
        print(
            f"경기 {len(result.matches)}개, 데이터 {len(rows)}행, API 실패 {len(result.errors)}건"
        )
        return 0
    except (RiotAPIError, ValueError, OSError) as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1


def save_raw_result(result: object, raw_dir: Path) -> None:
    raw_dir.mkdir(parents=True, exist_ok=False)
    account = result.account
    summoner = result.summoner
    matches = result.matches
    timelines = result.timelines
    (raw_dir / "account.json").write_text(
        json.dumps(account, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (raw_dir / "summoner.json").write_text(
        json.dumps(summoner, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for match in matches:
        match_id = match.get("metadata", {}).get("matchId", "unknown")
        filename = safe_name(str(match_id))
        (raw_dir / f"{filename}.json").write_text(
            json.dumps(match, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        if match_id in timelines:
            (raw_dir / f"{filename}_timeline.json").write_text(
                json.dumps(timelines[match_id], ensure_ascii=False, indent=2), encoding="utf-8"
            )


if __name__ == "__main__":
    raise SystemExit(main())
