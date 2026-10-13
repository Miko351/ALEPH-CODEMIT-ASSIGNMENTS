# 기록의 방 — Next.js 메모 앱과 Git 브랜치 협업

홈의 숫자 카운터와 state 기반 메모 앱, 실제 두 clone의 GitHub Flow 실습 기록을 제출합니다. 심화로 같은 줄 충돌 해결, 앱 개선 PR, 기존 Flask·PostgreSQL API를 쓰는 DB 메모 화면도 제공합니다. 기본 앱의 상단 **DB 메모** 링크로 API 화면에 이동할 수 있습니다.

작업 폴더: `D:\ALEPH_Codemit\nextjs-notes\next-practice`  
소스 제출 브랜치: [next-practice](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/tree/next-practice)  
Git 작업 기록: [GIT_WORK.md](GIT_WORK.md)  
일반 Git 실습의 병합 기준: `main` / 저장소 기본 브랜치: 파일 없는 `default`

프로젝트 소스는 `next-practice` 브랜치에 보관합니다. `main`에는 Git 실습 문서만 병합합니다. 앱 개선 PR의 기준 브랜치는 이 저장 방식에 맞춰 `next-practice`로 지정합니다.

## API 심화 3·4 확인 위치

기본 앱에서 <http://127.0.0.1:3000/db-notes>에 접속합니다. 아래 DB·계정·Flask 준비 단계로 API를 5200에서 실행한 뒤 운영자 계정으로 로그인하세요. `/notes`는 React state 실습이며 `/db-notes`는 실제 PostgreSQL 저장 실습입니다.

| 확인할 기능 | 구현 위치 및 실제 요청 |
| --- | --- |
| 목록·상세·등록, 새로고침 후 보존 | components/DatabaseNotes.js, lib/api/notes.js: GET /api/notes, GET /api/notes/:id, POST /api/notes |
| 수정·삭제·취소·오류, 새로고침 후 보존 | 같은 컴포넌트: PUT /api/notes/:id, DELETE /api/notes/:id; 취소 시 변경 요청을 보내지 않음 |
| Flask 연결 | next.config.mjs가 /api 요청을 기존 Flask에 전달; .env.example의 FLASK_API_URL로 설정 |
| DB SQL·400·404 | mini-watch/monitor/backend/repositories/notes.py 및 routes/notes.py |
| 실제 브라우저 확인 | tests/db-notes.spec.js와 GIT_WORK.md의 마지막 API 검증 기록 |

등록 201, 수정·삭제 200, 빈 입력 400, 삭제된 번호 조회·수정·삭제 404를 확인했습니다. 등록·수정 뒤 브라우저를 새로고침하여 DB 내용을 재조회하고, 삭제 뒤 새로고침해 목록에서 제거된 결과도 확인했습니다. 수정·삭제 취소와 잘못된 수정은 기존 데이터를 보존합니다. 쿠키·세션으로 로그인도 새로고침 후 유지됩니다.

## 시작 자료와 직접 작성한 부분

수업에서 만든 Next.js 소스는 제공되지 않아 공식 `create-next-app`으로 새 프로젝트를 준비했습니다. JavaScript, App Router, ESLint, npm을 선택했으며 Tailwind·src 디렉터리는 사용하지 않았습니다.

```cmd
npx create-next-app@latest next-practice --js --eslint --app --no-tailwind --no-src-dir --import-alias "@/*" --use-npm --disable-git --yes
```

생성된 기본 화면을 `npm run dev`로 실행하여 HTTP 200과 기본 제목을 확인한 뒤 수업 요구사항에 맞게 교체했습니다. 설치 버전은 Next.js 16.4.0, React 19.3.0이며 package-lock.json으로 재현합니다. 홈·메모 페이지, 공통 레이아웃과 Link, Counter·Notes·삭제 확인 컴포넌트, 반응형 CSS, 브라우저 테스트를 직접 구현했습니다. 외부 폰트 다운로드 없이 시스템 폰트로 실행됩니다.

심화의 Flask API는 이전 `monitor-dashboard` 과제에서 직접 작성한 코드를 복사했습니다. 계정 해시 검증·세션·psycopg SQL 저장소·요청 기록·메모 상태와 CRUD를 유지하고 Next.js API 호출 화면을 추가했습니다. 기존 프로젝트 폴더의 소스나 DB 데이터는 교체하지 않았습니다. ZIP에는 실행을 재현할 수 있는 general, monitor/backend, SQL과 DB·계정 준비 도구도 포함합니다.

