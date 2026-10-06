# 사이 게시판 — Flask · Jinja2 · PostgreSQL

작업 폴더: `D:\ALEPH_Codemit\posts-crud`  
게시판 코드: `mini-watch/general/`  
업로드 파일: 프로젝트 폴더 안의 `posts-crud.zip`

기존 mini-watch 프로젝트 경로가 없다는 확인을 받아 **새 프로젝트로 구성**했습니다. 새 `db.py`에 `connect_db()`를 정의하고 모든 게시글 DB 함수가 이를 사용합니다. 기존 로그인·DB 설정·SQL·연습 파일·감시 서비스가 제공되지 않았으므로 해당 파일을 덮어쓰거나 삭제한 것은 없습니다. `mini-watch/monitor/`는 새 프로젝트의 요청 기록 수집을 확인하는 예제 감시 서비스입니다. 기존 수업 프로젝트를 전달받으면 원래 연결 설정과 감시 프로토콜에 맞춰 통합할 수 있습니다.

## 실행

Python 3.11 이상과 PostgreSQL이 필요합니다. ZIP은 소스 제출용이며 DB 데이터, 접속 비밀번호, Python 가상환경, PostgreSQL 바이너리는 포함하지 않습니다.

프로젝트 루트에서 설치합니다.

```powershell
cd D:\ALEPH_Codemit\posts-crud
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock.txt
```

### 이미 PostgreSQL이 있는 경우

기존 `posts(id, title, body)` 테이블과 자동 번호 시퀀스가 있으면 그대로 사용합니다. 새 프로젝트에서 DB 접속 정보만 설정하려면:

```powershell
Copy-Item mini-watch\general\.env.example mini-watch\general\.env
```

`mini-watch/general/.env`의 `DATABASE_URL`을 실제 PostgreSQL 접속 정보로 수정하세요. 기존 `.env` 파일이 있다면 복사로 덮어쓰지 마세요. 비밀번호의 특수문자는 URL 인코딩해야 합니다.

테이블이 없는 새 DB만 초기화하려면:

```powershell
.\.venv\Scripts\python.exe scripts/init_db.py
```

이 명령은 기존 `posts`가 있으면 테이블·데이터·시퀀스를 변경하지 않습니다. 신규 DB에서만 `sql/001_posts.sql`을 적용합니다. 기존 테이블을 지우거나 번호를 초기화하는 SQL은 없습니다.

### PostgreSQL이 없는 Windows PC

프로젝트 전용 PostgreSQL을 로컬 캐시에 구성하는 선택 도구를 제공합니다.

```powershell
.\.venv\Scripts\python.exe scripts/dev_postgres.py setup
.\.venv\Scripts\python.exe scripts/init_db.py
```

공식 EDB Windows 바이너리를 다운로드하여 `.cache/` 안에 설치하고, 별도 클러스터를 `127.0.0.1:55432`에서 실행합니다. 시스템 서비스와 다른 PostgreSQL DB는 변경하지 않습니다. 새 임의 비밀번호로 `.env`를 생성하며 기존 `.env`가 있으면 유지합니다. DB 서버를 다시 실행하거나 종료할 때는:

```powershell
.\.venv\Scripts\python.exe scripts/dev_postgres.py start
.\.venv\Scripts\python.exe scripts/dev_postgres.py status
.\.venv\Scripts\python.exe scripts/dev_postgres.py stop
```

### 게시판과 감시 서비스 실행

첫 번째 터미널에서 게시판:

```powershell
cd D:\ALEPH_Codemit\posts-crud
.\.venv\Scripts\python.exe mini-watch/general/app.py
```

다른 터미널에서 감시 서비스:

```powershell
cd D:\ALEPH_Codemit\posts-crud
.\.venv\Scripts\python.exe mini-watch/monitor/app.py
```

