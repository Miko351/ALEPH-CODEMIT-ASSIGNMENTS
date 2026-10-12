# 사이 워치 — React와 Flask 감시 대시보드

일반 게시판의 실제 요청 기록을 PostgreSQL에 수집하고, 운영자가 로그인하여 관찰 메모를 작성·조회·수정·삭제하는 실습 프로젝트입니다.

작업 폴더는 `D:\ALEPH_Codemit\monitor-dashboard`입니다. 소스 제출용 `monitor-dashboard.zip`도 이 폴더에 생성합니다. ZIP은 환경 설정·계정·DB 데이터·설치된 실행 환경을 포함하지 않으므로 아래 순서로 준비하세요.

## 시작 자료와 직접 구현한 부분

수업의 mini-watch 원본 폴더는 제공되지 않았습니다. 이전 과제에서 직접 구현한 `posts-crud/mini-watch/general`의 Flask·Jinja2 게시판, DB 연결, 공통 입력 검사, SQL 저장소, 요청 로깅을 시작 자료로 복사했습니다. 이전 작업 폴더는 변경하지 않았습니다.

이번에 감시 API의 계정 해시 검증, 쿠키·세션 로그인 유지와 API 인증, PostgreSQL 요청 기록 수집, 처리 상태를 포함한 관찰 메모 CRUD, 공통 JSON 검증, React 화면과 API 모듈, Vite 프록시, DB·계정 준비 도구, 통합 테스트를 구현했습니다. 일반 서비스는 포트를 5100으로 변경하고 기록 수신 주소를 새 감시 API로 연결했습니다. 게시판의 기존 주소·GET/POST·303/400/404 동작과 로컬 요청 로그는 유지합니다.

## 필요한 프로그램

- Windows, Python 3.11 이상
- Node.js 22.12 이상과 npm
- PostgreSQL: 기존 설치를 사용하거나 아래의 프로젝트 전용 Windows DB 준비 도구 사용

아래 명령은 **Windows CMD** 기준입니다. 프로젝트를 다른 위치에 풀었다면 `cd /d` 경로를 그 위치로 바꾸세요.

## 1. 패키지 설치

```cmd
cd /d D:\ALEPH_Codemit\monitor-dashboard
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
cd monitor\frontend
npm ci
cd ..\..
```

Python 패키지는 루트 `requirements.txt`, 프론트엔드는 `package.json`과 `package-lock.json`으로 관리합니다. 각 백엔드의 requirements도 제공합니다. `npm ci`는 제출한 lock 파일의 버전을 설치합니다.

## 2. DB 및 환경 설정 준비

### 방법 A: PostgreSQL이 없는 Windows PC

프로젝트 전용 PostgreSQL을 `.cache`에 준비하는 도구입니다. 공식 EDB Windows 바이너리를 다운로드하므로 첫 실행은 인터넷 연결과 여유 디스크 공간이 필요합니다.

```cmd
cd /d D:\ALEPH_Codemit\monitor-dashboard
.venv\Scripts\python.exe scripts\dev_postgres.py setup
.venv\Scripts\python.exe scripts\init_db.py
```

별도 클러스터를 `127.0.0.1:55433`에서 실행하고 `monitor_dashboard` DB를 생성합니다. 임의 비밀번호가 담긴 `general/.env`와 `monitor/backend/.env`, 세션 서명용 임의 `SECRET_KEY`를 자동 준비합니다. 기존 DB 설정과 이미 생성한 세션 키는 유지합니다. DB와 설정은 프로젝트 내부에만 준비하고 시스템 서비스나 다른 프로젝트 DB는 변경하지 않습니다.

PC를 재시작한 후에는:

```cmd
.venv\Scripts\python.exe scripts\dev_postgres.py start
```

DB 상태 확인과 종료:

```cmd
.venv\Scripts\python.exe scripts\dev_postgres.py status
.venv\Scripts\python.exe scripts\dev_postgres.py stop
```

### 방법 B: 기존 PostgreSQL 사용

`psql`이 PATH에 등록되어 있다면 새 DB를 한 번 준비합니다. 이미 생성한 DB를 사용할 때는 CREATE DATABASE 명령을 건너뛰세요.

```cmd
psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -c "CREATE DATABASE monitor_dashboard;"
copy general\.env.example general\.env
copy monitor\backend\.env.example monitor\backend\.env
```