## 필수 메모 앱 설치와 실행 — Windows CMD

Node.js 22.18 이상과 npm이 필요합니다. ZIP을 다른 위치에 풀었다면 경로를 수정하세요. GitHub에서 `next-practice` 브랜치를 clone했다면 해당 폴더에서 같은 명령을 실행하면 됩니다.

```cmd
cd /d D:\ALEPH_Codemit\nextjs-notes\next-practice
npm ci
npm run dev -- --hostname 127.0.0.1 --port 3000
```

- 홈: <http://127.0.0.1:3000>
- 메모: <http://127.0.0.1:3000/notes>
- DB 메모: <http://127.0.0.1:3000/db-notes> (Flask·PostgreSQL 추가 실행 필요)

개발 서버는 Ctrl+C로 종료합니다. 빌드한 앱을 실행하려면:

```cmd
npm run build
npm run start -- --hostname 127.0.0.1 --port 3000
```

홈과 `/notes`는 DB·Flask·Python 없이 동작합니다. `/db-notes`를 사용하려면 아래의 DB·계정·API 준비 단계를 먼저 실행하세요. 프록시 주소를 바꾸려면 루트 .env.example을 .env.local로 복사해 FLASK_API_URL을 설정하고 개발 서버를 다시 실행하거나 다시 build합니다. 브라우저 코드에는 DB 비밀번호를 넣지 않습니다.

## 파일 역할과 학습 내용

| 파일 | 역할 |
| --- | --- |
| app/layout.js | 모든 페이지의 html/body, 공통 헤더·푸터, 홈·메모 Link |
| app/page.js | `/` 홈 화면, Counter 연결 |
| app/notes/page.js | `/notes` 화면, Notes 연결 |
| app/db-notes/page.js | `/db-notes` 화면, DatabaseNotes 연결 |
| components/DatabaseNotes.js | 로그인·DB 메모 CRUD·취소·API 오류 화면 |
| lib/api/ | 화면과 분리된 auth·notes API 호출 함수 |
| next.config.mjs | 기존 Flask API로 /api 요청 프록시 |
| components/Counter.js | 숫자 state와 증가·초기화 버튼 |
| components/Notes.js | 메모 배열·입력·수정·삭제 상태, ID 기반 처리 |
| components/DeleteDialog.js | 삭제 확인·취소, Escape 취소, 기본 dialog 초점 관리 |
| components/Icon.js | 공통 SVG 아이콘 |
| app/globals.css | 공통 디자인과 데스크톱·모바일 배치 |
| tests/notes.spec.js | 실제 프로덕션 앱의 필수 동작 검증 |
| tests/db-notes.spec.js | 기본 앱에서 실제 Flask·PostgreSQL 연동 검증 |

**Next.js와 React의 관계:** React가 컴포넌트·state·이벤트로 UI를 구성하며, Next.js는 React를 기반으로 페이지 라우팅·공통 레이아웃·서버 렌더링·빌드와 실행을 제공합니다. App Router는 파일과 폴더 구조를 URL에 연결합니다.

**page.js와 layout.js:** page.js는 해당 경로에서 표시할 화면을 정의합니다. layout.js는 하위 페이지에 공통으로 적용할 화면 틀을 정의하고 children 위치에 페이지를 표시합니다. 홈과 메모 이동에는 Next.js Link를 사용합니다.

**Client Component:** Counter.js와 Notes.js는 `"use client"`를 선언하고 useState로 값을 바꾸며 버튼·입력 이벤트를 처리합니다. DeleteDialog.js도 브라우저의 dialog API와 이벤트를 사용하므로 Client Component입니다. layout.js와 page.js는 기본 Server Component를 유지하며 인터랙션이 필요한 부분만 Client Component에 둡니다.

**메모 ID와 state:** 초기 메모는 고정 ID 두 개를 사용하고 새 메모는 제출 순간 crypto.randomUUID()로 ID를 생성합니다. map()의 key와 수정·삭제 대상을 ID로 찾으므로 내용이 같은 두 메모도 서로 구별됩니다. 입력은 state로 관리하고 등록·수정 시 trim() 후 빈 값과 공백만 있는 값을 거절합니다. 오류가 나면 기존 목록을 바꾸지 않습니다.

