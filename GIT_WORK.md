# Git 작업 기록 — 두 clone과 실제 GitHub PR
작성·확인 날짜: 2026-10-12 (한국 시간). 모든 소스·문서는 먼저 로컬에서 작성·검증·커밋하고 push했습니다. GitHub 웹에서 소스 파일을 직접 작성하지 않았습니다. PR 생성·본문 검토 기록·병합은 GitHub CLI로 실행했습니다.
저장소: https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
기본 브랜치 default는 파일 없는 초기 커밋을 유지합니다. main은 민수·지윤·점검표 Git 실습의 병합 기준입니다. 이전 세 과제와 이번 앱 소스는 각각 별도 브랜치에 보관합니다.
## 실제 clone 폴더와 초기 준비
브랜치 구조 준비 단계에서 다음 명령으로 두 폴더를 clone했습니다. 작업 브랜치는 각 clone의 main에서 생성했습니다. 아래는 그때의 실제 clone 출력이며, 뒤의 remote·reflog 출력에서도 같은 원격과 main 시작점을 확인할 수 있습니다.
```text
git clone --branch main https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu
Cloning into 'D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu'...
git switch -c feature/minsu
Switched to a new branch 'feature/minsu'

git clone --branch main https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun
Cloning into 'D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun'...
git switch -c feature/jiyun
Switched to a new branch 'feature/jiyun'
```
## PR별 작업과 검토·병합 결과
| 작업 | 원본 PR | Base | 작업 브랜치 | 상태 | 변경 파일 |
| --- | --- | --- | --- | --- | --- |
| 필수 1 · 민수 역할 문서와 보완 커밋 | [PR #1](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1) | `main` | `feature/minsu` | **MERGED** | `minsu.md` |
| 필수 2 · 지윤 역할 문서 | [PR #2](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2) | `main` | `feature/jiyun` | **MERGED** | `jiyun.md` |
| 필수 3 · 최신 main의 점검표 | [PR #3](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3) | `main` | `feature/checklist` | **MERGED** | `checklist.md` |
| 심화 · 같은 첫 줄의 민수 제목 변경 | [PR #4](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4) | `main` | `feature/minsu-title` | **MERGED** | `checklist.md` |
| 심화 · 지윤 제목 충돌 해결 | [PR #5](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5) | `main` | `feature/jiyun-title` | **MERGED** | `checklist.md` |

### 필수 1 · 민수 역할 문서와 보완 커밋

원본: https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1

작업 커밋:

- `9d5f4207b82e0a22cc12e30a3999eb532174d816` — Add Minsu collaboration practice record
- `6bad01aa16e08bcb19fe537e6fe627b383e8acf2` — Clarify local merge direction and remote pull after opening PR

병합 커밋: `45a550d8e3b6670a60950bc2b7ab79b598ec3ec6`. GitHub API에서 부모 커밋 2개를 확인하여 merge commit 방식임을 검증했습니다. 병합 시각(원본 UTC): 2026-10-12T07:52:53Z.

PR 본문에 남긴 실제 변경·검토 설명:

Minsu 역할의 Git 협업 실습 문서를 추가합니다. 작업 브랜치에서 커밋하고 로컬 main으로 이동하여 merge 방향과 파일 차이를 확인했습니다.

변경 파일: `minsu.md`. Base: `main`, head: `feature/minsu`.

PR 생성 후 같은 작업 브랜치에 보완 커밋을 추가했습니다. 문서에 로컬 merge와 원격 PR 병합의 차이를 설명했습니다.

직접 Files changed의 실제 diff와 커밋 목록을 읽었습니다. 역할 문서 외 다른 프로젝트 파일이 변경되지 않았고, 내용과 main으로의 병합 방향을 확인했습니다. 단독 실습이므로 자신의 PR에 Approve를 제출하지 않습니다.


### 필수 2 · 지윤 역할 문서

원본: https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2

작업 커밋:

- `ad583805ad91058a76b9a9a91a7292640ca1b17a` — Add Jiyun collaboration practice record

병합 커밋: `dbec7990103817b39bbe9c5a495bc38473dfc978`. GitHub API에서 부모 커밋 2개를 확인하여 merge commit 방식임을 검증했습니다. 병합 시각(원본 UTC): 2026-10-12T07:52:57Z.

PR 본문에 남긴 실제 변경·검토 설명:

Jiyun 역할의 Git 협업 실습 문서를 추가합니다. 작업 브랜치에서 커밋하고 로컬 main으로 이동하여 merge 방향과 파일 차이를 확인했습니다.

변경 파일: `jiyun.md`. Base: `main`, head: `feature/jiyun`.

직접 Files changed의 실제 diff와 커밋 목록을 읽었습니다. 역할 문서 외 다른 프로젝트 파일이 변경되지 않았고, 내용과 main으로의 병합 방향을 확인했습니다. 단독 실습이므로 자신의 PR에 Approve를 제출하지 않습니다.


### 필수 3 · 최신 main의 점검표

원본: https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3

작업 커밋:

- `4ec2e640188faff1cf5d91cd47dc64f76781f4e2` — Add verified Git collaboration checklist after both initial PRs

병합 커밋: `615de754dcfb3d85b0b83ba8dc08b450354df575`. GitHub API에서 부모 커밋 2개를 확인하여 merge commit 방식임을 검증했습니다. 병합 시각(원본 UTC): 2026-10-12T07:55:50Z.

PR 본문에 남긴 실제 변경·검토 설명:

두 초기 PR을 merge commit으로 병합한 뒤 두 clone의 main에서 pull한 결과를 점검표로 기록합니다.

변경 파일: `checklist.md`. 최신 main에서 새 브랜치를 만들었습니다. 로컬 diff를 직접 확인했고 체크한 항목은 실제 Git 명령 출력으로 확인한 작업입니다.


### 심화 · 같은 첫 줄의 민수 제목 변경

원본: https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4

작업 커밋:

- `788bafc418e34d652fc68d9754d7c3d11ab5a9f8` — Change shared checklist title from Minsu perspective

병합 커밋: `3b014b590b12038414c81a408d9ead75c7c22fc8`. GitHub API에서 부모 커밋 2개를 확인하여 merge commit 방식임을 검증했습니다. 병합 시각(원본 UTC): 2026-10-12T08:04:37Z.

PR 본문에 남긴 실제 변경·검토 설명:

같은 줄 충돌 해결 실습을 위해 checklist.md의 첫 제목을 # Git 협업 확인 — 민수의 관점로 변경합니다. 로컬 diff를 직접 읽어 첫 줄만 바뀌었음을 확인했습니다.


### 심화 · 지윤 제목 충돌 해결

원본: https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5

작업 커밋:

- `7bd9366ca06721dbd135db50d6e9e3ce001e887d` — Change shared checklist title from Jiyun perspective
- `93ad058e775b89c5d379e8fe08f934727f4838cc` — Resolve same-line checklist title conflict by retaining both perspect…

병합 커밋: `3efd941bcd014b66d4714ee880330a9651aac10b`. GitHub API에서 부모 커밋 2개를 확인하여 merge commit 방식임을 검증했습니다. 병합 시각(원본 UTC): 2026-10-12T08:04:47Z.

PR 본문에 남긴 실제 변경·검토 설명:

checklist.md 첫 줄에서 실제 merge 충돌을 해결했습니다.

민수 변경: Git 협업 확인 — 민수의 관점
지윤 변경: Git 협업 확인 — 지윤의 관점
최종 내용: Git 협업 확인 — 민수와 지윤의 공동 점검

양쪽의 역할을 제목에 함께 남기는 내용을 선택했습니다. 최신 main을 작업 브랜치로 merge하고 로컬에서 충돌 표식을 제거·커밋·push했습니다. 같은 PR의 Files changed를 다시 읽어 제목과 나머지 점검 항목 보존을 확인했습니다.


## 전환 위치·로컬 merge 방향·양쪽 pull

민수는 git-practice-minsu, 지윤은 git-practice-jiyun 폴더에서 main과 자기 작업 브랜치를 오갔습니다. 역할 파일을 커밋한 작업 브랜치에는 파일이 있고, 병합 전 main에는 없음을 git ls-files로 확인했습니다. 각 main에서 `git merge feature/minsu` 또는 `git merge feature/jiyun`을 실행해 **main이 변경을 받는 방향**을 확인했습니다. 이 로컬 merge는 fast-forward였으며 main을 직접 push하지 않았습니다. GitHub의 PR은 별도로 Create a merge commit 방식으로 병합했습니다.

두 초기 PR이 병합된 뒤 양쪽 폴더의 main에서 `git pull --ff-only origin main`을 실행하여 minsu.md와 jiyun.md를 모두 받았습니다. 최신 지윤 main에서 feature/checklist를 새로 만들고 점검표를 추가했습니다. 세 번째 PR 병합 후 두 main에서 다시 pull하여 checklist.md도 받았습니다. 이후 각자의 완료 브랜치를 로컬에서 삭제하고 원격 작업 브랜치도 정리했습니다. 실제 명령과 출력은 아래 부록에 순서대로 기록했습니다.

## 심화: 같은 줄 충돌

충돌 파일은 checklist.md의 첫 줄입니다. 민수는 “Git 협업 확인 — 민수의 관점”, 지윤은 “Git 협업 확인 — 지윤의 관점”으로 바꿨습니다. 민수 제목 PR을 먼저 병합하고 지윤 작업 브랜치에서 origin/main을 merge했을 때 실제 content conflict와 표식이 발생했습니다.

최종 제목은 “Git 협업 확인 — 민수와 지윤의 공동 점검”입니다. 한쪽 역할을 버리지 않고 두 관점을 함께 남기는 제목을 선택했습니다. 지윤 로컬에서 표식을 제거하고 resolve 커밋을 같은 작업 브랜치로 push하여 **기존 PR #5**에 반영했습니다. 다시 diff를 읽고 병합한 뒤 양쪽 main을 pull하여 최종 제목이 동일함을 확인했습니다.

## 심화: 앱 작업 브랜치

앱의 안정 기준 브랜치는 next-practice입니다. 앱 개선 PR의 실제 기록은 완료 후 이 절에 추가합니다.

## 두 질문에 대한 답

**main에서 git merge feature/minsu를 실행하면 어느 브랜치가 변경을 받는가?**

현재 선택한 main이 feature/minsu의 변경을 받습니다. 원본 작업 브랜치 feature/minsu 자체를 바꾸는 명령이 아닙니다.

**GitHub에서 PR을 병합한 뒤에도 각 폴더에서 pull해야 하는 이유는 무엇인가?**

PR 병합은 원격 main을 변경하며 로컬 clone은 자동으로 갱신되지 않습니다. 각 폴더에서 main을 선택하고 pull해야 다른 사람의 변경과 원격 병합 결과를 받습니다.

## 실제 명령과 출력 — 실행 순서 부록

아래 출력은 실행 도중 수집한 stdout·stderr입니다. 의도한 충돌 명령의 종료 코드 1도 그대로 남겼습니다. PR 본문 파일 경로는 로컬에서 작성한 문서를 CLI로 전송한 경로이며 해당 본문은 위 원본 PR에서 확인할 수 있습니다.

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git status --porcelain
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git remote -v
origin	https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git (fetch)
origin	https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git (push)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git reflog show "--format=%h %gs" feature/minsu
b7ae56a branch: Created from HEAD
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git pull --ff-only origin main
Already up to date.
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch feature/minsu
Your branch is up to date with 'origin/feature/minsu'.
Switched to branch 'feature/minsu'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git add minsu.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git commit -m "Add Minsu collaboration practice record"
[feature/minsu 9d5f420] Add Minsu collaboration practice record
 1 file changed, 6 insertions(+)
 create mode 100644 minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git show --stat --oneline HEAD
9d5f420 Add Minsu collaboration practice record
 minsu.md | 6 ++++++
 1 file changed, 6 insertions(+)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git ls-files minsu.md
minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git ls-files minsu.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git merge feature/minsu
Updating b7ae56a..9d5f420
Fast-forward
 minsu.md | 6 ++++++
 1 file changed, 6 insertions(+)
 create mode 100644 minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git ls-files minsu.md
minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch feature/minsu
Your branch is ahead of 'origin/feature/minsu' by 1 commit.
  (use "git push" to publish your local commits)
Switched to branch 'feature/minsu'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git push -u origin feature/minsu
branch 'feature/minsu' set up to track 'origin/feature/minsu'.
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
   b7ae56a..9d5f420  feature/minsu -> feature/minsu
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr create --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --base main --head feature/minsu --title "Add Minsu Git collaboration practice document" --body-file D:\ALEPH_Codemit\nextjs-notes\.cache\minsu-pr-body.md
https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git status --porcelain
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git remote -v
origin	https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git (fetch)
origin	https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git (push)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git reflog show "--format=%h %gs" feature/jiyun
b7ae56a branch: Created from HEAD
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git pull --ff-only origin main
Already up to date.
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch feature/jiyun
Your branch is up to date with 'origin/feature/jiyun'.
Switched to branch 'feature/jiyun'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git add jiyun.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git commit -m "Add Jiyun collaboration practice record"
[feature/jiyun ad58380] Add Jiyun collaboration practice record
 1 file changed, 6 insertions(+)
 create mode 100644 jiyun.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git show --stat --oneline HEAD
ad58380 Add Jiyun collaboration practice record
 jiyun.md | 6 ++++++
 1 file changed, 6 insertions(+)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git ls-files jiyun.md
jiyun.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git ls-files jiyun.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git merge feature/jiyun
Updating b7ae56a..ad58380
Fast-forward
 jiyun.md | 6 ++++++
 1 file changed, 6 insertions(+)
 create mode 100644 jiyun.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git ls-files jiyun.md
jiyun.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch feature/jiyun
Your branch is ahead of 'origin/feature/jiyun' by 1 commit.
  (use "git push" to publish your local commits)
Switched to branch 'feature/jiyun'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git push -u origin feature/jiyun
branch 'feature/jiyun' set up to track 'origin/feature/jiyun'.
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
   b7ae56a..ad58380  feature/jiyun -> feature/jiyun
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr create --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --base main --head feature/jiyun --title "Add Jiyun Git collaboration practice document" --body-file D:\ALEPH_Codemit\nextjs-notes\.cache\jiyun-pr-body.md
https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git add minsu.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git commit -m "Clarify local merge direction and remote pull after opening PR"
[feature/minsu 6bad01a] Clarify local merge direction and remote pull after opening PR
 1 file changed, 4 insertions(+)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git push origin feature/minsu
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
   9d5f420..6bad01a  feature/minsu -> feature/minsu
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr diff https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS
diff --git a/minsu.md b/minsu.md
new file mode 100644
index 0000000..1c36de4
--- /dev/null
+++ b/minsu.md
@@ -0,0 +1,6 @@
+# Minsu의 Git 협업 실습
+
+- 역할: 민수
+- 작업 브랜치: feature/minsu
+- 변경 파일: minsu.md
+- 작업: 로컬 작성 → 커밋 → 브랜치 전환 및 로컬 merge → push → PR 검토와 병합
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,baseRefName,headRefName,state,commits,files
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T07:44:43Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:43Z","messageBody":"","messageHeadline":"Add Minsu collaboration practice record","oid":"9d5f4207b82e0a22cc12e30a3999eb532174d816"},{"authoredDate":"2026-10-12T07:44:55Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:55Z","messageBody":"","messageHeadline":"Clarify local merge direction and remote pull after opening PR","oid":"6bad01aa16e08bcb19fe537e6fe627b383e8acf2"}],"files":[{"path":"minsu.md","additions":10,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/minsu","state":"OPEN","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr edit https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --body-file D:\ALEPH_Codemit\nextjs-notes\.cache\minsu-pr-body.md
https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr diff https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS
diff --git a/jiyun.md b/jiyun.md
new file mode 100644
index 0000000..2014364
--- /dev/null
+++ b/jiyun.md
@@ -0,0 +1,6 @@
+# Jiyun의 Git 협업 실습
+
+- 역할: 지윤
+- 작업 브랜치: feature/jiyun
+- 변경 파일: jiyun.md
+- 작업: 로컬 작성 → 커밋 → 브랜치 전환 및 로컬 merge → push → PR 검토와 병합
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,baseRefName,headRefName,state,commits,files
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T07:44:50Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:50Z","messageBody":"","messageHeadline":"Add Jiyun collaboration practice record","oid":"ad583805ad91058a76b9a9a91a7292640ca1b17a"}],"files":[{"path":"jiyun.md","additions":6,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/jiyun","state":"OPEN","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr edit https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --body-file D:\ALEPH_Codemit\nextjs-notes\.cache\jiyun-pr-body.md
https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,mergeable,baseRefName,headRefName,commits,files
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T07:44:43Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:43Z","messageBody":"","messageHeadline":"Add Minsu collaboration practice record","oid":"9d5f4207b82e0a22cc12e30a3999eb532174d816"},{"authoredDate":"2026-10-12T07:44:55Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:55Z","messageBody":"","messageHeadline":"Clarify local merge direction and remote pull after opening PR","oid":"6bad01aa16e08bcb19fe537e6fe627b383e8acf2"}],"files":[{"path":"minsu.md","additions":10,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/minsu","mergeable":"MERGEABLE","state":"OPEN","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr merge https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --merge
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,mergedAt,mergeCommit,baseRefName,headRefName,commits,files
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T07:44:43Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:43Z","messageBody":"","messageHeadline":"Add Minsu collaboration practice record","oid":"9d5f4207b82e0a22cc12e30a3999eb532174d816"},{"authoredDate":"2026-10-12T07:44:55Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:55Z","messageBody":"","messageHeadline":"Clarify local merge direction and remote pull after opening PR","oid":"6bad01aa16e08bcb19fe537e6fe627b383e8acf2"}],"files":[{"path":"minsu.md","additions":10,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/minsu","mergeCommit":{"oid":"45a550d8e3b6670a60950bc2b7ab79b598ec3ec6"},"mergedAt":"2026-10-12T07:52:53Z","state":"MERGED","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,mergeable,baseRefName,headRefName,commits,files
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T07:44:50Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:50Z","messageBody":"","messageHeadline":"Add Jiyun collaboration practice record","oid":"ad583805ad91058a76b9a9a91a7292640ca1b17a"}],"files":[{"path":"jiyun.md","additions":6,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/jiyun","mergeable":"UNKNOWN","state":"OPEN","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr merge https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --merge
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,mergedAt,mergeCommit,baseRefName,headRefName,commits,files
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T07:44:50Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:50Z","messageBody":"","messageHeadline":"Add Jiyun collaboration practice record","oid":"ad583805ad91058a76b9a9a91a7292640ca1b17a"}],"files":[{"path":"jiyun.md","additions":6,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/jiyun","mergeCommit":{"oid":"dbec7990103817b39bbe9c5a495bc38473dfc978"},"mergedAt":"2026-10-12T07:52:57Z","state":"MERGED","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git pull --ff-only origin main
Updating 9d5f420..dbec799
Fast-forward
 jiyun.md | 6 ++++++
 minsu.md | 4 ++++
 2 files changed, 10 insertions(+)
 create mode 100644 jiyun.md
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
   b7ae56a..dbec799  main       -> origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git ls-files
jiyun.md
minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git log --oneline --graph -7
*   dbec799 Merge pull request #2 from Miko351/feature/jiyun
|\  
| * ad58380 Add Jiyun collaboration practice record
* |   45a550d Merge pull request #1 from Miko351/feature/minsu
|\ \  
| |/  
|/|   
| * 6bad01a Clarify local merge direction and remote pull after opening PR
| * 9d5f420 Add Minsu collaboration practice record
|/  
* b7ae56a Initialize empty assignment branch base
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git pull --ff-only origin main
Updating ad58380..dbec799
Fast-forward
 minsu.md | 10 ++++++++++
 1 file changed, 10 insertions(+)
 create mode 100644 minsu.md
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
   b7ae56a..dbec799  main       -> origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git ls-files
jiyun.md
minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git log --oneline --graph -7
*   dbec799 Merge pull request #2 from Miko351/feature/jiyun
|\  
| * ad58380 Add Jiyun collaboration practice record
* |   45a550d Merge pull request #1 from Miko351/feature/minsu
|\ \  
| |/  
|/|   
| * 6bad01a Clarify local merge direction and remote pull after opening PR
| * 9d5f420 Add Minsu collaboration practice record
|/  
* b7ae56a Initialize empty assignment branch base
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch -c feature/checklist main
Switched to a new branch 'feature/checklist'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git add checklist.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git commit -m "Add verified Git collaboration checklist after both initial PRs"
[feature/checklist 4ec2e64] Add verified Git collaboration checklist after both initial PRs
 1 file changed, 11 insertions(+)
 create mode 100644 checklist.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git push -u origin feature/checklist
branch 'feature/checklist' set up to track 'origin/feature/checklist'.
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
   b7ae56a..4ec2e64  feature/checklist -> feature/checklist
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr create --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --base main --head feature/checklist --title "Add verified collaboration checklist from latest main" --body-file D:\ALEPH_Codemit\nextjs-notes\.cache\checklist-pr-body.md
https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr diff https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS
diff --git a/checklist.md b/checklist.md
new file mode 100644
index 0000000..01a7f18
--- /dev/null
+++ b/checklist.md
@@ -0,0 +1,11 @@
+# Git 협업 실습 점검표
+
+- [x] 민수·지윤 폴더가 같은 origin 저장소를 사용한다.
+- [x] 각 main에서 작업 브랜치를 선택하여 서로 다른 역할 문서를 커밋했다.
+- [x] 브랜치 전환 전후 파일 차이와 main으로의 로컬 merge를 확인했다.
+- [x] main을 base로 PR 두 개를 생성하고 Files changed를 직접 읽었다.
+- [x] 민수 PR 생성 후 같은 브랜치에 보완 커밋을 반영했다.
+- [x] GitHub에서 두 PR을 Create a merge commit 방식으로 병합했다.
+- [x] 양쪽 main에서 pull하여 minsu.md와 jiyun.md를 모두 받았다.
+
+이 점검표는 두 초기 PR을 병합하고 양쪽 pull을 완료한 뒤 최신 main에서 새 작업으로 작성했습니다.
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,baseRefName,headRefName,state,commits,files
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T07:53:17Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:53:17Z","messageBody":"","messageHeadline":"Add verified Git collaboration checklist after both initial PRs","oid":"4ec2e640188faff1cf5d91cd47dc64f76781f4e2"}],"files":[{"path":"checklist.md","additions":11,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/checklist","state":"OPEN","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr merge https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --merge
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,mergedAt,mergeCommit,baseRefName,headRefName,commits,files
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T07:53:17Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:53:17Z","messageBody":"","messageHeadline":"Add verified Git collaboration checklist after both initial PRs","oid":"4ec2e640188faff1cf5d91cd47dc64f76781f4e2"}],"files":[{"path":"checklist.md","additions":11,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/checklist","mergeCommit":{"oid":"615de754dcfb3d85b0b83ba8dc08b450354df575"},"mergedAt":"2026-10-12T07:55:50Z","state":"MERGED","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Already on 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git pull --ff-only origin main
Updating dbec799..615de75
Fast-forward
 checklist.md | 11 +++++++++++
 1 file changed, 11 insertions(+)
 create mode 100644 checklist.md
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
   dbec799..615de75  main       -> origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git ls-files
checklist.md
jiyun.md
minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git branch -d feature/minsu
Deleted branch feature/minsu (was 6bad01a).
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git branch -vv
* main 615de75 [origin/main] Merge pull request #3 from Miko351/feature/checklist
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git pull --ff-only origin main
Updating dbec799..615de75
Fast-forward
 checklist.md | 11 +++++++++++
 1 file changed, 11 insertions(+)
 create mode 100644 checklist.md
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
   dbec799..615de75  main       -> origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git ls-files
checklist.md
jiyun.md
minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git branch -d feature/jiyun
Deleted branch feature/jiyun (was ad58380).
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git branch -d feature/checklist
Deleted branch feature/checklist (was 4ec2e64).
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git branch -vv
* main 615de75 [origin/main] Merge pull request #3 from Miko351/feature/checklist
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git push origin --delete feature/minsu
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
 - [deleted]         feature/minsu
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git push origin --delete feature/jiyun
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
 - [deleted]         feature/jiyun
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git push origin --delete feature/checklist
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
 - [deleted]         feature/checklist
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git fetch --prune origin
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 - [deleted]         (none)     -> origin/feature/checklist
 - [deleted]         (none)     -> origin/feature/jiyun
 - [deleted]         (none)     -> origin/feature/minsu
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git status --short --branch
## main...origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git fetch --prune origin
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git status --short --branch
## main...origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Already on 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git pull --ff-only origin main
Already up to date.
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch -c feature/minsu-title main
Switched to a new branch 'feature/minsu-title'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git add checklist.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git commit -m "Change shared checklist title from Minsu perspective"
[feature/minsu-title 788bafc] Change shared checklist title from Minsu perspective
 1 file changed, 1 insertion(+), 1 deletion(-)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git push -u origin feature/minsu-title
branch 'feature/minsu-title' set up to track 'origin/feature/minsu-title'.
remote: 
remote: Create a pull request for 'feature/minsu-title' on GitHub by visiting:        
remote:      https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/new/feature/minsu-title        
remote: 
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
 * [new branch]      feature/minsu-title -> feature/minsu-title
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr create --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --base main --head feature/minsu-title --title "Update shared checklist title from Minsu perspective" --body-file D:\ALEPH_Codemit\nextjs-notes\.cache\minsu-title-body.md
https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr diff https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS
diff --git a/checklist.md b/checklist.md
index 01a7f18..67e9d60 100644
--- a/checklist.md
+++ b/checklist.md
@@ -1,4 +1,4 @@
-# Git 협업 실습 점검표
+# Git 협업 확인 — 민수의 관점
 
 - [x] 민수·지윤 폴더가 같은 origin 저장소를 사용한다.
 - [x] 각 main에서 작업 브랜치를 선택하여 서로 다른 역할 문서를 커밋했다.
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,baseRefName,headRefName,files,commits
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T08:00:38Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T08:00:38Z","messageBody":"","messageHeadline":"Change shared checklist title from Minsu perspective","oid":"788bafc418e34d652fc68d9754d7c3d11ab5a9f8"}],"files":[{"path":"checklist.md","additions":1,"deletions":1,"changeType":"MODIFIED"}],"headRefName":"feature/minsu-title","state":"OPEN","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Already on 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git pull --ff-only origin main
Already up to date.
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch -c feature/jiyun-title main
Switched to a new branch 'feature/jiyun-title'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git add checklist.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git commit -m "Change shared checklist title from Jiyun perspective"
[feature/jiyun-title 7bd9366] Change shared checklist title from Jiyun perspective
 1 file changed, 1 insertion(+), 1 deletion(-)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git push -u origin feature/jiyun-title
branch 'feature/jiyun-title' set up to track 'origin/feature/jiyun-title'.
remote: 
remote: Create a pull request for 'feature/jiyun-title' on GitHub by visiting:        
remote:      https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/new/feature/jiyun-title        
remote: 
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
 * [new branch]      feature/jiyun-title -> feature/jiyun-title
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr create --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --base main --head feature/jiyun-title --title "Update shared checklist title from Jiyun perspective" --body-file D:\ALEPH_Codemit\nextjs-notes\.cache\jiyun-title-body.md
https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr diff https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS
diff --git a/checklist.md b/checklist.md
index 01a7f18..678f77e 100644
--- a/checklist.md
+++ b/checklist.md
@@ -1,4 +1,4 @@
-# Git 협업 실습 점검표
+# Git 협업 확인 — 지윤의 관점
 
 - [x] 민수·지윤 폴더가 같은 origin 저장소를 사용한다.
 - [x] 각 main에서 작업 브랜치를 선택하여 서로 다른 역할 문서를 커밋했다.
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,baseRefName,headRefName,files,commits
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T08:00:46Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T08:00:46Z","messageBody":"","messageHeadline":"Change shared checklist title from Jiyun perspective","oid":"7bd9366ca06721dbd135db50d6e9e3ce001e887d"}],"files":[{"path":"checklist.md","additions":1,"deletions":1,"changeType":"MODIFIED"}],"headRefName":"feature/jiyun-title","state":"OPEN","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr merge https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --merge
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,mergedAt,mergeCommit,baseRefName,headRefName,files,commits
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T08:00:38Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T08:00:38Z","messageBody":"","messageHeadline":"Change shared checklist title from Minsu perspective","oid":"788bafc418e34d652fc68d9754d7c3d11ab5a9f8"}],"files":[{"path":"checklist.md","additions":1,"deletions":1,"changeType":"MODIFIED"}],"headRefName":"feature/minsu-title","mergeCommit":{"oid":"3b014b590b12038414c81a408d9ead75c7c22fc8"},"mergedAt":"2026-10-12T08:04:37Z","state":"MERGED","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git fetch origin main
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
   615de75..3b014b5  main       -> origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git merge origin/main
Auto-merging checklist.md
CONFLICT (content): Merge conflict in checklist.md
Automatic merge failed; fix conflicts and then commit the result.
[exit 1]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git status --short
UU checklist.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> Python Path.read_text("checklist.md") — 충돌한 실제 파일 내용
<<<<<<< HEAD
# Git 협업 확인 — 지윤의 관점
=======
# Git 협업 확인 — 민수의 관점
>>>>>>> origin/main

- [x] 민수·지윤 폴더가 같은 origin 저장소를 사용한다.
- [x] 각 main에서 작업 브랜치를 선택하여 서로 다른 역할 문서를 커밋했다.
- [x] 브랜치 전환 전후 파일 차이와 main으로의 로컬 merge를 확인했다.
- [x] main을 base로 PR 두 개를 생성하고 Files changed를 직접 읽었다.
- [x] 민수 PR 생성 후 같은 브랜치에 보완 커밋을 반영했다.
- [x] GitHub에서 두 PR을 Create a merge commit 방식으로 병합했다.
- [x] 양쪽 main에서 pull하여 minsu.md와 jiyun.md를 모두 받았다.

이 점검표는 두 초기 PR을 병합하고 양쪽 pull을 완료한 뒤 최신 main에서 새 작업으로 작성했습니다.
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git add checklist.md
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git commit -m "Resolve same-line checklist title conflict by retaining both perspectives"
[feature/jiyun-title 93ad058] Resolve same-line checklist title conflict by retaining both perspectives
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git push origin feature/jiyun-title
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
   7bd9366..93ad058  feature/jiyun-title -> feature/jiyun-title
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr diff https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS
diff --git a/checklist.md b/checklist.md
index 01a7f18..678f77e 100644
--- a/checklist.md
+++ b/checklist.md
@@ -1,4 +1,4 @@
-# Git 협업 실습 점검표
+# Git 협업 확인 — 지윤의 관점
 
 - [x] 민수·지윤 폴더가 같은 origin 저장소를 사용한다.
 - [x] 각 main에서 작업 브랜치를 선택하여 서로 다른 역할 문서를 커밋했다.
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr edit https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --body-file D:\ALEPH_Codemit\nextjs-notes\.cache\jiyun-title-resolved-body.md
https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr merge https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --merge
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,state,mergedAt,mergeCommit,baseRefName,headRefName,files,commits
{"baseRefName":"main","commits":[{"authoredDate":"2026-10-12T08:00:46Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T08:00:46Z","messageBody":"","messageHeadline":"Change shared checklist title from Jiyun perspective","oid":"7bd9366ca06721dbd135db50d6e9e3ce001e887d"},{"authoredDate":"2026-10-12T08:04:55Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T08:04:55Z","messageBody":"…ives","messageHeadline":"Resolve same-line checklist title conflict by retaining both perspect…","oid":"93ad058e775b89c5d379e8fe08f934727f4838cc"}],"files":[{"path":"checklist.md","additions":1,"deletions":1,"changeType":"MODIFIED"}],"headRefName":"feature/jiyun-title","mergeCommit":{"oid":"3efd941bcd014b66d4714ee880330a9651aac10b"},"mergedAt":"2026-10-12T08:04:47Z","state":"MERGED","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git switch main
Your branch is up to date with 'origin/main'.
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git pull --ff-only origin main
Updating 615de75..3efd941
Fast-forward
 checklist.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
   615de75..3efd941  main       -> origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git show HEAD:checklist.md
# Git 협업 확인 — 민수와 지윤의 공동 점검

- [x] 민수·지윤 폴더가 같은 origin 저장소를 사용한다.
- [x] 각 main에서 작업 브랜치를 선택하여 서로 다른 역할 문서를 커밋했다.
- [x] 브랜치 전환 전후 파일 차이와 main으로의 로컬 merge를 확인했다.
- [x] main을 base로 PR 두 개를 생성하고 Files changed를 직접 읽었다.
- [x] 민수 PR 생성 후 같은 브랜치에 보완 커밋을 반영했다.
- [x] GitHub에서 두 PR을 Create a merge commit 방식으로 병합했다.
- [x] 양쪽 main에서 pull하여 minsu.md와 jiyun.md를 모두 받았다.

이 점검표는 두 초기 PR을 병합하고 양쪽 pull을 완료한 뒤 최신 main에서 새 작업으로 작성했습니다.
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git branch -d feature/minsu-title
Deleted branch feature/minsu-title (was 788bafc).
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git push origin --delete feature/minsu-title
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
 - [deleted]         feature/minsu-title
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git fetch --prune origin
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * [new branch]      feature/jiyun-title -> origin/feature/jiyun-title
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git switch main
Your branch is behind 'origin/main' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
Switched to branch 'main'
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git pull --ff-only origin main
Updating 615de75..3efd941
Fast-forward
 checklist.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
From https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS
 * branch            main       -> FETCH_HEAD
   3b014b5..3efd941  main       -> origin/main
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git show HEAD:checklist.md
# Git 협업 확인 — 민수와 지윤의 공동 점검

- [x] 민수·지윤 폴더가 같은 origin 저장소를 사용한다.
- [x] 각 main에서 작업 브랜치를 선택하여 서로 다른 역할 문서를 커밋했다.
- [x] 브랜치 전환 전후 파일 차이와 main으로의 로컬 merge를 확인했다.
- [x] main을 base로 PR 두 개를 생성하고 Files changed를 직접 읽었다.
- [x] 민수 PR 생성 후 같은 브랜치에 보완 커밋을 반영했다.
- [x] GitHub에서 두 PR을 Create a merge commit 방식으로 병합했다.
- [x] 양쪽 main에서 pull하여 minsu.md와 jiyun.md를 모두 받았다.

이 점검표는 두 초기 PR을 병합하고 양쪽 pull을 완료한 뒤 최신 main에서 새 작업으로 작성했습니다.
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git branch -d feature/jiyun-title
Deleted branch feature/jiyun-title (was 93ad058).
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git push origin --delete feature/jiyun-title
To https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
 - [deleted]         feature/jiyun-title
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git fetch --prune origin
(출력 없음)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,title,state,baseRefName,headRefName,mergedAt,mergeCommit,commits,files,body
{"baseRefName":"main","body":"Minsu 역할의 Git 협업 실습 문서를 추가합니다. 작업 브랜치에서 커밋하고 로컬 main으로 이동하여 merge 방향과 파일 차이를 확인했습니다.\r\n\r\n변경 파일: `minsu.md`. Base: `main`, head: `feature/minsu`.\r\n\r\nPR 생성 후 같은 작업 브랜치에 보완 커밋을 추가했습니다. 문서에 로컬 merge와 원격 PR 병합의 차이를 설명했습니다.\r\n\r\n직접 Files changed의 실제 diff와 커밋 목록을 읽었습니다. 역할 문서 외 다른 프로젝트 파일이 변경되지 않았고, 내용과 main으로의 병합 방향을 확인했습니다. 단독 실습이므로 자신의 PR에 Approve를 제출하지 않습니다.\r\n","commits":[{"authoredDate":"2026-10-12T07:44:43Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:43Z","messageBody":"","messageHeadline":"Add Minsu collaboration practice record","oid":"9d5f4207b82e0a22cc12e30a3999eb532174d816"},{"authoredDate":"2026-10-12T07:44:55Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:55Z","messageBody":"","messageHeadline":"Clarify local merge direction and remote pull after opening PR","oid":"6bad01aa16e08bcb19fe537e6fe627b383e8acf2"}],"files":[{"path":"minsu.md","additions":10,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/minsu","mergeCommit":{"oid":"45a550d8e3b6670a60950bc2b7ab79b598ec3ec6"},"mergedAt":"2026-10-12T07:52:53Z","state":"MERGED","title":"Add Minsu Git collaboration practice document","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh api repos/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/git/commits/45a550d8e3b6670a60950bc2b7ab79b598ec3ec6 --jq ".parents | length"
2
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,title,state,baseRefName,headRefName,mergedAt,mergeCommit,commits,files,body
{"baseRefName":"main","body":"Jiyun 역할의 Git 협업 실습 문서를 추가합니다. 작업 브랜치에서 커밋하고 로컬 main으로 이동하여 merge 방향과 파일 차이를 확인했습니다.\r\n\r\n변경 파일: `jiyun.md`. Base: `main`, head: `feature/jiyun`.\r\n\r\n직접 Files changed의 실제 diff와 커밋 목록을 읽었습니다. 역할 문서 외 다른 프로젝트 파일이 변경되지 않았고, 내용과 main으로의 병합 방향을 확인했습니다. 단독 실습이므로 자신의 PR에 Approve를 제출하지 않습니다.\r\n","commits":[{"authoredDate":"2026-10-12T07:44:50Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:44:50Z","messageBody":"","messageHeadline":"Add Jiyun collaboration practice record","oid":"ad583805ad91058a76b9a9a91a7292640ca1b17a"}],"files":[{"path":"jiyun.md","additions":6,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/jiyun","mergeCommit":{"oid":"dbec7990103817b39bbe9c5a495bc38473dfc978"},"mergedAt":"2026-10-12T07:52:57Z","state":"MERGED","title":"Add Jiyun Git collaboration practice document","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh api repos/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/git/commits/dbec7990103817b39bbe9c5a495bc38473dfc978 --jq ".parents | length"
2
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,title,state,baseRefName,headRefName,mergedAt,mergeCommit,commits,files,body
{"baseRefName":"main","body":"두 초기 PR을 merge commit으로 병합한 뒤 두 clone의 main에서 pull한 결과를 점검표로 기록합니다.\r\n\r\n변경 파일: `checklist.md`. 최신 main에서 새 브랜치를 만들었습니다. 로컬 diff를 직접 확인했고 체크한 항목은 실제 Git 명령 출력으로 확인한 작업입니다.\r\n","commits":[{"authoredDate":"2026-10-12T07:53:17Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T07:53:17Z","messageBody":"","messageHeadline":"Add verified Git collaboration checklist after both initial PRs","oid":"4ec2e640188faff1cf5d91cd47dc64f76781f4e2"}],"files":[{"path":"checklist.md","additions":11,"deletions":0,"changeType":"ADDED"}],"headRefName":"feature/checklist","mergeCommit":{"oid":"615de754dcfb3d85b0b83ba8dc08b450354df575"},"mergedAt":"2026-10-12T07:55:50Z","state":"MERGED","title":"Add verified collaboration checklist from latest main","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh api repos/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/git/commits/615de754dcfb3d85b0b83ba8dc08b450354df575 --jq ".parents | length"
2
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,title,state,baseRefName,headRefName,mergedAt,mergeCommit,commits,files,body
{"baseRefName":"main","body":"같은 줄 충돌 해결 실습을 위해 checklist.md의 첫 제목을 # Git 협업 확인 — 민수의 관점로 변경합니다. 로컬 diff를 직접 읽어 첫 줄만 바뀌었음을 확인했습니다.\r\n","commits":[{"authoredDate":"2026-10-12T08:00:38Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T08:00:38Z","messageBody":"","messageHeadline":"Change shared checklist title from Minsu perspective","oid":"788bafc418e34d652fc68d9754d7c3d11ab5a9f8"}],"files":[{"path":"checklist.md","additions":1,"deletions":1,"changeType":"MODIFIED"}],"headRefName":"feature/minsu-title","mergeCommit":{"oid":"3b014b590b12038414c81a408d9ead75c7c22fc8"},"mergedAt":"2026-10-12T08:04:37Z","state":"MERGED","title":"Update shared checklist title from Minsu perspective","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh api repos/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/git/commits/3b014b590b12038414c81a408d9ead75c7c22fc8 --jq ".parents | length"
2
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh pr view https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5 --repo Miko351/ALEPH-CODEMIT-ASSIGNMENTS --json url,title,state,baseRefName,headRefName,mergedAt,mergeCommit,commits,files,body
{"baseRefName":"main","body":"checklist.md 첫 줄에서 실제 merge 충돌을 해결했습니다.\r\n\r\n민수 변경: Git 협업 확인 — 민수의 관점\r\n지윤 변경: Git 협업 확인 — 지윤의 관점\r\n최종 내용: Git 협업 확인 — 민수와 지윤의 공동 점검\r\n\r\n양쪽의 역할을 제목에 함께 남기는 내용을 선택했습니다. 최신 main을 작업 브랜치로 merge하고 로컬에서 충돌 표식을 제거·커밋·push했습니다. 같은 PR의 Files changed를 다시 읽어 제목과 나머지 점검 항목 보존을 확인했습니다.\r\n","commits":[{"authoredDate":"2026-10-12T08:00:46Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T08:00:46Z","messageBody":"","messageHeadline":"Change shared checklist title from Jiyun perspective","oid":"7bd9366ca06721dbd135db50d6e9e3ce001e887d"},{"authoredDate":"2026-10-12T08:04:55Z","authors":[{"email":"miko351563@gmail.com","id":"U_kgDODRT7UA","login":"Miko351","name":"Miko351"}],"committedDate":"2026-10-12T08:04:55Z","messageBody":"…ives","messageHeadline":"Resolve same-line checklist title conflict by retaining both perspect…","oid":"93ad058e775b89c5d379e8fe08f934727f4838cc"}],"files":[{"path":"checklist.md","additions":1,"deletions":1,"changeType":"MODIFIED"}],"headRefName":"feature/jiyun-title","mergeCommit":{"oid":"3efd941bcd014b66d4714ee880330a9651aac10b"},"mergedAt":"2026-10-12T08:04:47Z","state":"MERGED","title":"Update shared checklist title from Jiyun perspective","url":"https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5"}
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\next-practice`

```text
> gh api repos/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/git/commits/3efd941bcd014b66d4714ee880330a9651aac10b --jq ".parents | length"
2
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git remote -v
origin	https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git (fetch)
origin	https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git (push)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git branch -vv
* main 3efd941 [origin/main] Merge pull request #5 from Miko351/feature/jiyun-title
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git reflog show main "--format=%h %gs" -8
3efd941 pull --ff-only origin main: Fast-forward
615de75 pull --ff-only origin main: Fast-forward
dbec799 pull --ff-only origin main: Fast-forward
9d5f420 merge feature/minsu: Fast-forward
b7ae56a clone: from https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git rev-parse HEAD
3efd941bcd014b66d4714ee880330a9651aac10b
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu`

```text
> git ls-files
checklist.md
jiyun.md
minsu.md
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git remote -v
origin	https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git (fetch)
origin	https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git (push)
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git branch -vv
* main 3efd941 [origin/main] Merge pull request #5 from Miko351/feature/jiyun-title
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git reflog show main "--format=%h %gs" -8
3efd941 pull --ff-only origin main: Fast-forward
615de75 pull --ff-only origin main: Fast-forward
dbec799 pull --ff-only origin main: Fast-forward
ad58380 merge feature/jiyun: Fast-forward
b7ae56a clone: from https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS.git
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git rev-parse HEAD
3efd941bcd014b66d4714ee880330a9651aac10b
[exit 0]
```

### `D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun`

```text
> git ls-files
checklist.md
jiyun.md
minsu.md
[exit 0]
```