각 `.env`의 `DATABASE_URL`에 본인의 접속 정보를 설정합니다. 두 서비스는 같은 DB를 사용해도 되고 각각 별도 DB를 사용해도 됩니다. 복사 명령으로 기존 `.env`를 덮어쓰지 마세요. 비밀번호에 특수문자가 있으면 URL 인코딩하세요. CMD에서 환경 변수 `DATABASE_URL`을 설정한 경우 `.env`보다 우선하며 두 서비스에 적용됩니다.

```cmd
.venv\Scripts\python.exe scripts\configure_session.py
.venv\Scripts\python.exe scripts\init_db.py
```

`configure_session.py`는 실제 `.env`에 64자리 임의 세션 서명 키를 한 번 생성하고 기존 키는 유지합니다. `.env.example`의 자리 표시자 키로는 서버를 시작할 수 없습니다. 서버 재실행 후에도 같은 키를 사용해야 기존 로그인 쿠키를 검증할 수 있습니다.

DB 준비 순서는 `general/sql/001_posts.sql` → `monitor/backend/sql/002_monitor.sql` → `monitor/backend/sql/003_note_status.sql`입니다. 준비 도구가 해당 서비스의 DB에 순서대로 실행합니다. 기존 posts 테이블이 있으면 게시글 테이블과 시퀀스를 유지하고, 감시 테이블도 `IF NOT EXISTS`로 준비하여 기존 데이터는 삭제하지 않습니다. 상태 마이그레이션은 기존 notes에 status 컬럼을 추가하고 기존 메모를 '확인 전'으로 시작합니다. 반복 실행해도 저장한 상태를 초기화하지 않습니다. 테이블 역할은 다음과 같습니다.

| 테이블 | 저장 내용 |
| --- | --- |
| posts | 기존 게시판 번호·제목·본문, 자동 번호 시퀀스 |
| users | 로그인 아이디·사용자 이름·비밀번호 해시 |
| events | 요청 시각·메서드·경로·상태 코드·처리 시간 |
| notes | 메모 번호·제목·내용·처리 상태·작성 및 수정 시각 |

### 설정값

| 파일·설정 | 용도 |
| --- | --- |
| general/.env → DATABASE_URL | 게시판 PostgreSQL 접속 주소 |
| general/.env → MONITOR_URL | `http://127.0.0.1:5200/api/events`, 기록을 JSON으로 전송할 주소. 비우면 로컬 로그만 기록 |
| general/.env → REQUEST_LOG_PATH | 로컬 요청 기록 파일, 기본 `instance/requests.log` |
| general/.env → PORT | 일반 서비스 포트, 5100 |
| monitor/backend/.env → DATABASE_URL | 감시 PostgreSQL 접속 주소 |
| monitor/backend/.env → PORT | 감시 API 포트, 5200 |
| monitor/backend/.env → SECRET_KEY | Flask 로그인 쿠키 서명 키, `configure_session.py`로 생성하고 Git·ZIP에서 제외 |
| monitor/frontend/.env.example → MONITOR_API_TARGET | Vite `/api` 프록시 대상, 기본 `http://127.0.0.1:5200` |
| monitor/frontend/.env.example → VITE_GENERAL_URL | 일반 게시판 링크, 기본 `http://127.0.0.1:5100` |

프론트 기본 설정은 별도 `.env` 없이 동작합니다. 변경이 필요하면 `.env.example`을 `.env`로 복사하고 Vite를 재실행하세요. DB 비밀번호를 프론트 환경 변수에 넣지 마세요. 모든 실제 `.env`는 Git과 ZIP에서 제외합니다.

## 3. 실습 계정 생성

```cmd
cd /d D:\ALEPH_Codemit\monitor-dashboard
.venv\Scripts\python.exe scripts\create_user.py --username operator --name "운영자"
```

직접 정한 8자 이상의 비밀번호를 두 번 입력합니다. 입력은 화면에 표시되지 않고 명령줄·README에 남지 않습니다. Werkzeug의 `generate_password_hash()`로 생성한 scrypt 해시만 DB에 저장하고 로그인은 `check_password_hash()`로 확인합니다. 이미 있는 아이디는 덮어쓰지 않으므로 다른 아이디로 생성하세요. 제출물에 미리 정해진 실제 로그인 비밀번호는 없습니다.

