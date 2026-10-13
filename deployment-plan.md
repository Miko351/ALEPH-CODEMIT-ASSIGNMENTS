# Day2 배포 계획·진행 상태

저장소: [Miko351/ALEPH-CODEMIT-ASSIGNMENTS](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS). 배포·제출 브랜치는 **day2-deploy**다. main과 default에는 앱 소스를 넣지 않는다.

## Render 세 앱

Render Hobby 워크스페이스에서 각 앱을 **Free Docker Web Service**로 준비한다. 무료 한도·가입 문제가 있으면 상태를 남기며 결제·유료 전환을 요구하지 않는다.

| 앱 | Root Directory | Dockerfile Path | Docker Build Context | Health Check Path | Branch |
| --- | --- | --- | --- | --- | --- |
| 일반 · mini-general | general | ./Dockerfile | . | /health | day2-deploy |
| 감시 API · mini-monitor | monitor/backend | ./Dockerfile | . | /health | day2-deploy |
| 감시 화면 · mini-monitor-web | monitor/next-frontend | ./Dockerfile | . | / | day2-deploy |

공통: Runtime Docker, Docker Command 빈칸, Auto-Deploy **On Commit**, Instance Type **Free**. 앱 Root Directory 안에서 Dockerfile과 context를 사용한다. Dockerfile의 CMD가 시작 명령이며 Render PORT를 따른다.

두 Flask는 `waitress-serve --listen=0.0.0.0:${PORT:-5000} app:app`이며 python app.py 개발 실행도 같은 전역 app을 사용한다. 둘 다 앱 생성에서 Sentry 초기화한다. 감시 backend의 기존 패키지 import는 /app/monitor/backend와 PYTHONPATH=/app으로 유지한다.

Next는 npm ci → npm run build → 빌드 결과 npm run start다. start는 0.0.0.0에서 PORT로 수신한다. MONITOR_API_URL을 요청 시에만 읽으므로 이미지 빌드에는 API·DB가 필요 없다. Compose·Nginx는 로컬용이고 Render는 세 Dockerfile로 각각 배포한다.

## 두 Supabase 저장소

| 설정 | 일반 DB | 감시 DB |
| --- | --- | --- |
| 프로젝트 | 일반용 수업 샘플 재사용 또는 일반용 Free 프로젝트 | 별도 감시용 Free 프로젝트 |
| SQL | general/sql/deploy.sql | monitor/backend/sql/deploy.sql |
| 테이블 | users, posts | users, http_events, notes |
| DB_HOST·DB_USER | 일반 프로젝트 Session pooler Host·User | 감시 프로젝트 Session pooler Host·User |
| DB_PORT·DB_NAME·DB_SSLMODE | 5432 · postgres · require | 5432 · postgres · require |

각 프로젝트의 Connect → **Session pooler**에서 Host와 User(postgres.PROJECT_REF)를 확인해 대응시킨다. 6543 Transaction pooler를 쓰지 않는다. DB 이름이 둘 다 postgres여도 별도 프로젝트의 저장소다. Data API를 비활성화하고 Flask의 psycopg로 PostgreSQL에 직접 연결한다. 이 과제에 RLS 정책을 추가하지 않는다.

각 Supabase SQL Editor에서 해당 deploy.sql을 실행한다. IF NOT EXISTS와 기존 events→http_events 이름 변경으로 자료를 보존하며 DROP·TRUNCATE·DELETE나 시퀀스 재시작을 하지 않는다. SQL 입력값은 매개변수 바인딩을 유지한다.

## 환경 변수와 주소

| 변수 | 일반 Flask | 감시 Flask | Next 서버 |
| --- | --- | --- | --- |
| DB_HOST·DB_PORT·DB_NAME·DB_USER·DB_PASSWORD·DB_SSLMODE | 일반 Supabase | 감시 Supabase | 없음 |
| SECRET_KEY | 일반용 별도 32자 이상 키 | 일반과 다른 감시 키 | 없음 |
| SESSION_COOKIE_SECURE | HTTP false, Render HTTPS true | HTTP false, Render HTTPS true | upstream 쿠키 전달 |
| EVENT_TOKEN | 감시와 동일한 32자 이상 값 | 일반과 동일한 값 | 없음 |
| MONITOR_URL | 감시 Flask HTTPS URL + /api/events | 없음 | 없음 |
| MONITOR_API_URL | 없음 | 없음 | 감시 Flask HTTPS 기준 URL |
| SENTRY_DSN | 일반 Sentry 프로젝트, 예시 빈칸 | 감시 Sentry 프로젝트, 예시 빈칸 | 없음 |
| SENTRY_ENVIRONMENT | mini-general | mini-monitor | 없음 |
| APP_VERSION | 배포 커밋 또는 day2-v1 | 배포 커밋 또는 day2-v1 | 없음 |
| ENABLE_SENTRY_TEST | 최종 false | 해당 경로 없음 | 없음 |
| PORT | Render 제공 | Render 제공 | Render 제공 |

각 앱의 .env.example은 비밀값 없는 자리표시자다. Flask는 자체 .env를 interpolate=False로 읽어 비밀번호의 $ 등을 치환하지 않는다. Render에서는 Dashboard의 환경 변수에 직접 설정한다. 실제 .env는 Git·Docker build에서 제외한다. DB 비밀번호·세션 키·토큰은 NEXT_PUBLIC_*나 브라우저에 넣지 않는다.

