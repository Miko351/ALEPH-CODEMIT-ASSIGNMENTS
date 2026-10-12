# Minsu의 Git 협업 실습

- 역할: 민수
- 작업 브랜치: feature/minsu
- 변경 파일: minsu.md
- 작업: 로컬 작성 → 커밋 → 브랜치 전환 및 로컬 merge → push → PR 검토와 병합

## PR 생성 후 보완

main에서 git merge feature/minsu를 실행하면 현재 체크아웃한 main이 변경을 받습니다. 로컬 merge와 GitHub PR 병합은 서로 다른 위치에서 수행되므로, 원격 병합 후 각 clone에서 pull해야 합니다.