## 4. 서비스 실행

**CMD 창 1: 감시 API**

```cmd
cd /d D:\ALEPH_Codemit\monitor-dashboard
.venv\Scripts\python.exe monitor\backend\app.py
```

**CMD 창 2: 일반 게시판**

```cmd
cd /d D:\ALEPH_Codemit\monitor-dashboard
.venv\Scripts\python.exe general\app.py
```

**CMD 창 3: React 화면**

```cmd
cd /d D:\ALEPH_Codemit\monitor-dashboard\monitor\frontend
npm run dev
```

- 감시 화면: <http://127.0.0.1:5173>
- 일반 게시판: <http://127.0.0.1:5100>
- 감시 API: `http://127.0.0.1:5200/api/events` (로그인 쿠키 필요)

React는 상대 주소 `/api`로 요청하고 Vite가 5200의 Flask로 전달합니다. 프론트에서 DB에 직접 연결하지 않습니다. 개발 서버 종료는 각 창에서 Ctrl+C를 누르세요. 프론트 빌드 확인은 `npm run build`이며, 로컬 빌드 미리보기는 `npm run preview`로 4173에서 실행합니다. 빌드 미리보기도 같은 API 프록시를 사용합니다.

## 사용 흐름과 구현 범위

로그인 입력은 React state로 관리하고 JSON으로 Flask에 전달합니다. 빈 아이디·비밀번호는 400, 잘못된 계정은 401이며 화면에 안내를 표시합니다. 성공하면 사용자 정보를 state에 저장하고 Flask 세션에 사용자 번호를 기록합니다. 로그인 쿠키는 서명되어 있으며 HttpOnly·SameSite=Lax 설정과 8시간의 세션 유효기간을 사용합니다. 로컬 HTTP 실행이므로 Secure는 꺼져 있고 HTTPS 배포 시 켜야 합니다.

React는 첫 로드와 새로고침에서 `GET /api/auth/me`로 로그인 상태를 복구합니다. `POST /api/auth/logout`이 서버 세션을 비우고 쿠키를 만료시킨 뒤 화면도 로그인 폼으로 돌아갑니다. 세션이 없거나 만료·변조되면 `GET /api/events`, 모든 메모 CRUD API, `/api/auth/me`는 JSON **401**을 반환합니다. 서버는 매 요청에서 세션의 사용자 번호를 DB 계정과 비교하므로 삭제한 계정도 거절합니다. React는 보호 API의 401을 받으면 로그인 화면과 만료 안내를 표시합니다.

일반 서비스의 자동 전송용 `POST /api/events`는 별도 수신 경로로 로그인 검사에서 제외하여 기존 기록 수집을 유지합니다. 운영자의 기록 조회인 GET과 모든 메모 API는 보호합니다. 로그인은 감시 화면 주소인 5173에서 진행하세요. 서로 다른 호스트 이름(`localhost`와 `127.0.0.1`)으로 접속하면 쿠키가 공유되지 않습니다.

일반 게시판을 연 뒤 **목록 새로고침**을 누르면 실제 요청 기록과 메모 목록을 함께 조회합니다. 기록에는 메서드·경로·상태 코드·시각·처리 시간을 표시합니다. 빈 목록 및 조회 실패 안내를 제공합니다. 일반 서비스의 `requests.post(..., json=event)`가 Flask 수신 API로 보내고 DB에 저장합니다. 전송 실패는 경고 로그를 남기며 게시판 요청은 계속 처리됩니다. 폼 본문·비밀번호·쿼리 문자열은 기록하지 않습니다.

관찰 메모는 새 메모 → 저장 → 상세 → 수정 또는 삭제 확인으로 연결합니다. 목록은 `map()`과 메모 id의 key로 렌더링하며 클릭하면 상세 API를 호출합니다. 작성·수정 폼에서 **확인 전(pending)·확인 중(in_progress)·완료(completed)** 중 처리 상태를 선택할 수 있습니다. API가 상태를 함께 받아 DB에 저장하고 목록·상세에 상태 배지를 표시합니다. 상태 변경은 수정 폼의 저장 버튼으로 확정하며 취소하면 유지됩니다. 작성·수정 성공 후 DB 목록을 다시 조회합니다. 삭제 취소는 메모를 유지하고 삭제 확정만 DELETE를 전송합니다. 삭제 후 목록을 다시 조회하고 상세 선택을 해제합니다.