키·토큰은 `python -c "import secrets; print(secrets.token_urlsafe(48))"`로 생성해 개인 설정에만 저장한다. 일반/감시 키는 다르게, EVENT_TOKEN만 같게 설정한다. Sentry Developer 무료 범위로 준비하고 실제 DSN은 제출하지 않는다.

## 계정 준비 — 각 Flask의 로컬 가상환경

먼저 SQL과 각 .env를 준비한다. .env.example을 .env로 복사한 후 Host·User 자리표시자와 빈 비밀값을 채운다. 기존 .env가 있으면 덮어쓰지 않는다.

```cmd
cd /d D:\ALEPH_Codemit\mini-watch-cloud\general
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe create_user.py --username student --name "학생"
cd /d D:\ALEPH_Codemit\mini-watch-cloud\monitor\backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe create_user.py --username operator --name "운영자"
```

비밀번호를 두 번 입력하며 해당 DB users에 해시만 저장한다. 기존 같은 계정은 변경하지 않는다. 자동화의 ACCOUNT_PASSWORD도 프로세스 환경에서만 전달한다. 실제 로그인 비밀번호를 과제 문서에 적지 않는다.

## 배포·재확인 순서

1. 일반·감시 Supabase에 SQL·계정을 각각 준비한다.
2. 감시 Flask를 먼저 배포하고 /health를 확인한다. 200은 HTTP 생존이며 DB 인증 증거가 아니다.
3. 그 Flask HTTPS 주소를 일반 MONITOR_URL과 Next MONITOR_API_URL에 역할대로 넣고 EVENT_TOKEN·Secure 쿠키를 확인한다.
4. 일반·Next를 배포한다. 본인 계정으로 로그인하고 실패/성공 기록, 게시글·메모 등록/수정·새로고침 조회 및 DB 행을 확인한다.
5. 실습 오류 경로는 로그인 조건 안에서 잠시 켜고 수정 후 정상 JSON을 확인한 뒤 false로 끈다.
6. 테스트·커밋·push 후 Render 배포 커밋과 APP_VERSION을 확인한다. 재배포 후 기존 게시글·메모를 다시 조회한다.

감시 주소 오류는 Next의 502/503·화면 안내, DB 오류는 해당 Flask의 503·로그, 입력 오류는 400·fields로 구분한다. 감시 연결을 복구한 뒤 새 로그인 실험을 만든다. Sentry Resolve는 코드 수정·배포를 대신하지 않는다. 구체적 코드 경로·재시도는 README에 있다.

## 진행 상태 — 2026-10-13

| 항목 | 상태 |
| --- | --- |
| 세 앱 배포 코드·Dockerfile·예시·SQL | 구현 완료 |
| 개발/Waitress·Next production build·프록시 | 로컬 검증 완료, 아래 확인 범위 참고 |
| 실제 Render 서비스·배포 URL | 미배포, 주소 없음 |
| 실제 Supabase 두 프로젝트 연결 | 미연결, 개인 연결값 미입력 |
| 실제 Sentry DSN·화면 수신 | 미연결·미검증, 예시 DSN 빈칸 |

로컬 PostgreSQL/Docker 검증은 클라우드 배포 완료를 의미하지 않는다. 가입·무료 한도도 확인하지 않았으며 결제나 유료 전환은 하지 않았다.

확인한 로컬 범위: Python **9 passed**, Next lint·production build 통과, 실제 컨테이너 브라우저/프록시 **4 passed (3.7s)**. Cookie·CSRF·여러 Set-Cookie·상태 전달, 서버 이벤트 토큰, 게시글/메모 CRUD, 공백 400·CSRF 403·없는 자료 404, 새로고침 조회를 확인했다. API·DB가 없는 이미지 빌드도 성공했고 두 Flask 컨테이너가 실제 Waitress로 실행된다. down/up 후 저장 기록·메모가 유지되는 것도 확인했다.

기존 Day1 서비스를 건드리지 않도록 이번 로컬 검증만 별도 m5d2-general/m5d2-monitor 프로젝트와 m5d2-events, 8181/8182 포트로 분리했다. 제출 Compose의 기본값은 기존 m5d1 이름과 8081/8082다. 앱 소스·Dockerfile·네트워크 역할은 같고 검증용 경로/포트 설정과 실제 비밀값은 캐시에만 두어 제출에서 제외했다.

연결·재현 커밋 e3d22b33092826d7d3aa9ec27d4bcbbc29e2605b, 오류 수정 커밋 8c29e2e71fcc2101dcdf7c5984792fc5f3214904. 수정 파일·함수·원인·효과와 diff는 README에 포함한다.

통합 검증·배포 문서 커밋: e56006d09baf05178dc42b2f353de59d48eb71a9. 기존 과제용 공개 기본 키·비밀번호 대신 개인 로컬 설정을 필수로 요구하도록 보완한 커밋: 8b5276b. 모든 작업은 로컬 수정·검증·커밋 후 day2-deploy로 push했다.

참고: [Render Docker 설정](https://render.com/docs/blueprint-spec), [Supabase PostgreSQL 연결](https://supabase.com/docs/guides/database/connecting-to-postgres), [Waitress 실행](https://docs.pylonsproject.org/projects/waitress/en/stable/usage.html), [Sentry 설정](https://docs.sentry.io/platforms/python/configuration/options/).