- [게시판 목록](http://127.0.0.1:5000/)
- [새 글 작성](http://127.0.0.1:5000/board/new)
- [수집된 요청 기록](http://127.0.0.1:5001/logs)

`MONITOR_URL`을 비워두면 요청 기록은 `general/instance/requests.log`에만 남습니다. 감시 서버가 꺼져 있어도 게시판 요청은 처리되며, 전송 실패는 경고 로그로 기록됩니다. 기록에는 요청 시각·메서드·경로·상태 코드·처리 시간만 포함하고 폼 입력 내용·쿼리 문자열은 포함하지 않습니다.

## 화면과 흐름

| 요청 | 주소 | 화면·응답 |
| --- | --- | --- |
| GET | `/` | `index.html`, 번호 오름차순 목록, 빈 목록 안내 |
| GET | `/board/<int:post_id>` | `detail.html`, 번호·제목·내용, 목록·수정·삭제 링크 |
| GET / POST | `/board/new` | `new.html`, 저장 후 상세로 303 이동 |
| GET / POST | `/board/<int:post_id>/edit` | `edit.html`, 수정 후 상세로 303 이동 |
| GET / POST | `/board/<int:post_id>/delete` | `delete.html`, 확인 후 삭제, 목록으로 303 이동 |
| 오류 | 해당 요청 주소 | `error.html`, 없는 글은 404 |

작성·수정은 서버에서 앞뒤 공백을 제거하고 동일한 입력 검사 함수를 사용합니다. 제목이나 내용이 비어 있으면 입력값과 오류를 폼에 다시 표시하고 **400**을 반환합니다. 이때 INSERT·UPDATE는 실행하지 않습니다. 없는 게시글 수정은 입력 내용과 관계없이 **404**입니다.

GET 삭제 확인과 취소는 데이터를 변경하지 않습니다. 실제 삭제는 POST에서만 실행합니다. 모든 변경 요청은 **303**으로 GET 화면에 이동하므로 상세를 새로고침해도 같은 POST가 재실행되지 않습니다. 번호는 DB 시퀀스에서 생성하며 삭제한 번호를 재사용하거나 기존 번호를 다시 정렬하지 않습니다.

## 역할별 코드

```text
posts-crud/
├─ mini-watch/
│  ├─ general/
│  │  ├─ app.py                 # 앱 생성, 설정, Blueprint·로깅 등록, 실행
│  │  ├─ db.py                  # connect_db()
│  │  ├─ post_rules.py          # 작성·수정 공통 입력 검사
│  │  ├─ request_logging.py     # 요청 기록 및 감시 서버 전송
│  │  ├─ requirements.txt
│  │  ├─ repositories/posts.py  # find_post 및 CRUD SQL, 데이터 반환
│  │  ├─ routes/posts.py        # Blueprint, HTML·303·400·404 결정
│  │  ├─ templates/            # 필수 6개 화면, 공통 레이아웃·폼
│  │  ├─ static/style.css
│  │  └─ sql/001_posts.sql      # 신규 DB용 테이블·시퀀스 생성
│  └─ monitor/app.py            # 새 프로젝트용 감시 서비스
├─ scripts/                    # DB 초기화, 로컬 PostgreSQL, ZIP 생성
├─ tests/                      # 실제 PostgreSQL 및 브라우저 테스트
├─ requirements-dev.lock.txt
├─ pytest.ini
└─ README.md
```

SQL 입력값은 모두 `%s`와 매개변수로 전달합니다. DB 함수는 데이터 또는 `None`만 반환하고 HTTP 응답을 만들지 않습니다. 연결과 커서는 닫히며 변경은 트랜잭션에서 커밋되고 예외가 발생하면 롤백됩니다. Jinja2의 자동 이스케이프를 유지해 제목·본문의 HTML을 실행하지 않습니다.

선택 실습인 로그인 판정 화면은 추가하지 않았습니다. 게시판에 로그인 접근 제한이나 세션 기능도 없습니다.

## 검증

2026-10-06 검증 결과: PostgreSQL 18.6에서 통합 테스트 **24개 통과**, 실제 데스크톱·모바일 Chromium 흐름 **2개 통과**, Python 컴파일 통과. 기존 테이블이 있을 때 초기화 명령이 테이블과 시퀀스를 변경하지 않는 것도 확인했습니다.

테스트는 SQLite나 모의 DB가 아니라 **실제 PostgreSQL**을 사용합니다. 각 테스트마다 무작위 `test_posts_...` 스키마를 생성해 격리하고 종료 시 해당 테스트 스키마만 정리합니다. 일반 게시판의 `public.posts`는 변경하지 않습니다. 테스트 계정에는 테스트 스키마 생성 권한이 필요합니다.

```powershell
cd D:\ALEPH_Codemit\posts-crud
.\.venv\Scripts\python.exe -m compileall -q mini-watch scripts tests
.\.venv\Scripts\python.exe -m pytest -q -m 'not browser' --basetemp .cache/pytest-api
```

다른 테스트 DB를 사용하려면 `TEST_DATABASE_URL`을 설정합니다. 설정하지 않으면 로컬 `.env`의 DB에서 격리 스키마를 만듭니다.

실제 데스크톱·모바일 Chromium 화면의 CRUD 흐름도 검증합니다.

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = 'D:\ALEPH_Codemit\posts-crud\.cache\ms-playwright'
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest -q -m browser --basetemp .cache/pytest-browser
```

완료 기준별 테스트는 `CHECKLIST.md`에 정리했습니다. 직접 테스트할 때는 목록 → 작성 → 상세 → 새로고침 → 목록 → 수정 → 삭제 확인 → 취소 → 삭제 확인 → 삭제 순서로 확인하면 됩니다. 공백 입력의 400과 삭제 후 404도 확인하세요.

## Git과 ZIP

이 프로젝트만 별도 Git 저장소로 관리합니다. 작업 폴더에서 `git log -1 --oneline`, `git status --short`로 커밋을 확인할 수 있습니다. GitHub 원격 저장소 주소는 제공되지 않아 원격 업로드는 수행하지 않았습니다.

ZIP에는 `posts-crud.bundle`도 넣어 **실제 Git 커밋 이력**을 전달합니다. 압축을 푼 폴더에서 `git clone posts-crud.bundle recovered-posts-crud`를 실행하면 별도 폴더로 저장소를 복원할 수 있습니다. 수정한 내용을 새로 커밋한 뒤 제출할 때는 `git bundle create posts-crud.bundle --all`로 bundle을 갱신하고 ZIP을 다시 생성하세요.

업로드용 ZIP은 폴더 안에 생성합니다.

```powershell
.\.venv\Scripts\python.exe scripts/package.py
```

`posts-crud.zip`에는 소스·테스트·SQL·설정 예시·실행 안내와 lock 파일을 넣습니다. `.env`, 로그, 회원·게시글 데이터, PostgreSQL 바이너리, 가상환경, 캐시, `.git`은 제외합니다. 압축 무결성·Python 문법·필수 템플릿 존재도 검사합니다.

공식 참고 문서: [Flask Blueprint](https://flask.palletsprojects.com/en/stable/blueprints/), [Psycopg SQL 매개변수와 트랜잭션](https://www.psycopg.org/docs/usage), [EDB PostgreSQL 바이너리](https://www.enterprisedb.com/download-postgresql-binaries).