서버는 작성·수정에 같은 검증 함수를 사용하여 앞뒤 공백을 제거합니다. 빈 값·공백만 있는 값과 허용하지 않은 처리 상태는 400이며 기존 DB 제목·내용·상태는 유지됩니다. 상태 없는 작성 요청은 확인 전이 기본값이고, 상태 없는 수정 요청은 기존 상태를 유지합니다. 로그인한 사용자의 없는 메모 조회·수정·삭제는 404입니다. 모든 SQL 입력은 `%s`와 별도 매개변수로 전달합니다. DB 연결의 문맥 관리자는 변경을 커밋하고 예외 시 롤백합니다. 로그인·조회·저장·삭제·네트워크 실패는 화면에 표시하며 실패를 성공으로 표시하지 않습니다.

선택 기능 네 가지인 **요청 경로 검색·응답 상태 필터**, **요청 건수 요약**, **메모 처리 상태**, **쿠키·세션 유지와 API 보호**를 모두 구현했습니다. 필터 초기화 버튼으로 전체 목록을 복원합니다. 요약은 DB에서 조회한 전체 이벤트 중 현재 검색·필터에 맞는 목록을 집계하며, 오류 기준은 **상태 코드 400 이상**입니다. 표시한 목록의 행 수와 전체 요청 수, 해당 목록의 오류 행 수와 오류 요청 수가 일치합니다. 메모 개수는 조회한 전체 메모 수입니다.

**새로고침해도 로그인이 유지되고, 메모의 처리 상태와 요청 기록도 DB에 유지됩니다.** 로그아웃 후 새로고침하면 로그인 화면으로 돌아오며 보호 API 직접 호출은 401입니다. 기존 결과물에서 업그레이드할 때는 서비스를 종료하고 `configure_session.py`, `init_db.py`를 실행한 뒤 다시 켜세요. 기존 메모·게시글·계정 비밀번호는 변경하지 않습니다.

## 파일별 역할

```text
monitor-dashboard/
├─ general/                        # 이전 게시판 CRUD와 로깅 유지
│  ├─ app.py, db.py, post_rules.py, request_logging.py
│  ├─ routes/, repositories/, templates/, static/
│  └─ sql/001_posts.sql
├─ monitor/
│  ├─ backend/
│  │  ├─ app.py                     # 설정·Blueprint·오류 처리·실행
│  │  ├─ db.py                      # 공통 connect_db()
│  │  ├─ rules.py                   # JSON 및 공통 메모 검증
│  │  ├─ authentication.py          # 세션 사용자 확인·API 접근 검사
│  │  ├─ routes/auth.py, events.py, notes.py
│  │  ├─ repositories/users.py, events.py, notes.py
│  │  ├─ sql/002_monitor.sql, 003_note_status.sql
│  │  ├─ requirements.txt, .env.example
│  └─ frontend/
│     ├─ src/App.jsx                # 로그인 전후 화면 및 사용자 state
│     ├─ src/components/            # 로그인·대시보드·기록·메모 화면
│     ├─ src/api/                   # 공통 요청·로그인·기록·메모 API
│     ├─ src/styles.css, src/main.jsx
│     ├─ vite.config.js, .env.example
│     └─ package.json, package-lock.json
├─ scripts/                        # DB·계정·ZIP 준비
├─ tests/                          # 실제 PostgreSQL·Vite·Chromium 통합 검증
├─ requirements.txt, requirements-dev.txt
├─ pytest.ini, .gitignore
└─ README.md
```

Flask 저장소는 SQL과 데이터 반환을 담당하고, 라우터가 HTTP 응답을 결정합니다. app.py에서 모듈을 연결합니다. React Dashboard가 목록·선택·화면 상태를 관리하고 자식 컴포넌트에 데이터와 이벤트 함수를 props로 전달합니다. 화면 컴포넌트는 `api/`의 요청 함수를 호출하며 공통 요청 함수에서 HTTP 오류와 연결 실패를 처리합니다. 사용자 입력을 일반 텍스트로 렌더링합니다.

