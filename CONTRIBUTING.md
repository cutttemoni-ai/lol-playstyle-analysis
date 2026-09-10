# 협업 가이드

`main`에서 직접 개발하지 않고 기능 브랜치와 Pull Request를 사용합니다.

1. 작업 전 `git switch main`과 `git pull --ff-only`로 최신화합니다.
2. `git switch -c feature/riot-api-client`처럼 기능별 브랜치를 만듭니다.
3. 한 가지 목적에 집중해 코드를 작성합니다.
4. `python -m pytest`와 `python -m ruff check .`을 실행합니다.
5. 변경 내용을 확인하고 작은 단위로 commit합니다.
6. `git push -u origin <브랜치>`로 push합니다.
7. GitHub에서 Pull Request를 생성하고 템플릿을 채웁니다.
8. 다른 팀원의 검토와 CI 통과 후 `main`에 병합합니다.

브랜치 예시는 `feature/riot-api-client`, `feature/excel-export`, `feature/playstyle-analysis`, `fix/rate-limit`, `docs/readme`입니다.

커밋 메시지는 다음처럼 변경 종류와 목적을 명확히 씁니다.

```text
feat: Riot API 경기 수집 기능 추가
feat: 94개 컬럼 엑셀 생성 기능 추가
fix: 429 응답 재시도 처리
test: Match 데이터 파서 테스트 추가
docs: 팀원 실행 방법 작성
```

commit 전에 반드시 `git status`, `git diff --staged`, `git ls-files`를 확인합니다. `.env`, `RGAPI-`로 시작하는 키, XLSX, 원본 JSON, 로그와 실제 사용자 데이터가 포함되면 commit하거나 push하지 않습니다.