수정 버튼은 기존 내용을 입력칸에 보여 줍니다. 저장하면 같은 ID만 바꾸고 취소하면 원래 내용을 유지합니다. 삭제는 확인 dialog에서 확정한 ID만 제거합니다. 취소·Escape는 그대로 보존합니다. 수정 중인 메모를 삭제하면 입력 폼을 등록 상태로 초기화합니다. 목록이 비면 안내를 표시합니다.

**새로고침과 DB 저장의 차이:** 필수 앱은 브라우저 메모리의 React state만 사용하며 localStorage나 DB에 저장하지 않습니다. 새로고침하면 컴포넌트가 다시 시작하여 코드의 초기 메모 두 개로 돌아옵니다. DB 메모는 서버의 PostgreSQL에 커밋되므로 컴포넌트를 다시 시작해도 API에서 저장한 내용을 다시 조회할 수 있습니다.

## Git 협업 실습

같은 원격 저장소를 아래 두 폴더에서 사용합니다.

```text
D:\ALEPH_Codemit\nextjs-notes\git-practice-minsu
D:\ALEPH_Codemit\nextjs-notes\git-practice-jiyun
```

필수 PR은 [민수 #1](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/1), [지윤 #2](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/2), [점검표 #3](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/3)입니다. 세 PR 모두 base=main이고 **merge commit 방식으로 Merged**되었습니다. 민수 PR에는 생성 후 같은 브랜치의 보완 커밋을 추가했습니다. 각 PR의 실제 diff를 읽은 검토 결과를 PR 본문에 기록했습니다.

로컬 main에서 자기 작업 브랜치를 merge한 방향을 확인했고, 원격 PR 병합 뒤 양쪽 main에서 pull하여 역할 문서와 점검표를 받았습니다. 완료한 자기 작업 브랜치를 로컬과 원격에서 정리했습니다. clone·브랜치 전환·로컬 merge·PR·보완 커밋·병합 후 pull·브랜치 정리 명령과 **실제 출력**, PR의 base/head/커밋/변경 파일/병합 상태는 GIT_WORK.md에 있습니다.

심화 충돌 실습은 [민수 제목 변경 #4](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/4)와 [지윤 제목 변경·충돌 해결 #5](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/5)입니다. checklist.md의 같은 첫 줄을 다르게 변경하고 첫 PR 병합 후 다른 작업 브랜치에서 최신 main을 merge해 실제 충돌을 만들었습니다. 두 역할을 함께 나타내는 제목으로 로컬 해결·커밋·push하고 **같은 PR**을 병합한 뒤 양쪽 pull을 완료했습니다. 선택 이유와 실제 충돌 표식도 GIT_WORK.md에 남겼습니다.

앱 개선은 [빈 목록 안내 개선 PR #6](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/6)에서 실제 진행했습니다. components/Notes.js와 tests/notes.spec.js를 로컬에서 바꾸고 lint·build·데스크톱/모바일 빈 목록 테스트를 통과한 뒤 커밋·push했습니다. 실제 diff를 읽고 merge commit으로 병합한 뒤 로컬 next-practice에서 pull하고 작업 브랜치를 정리했습니다. 프로젝트 소스와 실습 문서를 분리하려는 저장소 구성에 따라 앱 PR의 base는 next-practice입니다. 상세 명령·출력·변경 파일·검토 결과는 GIT_WORK.md에 있습니다.

## 심화: 기존 Flask·PostgreSQL API를 사용하는 Next.js 메모

기본 앱의 `/db-notes`에 연결되어 있으며, 수업의 폴더 구성대로 `mini-watch/monitor/next-frontend`에서도 독립 실행할 수 있습니다. 두 화면 모두 제목·내용·처리 상태를 가진 관찰 메모를 같은 기존 API로 조회·상세·등록·수정·삭제합니다. 로그인 쿠키를 Next.js `/api` 프록시로 전달하여 기존 보호 API를 사용합니다. 기본 앱은 `lib/api/`, 독립 앱은 `api/`에 요청 함수를 분리했습니다.

### 이미 이전 감시 API를 실행하는 경우

기존 PostgreSQL과 `monitor-dashboard/monitor/backend/app.py`를 5200에서 실행하면 기본 앱의 <http://127.0.0.1:3000/db-notes>에서 그대로 연결합니다. 기존 운영자 계정으로 로그인합니다. 독립 앱을 사용하려면 다음 명령을 실행합니다.

```cmd
cd /d D:\ALEPH_Codemit\nextjs-notes\next-practice\mini-watch\monitor\next-frontend
npm ci
npm run dev
```

접속: <http://127.0.0.1:3001>. `FLASK_API_URL` 기본값은 `http://127.0.0.1:5200`입니다. 다른 API 주소를 쓰면 `.env.example`을 `.env.local`로 복사하여 수정하고 개발 서버를 재실행하세요. 빌드 실행에서는 프록시 주소가 빌드 결과에 반영되므로 주소 변경 후 다시 build해야 합니다. 프론트에는 DB 비밀번호를 넣지 않습니다.

### ZIP만 받은 Windows PC에서 DB·계정·API 준비

Python 3.11 이상이 추가로 필요합니다. 아래는 CMD 기준입니다.

```cmd
cd /d D:\ALEPH_Codemit\nextjs-notes\next-practice\mini-watch
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts\dev_postgres.py setup
.venv\Scripts\python.exe scripts\init_db.py
.venv\Scripts\python.exe scripts\create_user.py --username operator --name "운영자"
.venv\Scripts\python.exe monitor\backend\app.py
```

공식 EDB PostgreSQL Windows 바이너리를 캐시에 다운로드하고 이 제출물 전용 클러스터를 **55434**에서 실행합니다. 기존 프로젝트의 55433 DB는 변경하지 않습니다. DB 이름은 next_watch이며 실제 .env와 세션 키를 로컬에 준비합니다. 계정 생성 시 직접 정한 비밀번호를 두 번 입력하고 해시만 저장합니다. 실제 비밀번호는 제출물에 포함하지 않습니다.

기존 PostgreSQL을 사용할 때는 general/.env.example과 monitor/backend/.env.example을 각각 .env로 복사해 DATABASE_URL을 설정하고 `configure_session.py`, `init_db.py`, `create_user.py` 순서로 실행하세요. SQL 준비 순서는 `general/sql/001_posts.sql` → `monitor/backend/sql/002_monitor.sql` → `003_note_status.sql`입니다. 기존 데이터를 삭제하거나 번호를 초기화하지 않습니다.

API가 실행된 CMD 창을 유지하고 다른 창에서 기본 앱을 실행합니다.

```cmd
cd /d D:\ALEPH_Codemit\nextjs-notes\next-practice
npm ci
npm run dev -- --hostname 127.0.0.1 --port 3000
```

접속: <http://127.0.0.1:3000/db-notes>. 독립 API 앱을 사용할 경우에는 다음 명령을 대신 실행합니다.

```cmd
cd /d D:\ALEPH_Codemit\nextjs-notes\next-practice\mini-watch\monitor\next-frontend
npm ci
npm run dev
```

API 화면도 `npm run build` 후 `npm run start`로 3001에서 실행할 수 있습니다. general 게시판이 필요하면 다른 CMD에서 mini-watch/.venv/Scripts/python.exe general/app.py를 실행합니다. 요청 기록 수집 등 기존 API 기능도 유지했습니다.

메모를 저장하면 API가 DB에 커밋하고 목록·상세를 갱신합니다. 수정은 기존 제목·내용·상태를 폼에 불러와 저장한 경우에만 PUT을 전송합니다. 수정·삭제 취소는 자료를 보존합니다. 서버의 400·404·401·연결 실패를 화면에 안내하며 실패를 저장 완료로 표시하지 않습니다. 새로고침 후 로그인과 저장·수정·삭제 결과가 유지됩니다.

## 동작 확인 결과와 자동 테스트

필수 앱은 개발 서버 종료 → npm run build → npm run start 순서로 실제 빌드 결과를 확인했습니다. 데스크톱·모바일 **12개 브라우저 시나리오**를 검증했고 모두 통과했습니다. 같은 내용 두 개의 ID 구분, 한쪽 수정, 수정·삭제 취소, 공백 거절, 수정 중 삭제 후 폼 초기화, 전체 삭제와 빈 목록, 새로고침 초기화, Link 이동·카운터, 화면 가로 넘침을 확인했습니다. lint와 build도 통과했습니다.

```cmd
cd /d D:\ALEPH_Codemit\nextjs-notes\next-practice
npm run lint
npm run build
npx playwright install chromium
npm test
```

Playwright는 프로덕션 앱을 3100에서 자동 실행하고 종료합니다. 최초 브라우저 설치에는 인터넷 연결이 필요합니다. .cache의 화면·trace·설치 자료는 Git과 ZIP에서 제외합니다.

API 심화는 실제 이전 Flask·PostgreSQL에 연결하여 데스크톱·모바일 **2개 통합 시나리오**를 통과했습니다. 로그인 실패·성공, DB 목록·상세·등록·수정·삭제, 400 무변경, 실제 삭제된 번호의 404 오류 화면, 취소 보존, 새로고침 후 DB 결과 유지, 로그아웃 후 401을 확인했습니다. 테스트는 무작위 제목의 자기 테스트 메모만 생성·정리하며 기존 메모를 지우지 않습니다.

2026-10-13 기본 앱에서도 실제 API를 연결해 테스트했으며 **14 passed (11.7s)**입니다. 필수 state 시나리오 12개와 DB 시나리오 2개를 함께 통과했습니다. 실제 메서드·경로·응답 코드와 새로고침 확인 출력은 GIT_WORK.md 마지막에 있습니다.

API 테스트는 5200의 Flask가 실행 중인 상태에서 본인이 만든 실습 계정을 CMD 환경 변수로 설정합니다. 아래의 YOUR_PRACTICE_PASSWORD는 실제 비밀번호로 바꾸되 README나 Git 파일에 기록하지 마세요. 기본 앱 테스트 명령은 다음과 같습니다.

```cmd
cd /d D:\ALEPH_Codemit\nextjs-notes\next-practice
npm run lint
npm run build
npx playwright install chromium
set TEST_USERNAME=operator
set TEST_PASSWORD=YOUR_PRACTICE_PASSWORD
npm test
set TEST_PASSWORD=
```

계정 환경 변수를 설정하지 않으면 기본 state 테스트 12개만 실행하고 DB 테스트 2개는 건너뜁니다. 독립 앱의 API 테스트는 `mini-watch/monitor/next-frontend`에서 같은 환경 변수를 설정하고 npm run build, npm test를 실행합니다.

## 제출 ZIP

ZIP에는 Next.js 소스·두 package.json과 package-lock.json·README·GIT_WORK.md·Git 실습 문서·SQL·설정 예시·DB 준비 도구·테스트를 포함합니다. 실제 .env·계정 비밀번호·토큰·DB·node_modules·.next·가상환경·캐시·Git 내부 디렉터리는 제외합니다. 압축 생성 도구는 scripts/package.py이며 Python 기본 라이브러리만 사용합니다.

ZIP의 Git 작업 기록에는 실제 PR의 base·head·커밋·변경 파일·Merged 상태와 원본 PR 링크를 포함하므로 공개 저장소에서 교차 확인할 수 있습니다. 앱 제출 링크는 저장소 첫 화면 대신 next-practice 브랜치 주소를 사용하세요. default는 파일 없이 유지합니다.

로컬에서 ZIP을 다시 생성하려면:

```cmd
cd /d D:\ALEPH_Codemit\nextjs-notes\next-practice
python scripts\package.py
```

결과는 상위 과제 폴더 `D:\ALEPH_Codemit\nextjs-notes\nextjs-notes.zip`에 생성합니다. Git 실습 clone이 없는 GitHub 소스만 내려받은 경우, 위의 두 실습 폴더를 main 브랜치로 clone한 뒤 실행하세요. ZIP에는 두 실습 폴더의 최종 문서를 넣으며 Git 내부 데이터 대신 GIT_WORK.md와 공개 원본 PR로 과정과 병합을 확인합니다.

공식 참고: [Next.js create-next-app](https://nextjs.org/docs/app/api-reference/cli/create-next-app), [페이지와 레이아웃](https://nextjs.org/docs/app/getting-started/layouts-and-pages), [Server·Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).