## 통합 검증

테스트는 실제 PostgreSQL의 무작위 `test_dashboard_...` 스키마에 격리하여 실행하고 종료 시 해당 스키마만 제거합니다. 실제 `public` 게시글·메모·계정은 변경하지 않습니다. 테스트 DB 계정에는 스키마 생성 권한이 필요합니다. 다른 DB는 CMD의 `set TEST_DATABASE_URL=...`로 지정할 수 있습니다.

```cmd
cd /d D:\ALEPH_Codemit\monitor-dashboard
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m compileall -q general monitor\backend scripts tests
.venv\Scripts\python.exe -m pytest -q -m "not browser" --basetemp .cache\pytest-api
.venv\Scripts\python.exe -m playwright install chromium
.venv\Scripts\python.exe -m pytest -q -m browser --basetemp .cache\pytest-browser
cd monitor\frontend
npm run build
```

실행 결과: **실제 PostgreSQL API 테스트 44개, 데스크톱·모바일 Chromium 통합 테스트 2개가 모두 통과**했습니다. React의 `npm run build`도 통과했습니다. 세 서비스를 5100·5200·5173에서 실행하여 일반 게시판의 200·303·404 기록이 Vite 프록시를 통해 조회되는 것도 확인했습니다.

API 테스트는 기존 CRUD·오류·기록 수집·데이터 유지 외에 처리 상태 세 가지의 저장·변경·재조회, 잘못된 상태의 400과 무변경, 기존 메모 보존 마이그레이션, 비로그인 상태의 모든 보호 API 401, 쿠키 속성·변조·만료·삭제한 계정 거절, 새 앱에서의 세션 유지와 로그아웃을 검증합니다. 브라우저 테스트는 데스크톱과 모바일에서 실제 Vite 프록시를 통해 상태 선택·변경·취소·공백 수정 시 상태 보존, 새로고침 후 로그인 및 상태 유지, 로그아웃 후 API 401, 쿠키가 사라진 경우 로그인 화면 복귀와 만료 안내까지 확인합니다.

직접 통합 확인할 때는 일반 게시판에서 글을 작성·조회한 뒤 `/board/2147483647` 같은 없는 주소를 열어 보세요. 감시 화면에서 틀린 비밀번호와 올바른 비밀번호를 차례로 입력하고, 목록을 새로고침해 같은 경로의 200과 404를 비교하세요. 메모를 확인 중 상태로 작성한 뒤 수정하여 완료로 저장하고 공백 입력 시 내용과 상태가 보존되는지 확인하세요. 별도의 메모로 삭제 취소·확정을 확인하고, 새로고침 후 로그인과 완료 상태 유지도 확인하세요. 로그아웃 후 메모·기록 API를 직접 호출하면 401입니다.

## Git과 제출 ZIP

기존 로컬 Git 이력을 유지하며 공통 과제 저장소의 [monitor-dashboard 브랜치](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/tree/monitor-dashboard)에 소스를 보관합니다. 이 폴더의 `origin`은 해당 저장소이며 작업 브랜치는 `monitor-dashboard`입니다. 실제 환경 파일·DB·로그·캐시·가상환경·node_modules·빌드 결과는 제외합니다.

```cmd
cd /d D:\ALEPH_Codemit\monitor-dashboard
git status --short
git log -1 --oneline
.venv\Scripts\python.exe scripts\package.py
```

ZIP 생성 도구는 Git에서 관리하는 소스 파일만 넣고, Python 문법·비밀 설정 파일 제외·압축 무결성을 확인합니다. ZIP은 루트 안의 `monitor-dashboard.zip`에 생성하며 자기 자신을 포함하지 않습니다. ZIP을 다른 폴더에 풀면 그 안의 README 순서대로 DB·계정을 새로 준비하여 실행할 수 있습니다.

공식 참고: [React state와 props](https://react.dev/learn/sharing-state-between-components), [Vite 서버 프록시](https://vite.dev/config/server-options.html#server-proxy), [Psycopg 3 연결 및 SQL 실행](https://www.psycopg.org/psycopg3/docs/basic/usage.html), [Flask Blueprint](https://flask.palletsprojects.com/en/stable/blueprints/), [EDB PostgreSQL 바이너리](https://www.enterprisedb.com/download-postgresql-binaries).
