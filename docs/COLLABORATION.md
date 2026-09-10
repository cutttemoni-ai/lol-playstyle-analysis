# GitHub 협업 요약

저장소를 clone한 뒤 각자 `.env.example`을 `.env`로 복사하고 개인 Riot API Key를 입력합니다. `.env`와 수집 결과는 공유하지 않습니다. 팀에서 필요한 샘플은 개인정보와 식별자를 제거한 최소 fixture로 작성합니다.

작업은 Issue로 범위를 합의하고 기능 브랜치에서 진행합니다. Pull Request에는 변경 목적, 테스트 결과, 보안 확인 내용을 적습니다. CI는 실제 API를 호출하지 않으므로 API Key를 GitHub Actions Secret에 등록할 필요가 없습니다.

저장소 관리자는 `main` branch protection에서 Pull Request와 CI 통과를 필수로 설정하고, 팀원을 GitHub의 **Settings → Collaborators and teams**에서 초대하는 것을 권장합니다.
