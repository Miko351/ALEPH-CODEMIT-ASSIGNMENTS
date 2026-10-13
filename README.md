# 미니프로젝트 클라우드 배포·오류 수집 적용

작업 폴더: `D:\ALEPH_Codemit\mini-watch-cloud`

제출 브랜치: [day2-deploy](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/tree/day2-deploy)

세 앱의 배포 설정·DB 준비·환경 변수·계정 준비·진행 상태는 [deployment-plan.md](deployment-plan.md)에 있다. 실제 Render·Supabase·Sentry 배포·접속·수신은 **미완료**이며 완료했다고 기록하지 않는다.

## 시작 코드와 변경

이전 mini-watch-compose의 최종 커밋 774b2a69294caa27592dea421e6de2c60e196de3을 별도 폴더에 clone해 작업했다. 기존 과제 폴더·DB는 유지했다. 일반 Flask는 로그인·세션·게시글 CRUD, 감시 Flask는 로그인·기록·메모 DB API, 감시 Next.js는 기록 표·메모 CRUD 화면을 담당한다.

수업 day07-cloud-materials 지원 자료에서 observability.py와 Next Route Handler만 필요한 위치에 적용했다. 기존 앱 전체를 지원 자료로 덮어쓰지 않았다. 다음 파일을 직접 연결·수정했다.

| 파일 | 적용 내용 |
| --- | --- |
| 두 app.py·Dockerfile·requirements.txt | 개발 python app.py와 같은 app:app의 Waitress 배포 실행, PORT, 독립 /health |
| 각 db.py·.env.example·sql/deploy.sql | DB_* 여섯 변수·SSL·일반/감시 별도 스키마 |
| 각 create_user.py | 비밀번호 입력·해시 저장, 기존 계정 보존 |
| request_logging.py·감시 events 라우터/저장소 | X-Event-Token 검사, HTTPS 주소, http_events 저장 |
| 감시 auth_helpers.py·authentication.py·auth 라우터 | 세션·CSRF 발급/검사 |
| Next app/api/[...path]/route.js·api/ | 서버 프록시, Cookie/CSRF/Set-Cookie/상태 전달, 오류 안내·재시도 |
| 각 observability.py·general/app.py:sentry_test | Sentry 초기화·정보 제외, 나눗셈 오류 수정 |
| Compose·gateway | 기존 로컬 실행 유지, /api도 Next 서버를 통과하도록 연결 |

## 요청·데이터 흐름

감시 브라우저 → 같은 사이트 `/api/...` → Next Route Handler → MONITOR_API_URL의 감시 Flask → 감시 DB. 일반 브라우저 → 일반 Flask → 일반 DB. 일반의 요청 기록은 서버의 MONITOR_URL과 X-Event-Token으로 감시 Flask → http_events에 저장된다.

일반 MONITOR_URL은 **감시 Flask HTTPS 주소 + /api/events**, Next MONITOR_API_URL은 **감시 Flask HTTPS 기준 주소**다. 두 값에 감시 화면 주소를 넣지 않는다. DB 비밀번호·SECRET_KEY·EVENT_TOKEN은 Flask 서버에만 설정하고 브라우저나 NEXT_PUBLIC_*에 넣지 않는다.

프록시는 요청 시에만 fetch하므로 API·DB 없이 npm run build가 성공한다. 요청 Cookie·X-CSRF-Token, 응답의 여러 Set-Cookie와 HTTP 상태를 유지한다. 브라우저의 이벤트 수신 POST는 차단하며 일반 서버가 감시로 직접 전송한다. 로그인 실패는 login_failure/401, 성공은 login_success/200이다. 기존 게시글·메모 CRUD·취소·오류 안내·새로고침 조회를 유지하고 DB에 커밋한다. 메모 처리 상태도 DB에 저장한다.

## 로컬 Compose 실행

Render에는 각 앱 Dockerfile로 배포하며, 두 Compose와 Nginx는 로컬 실행용이다.

```cmd
cd /d D:\ALEPH_Codemit\mini-watch-cloud
python scripts\configure_local.py
docker network create m5d1-events
docker compose -f compose-general.yaml config --quiet
docker compose -f compose-monitor.yaml config --quiet
docker compose -f compose-monitor.yaml up -d --build
curl -i http://localhost:8082/api/auth/me
docker compose -f compose-monitor.yaml exec monitor-api python create_user.py
docker compose -f compose-general.yaml up -d --build
docker compose -f compose-general.yaml exec general-api python create_user.py
```

감시 gateway는 Next에 연결되어 있으므로 감시 Flask의 /health 직접 확인은 `docker compose -f compose-monitor.yaml exec monitor-api python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').status)"`로 한다. 화면 gateway의 `/api/auth/me`도 확인한다. 계정 비밀번호는 직접 입력하고 문서에 기록하지 않는다.

공유 망이 있으면 생성 단계를 건너뛴다. 이전 m5d1 프로젝트가 실행 중이면 이전 폴더에서 먼저 down한다. **-v는 사용하지 않는다.** 기존 DB 볼륨을 사용할 때 DB 비밀번호는 기존 값을 유지한다. 새 설정 파일 생성이 기존 DB 계정의 비밀번호를 바꾸지는 않는다. 기존 감시 DB에는 API 시작 전 다음 마이그레이션을 적용한다.

```cmd
docker compose -f compose-monitor.yaml up -d monitor-db
docker compose -f compose-monitor.yaml exec -T monitor-db psql -U monitor -d monitor < monitor\backend\sql\deploy.sql
```

deploy.sql은 기존 events가 있고 http_events가 없으면 행을 삭제하지 않고 이름을 변경한다. 이어 IF NOT EXISTS로 필요한 테이블·열을 준비한다. 일반 SQL도 posts·users를 지우거나 번호를 초기화하지 않는다. 빈 로컬 DB는 docker-init.sql로 준비된다.

접속은 일반 http://localhost:8081, 감시 http://localhost:8082다. 공개 포트는 두 gateway뿐이다. web은 프로젝트별 bridge, data는 DB 격리 망이며 두 API만 external m5d1-events에 참여한다. 다음 명령으로 상태·로그·DNS를 확인하고 각각 종료한다.

```cmd
docker compose -f compose-general.yaml ps
docker compose -f compose-monitor.yaml ps
docker compose -f compose-general.yaml logs --tail=50 general-api
docker compose -f compose-monitor.yaml logs --tail=50 monitor-api monitor-web
docker network inspect m5d1-events
docker compose -f compose-general.yaml exec general-api getent hosts monitor-api
docker compose -f compose-general.yaml down
docker compose -f compose-monitor.yaml down
```

down은 named volume을 유지한다. 다시 감시→일반 순서로 up하고 로그인해 자료를 조회한다. Supabase 배포에서는 외부 DB에 자료가 남으며 Render 이미지 재배포가 DB를 초기화하지 않는다.

## 오류 수집과 수정

두 앱 생성 시 observability.configure_errors를 호출하므로 개발·Waitress 실행 모두 적용된다. SENTRY_DSN이 비면 전송을 시작하지 않는다. SENTRY_ENVIRONMENT·APP_VERSION을 읽고 service 태그를 mini-general·mini-monitor로 구분한다.

send_default_pii=False, include_local_variables=False, max_request_body_size='never', traces_sample_rate=0.0을 유지한다. before_send의 remove_request_secrets는 request의 data·cookies·headers·query_string과 event의 user를 제거한다. 로그인 본문·세션 쿠키·인증 헤더·사용자 정보를 오류 자료에서 제외한다.

수정 파일·함수: **general/app.py의 sentry_test**. 원인은 `1 / 0`의 ZeroDivisionError이며 `result = 1`로 바꿔 정상 JSON `{"result":1}`을 반환한다. ENABLE_SENTRY_TEST=false이면 404, 켰지만 로그인하지 않으면 401, 켜고 로그인하면 수정 후 200이다. 로그인·게시글·오류 수집 코드는 유지한다.

- 재현·연결 커밋: `e3d22b33092826d7d3aa9ec27d4bcbbc29e2605b`.
- 수정 커밋: `8c29e2e71fcc2101dcdf7c5984792fc5f3214904`.

로그인·활성화 조건 안에서 실제 ZeroDivisionError를 확인한 뒤 같은 요청이 200/result=1임을 테스트했다. 최종 예시와 Compose는 false다. DSN을 개인 환경에 설정하고 실습 경로를 잠시 켜서 확인한 뒤 **다시 false로 끈다**. 재현 커밋을 확인할 때는 별도 로컬 실습 환경을 사용한다. 실제 비밀번호·DSN은 제출하지 않는다. Sentry Resolve는 목록 표시 상태만 바꾸므로 코드 수정·push·재배포를 대신하지 않는다.

코드 수정 → 로컬 검증 → 커밋 → day2-deploy push → Render 배포 커밋 확인 → /health와 같은 로그인·DB 기능 재확인 순서로 진행한다. APP_VERSION을 배포 커밋으로 맞춰 코드와 오류 자료를 구분한다.

## 설정 오류 진단과 재시도

| 증상 | 확인할 설정·처리 |
| --- | --- |
| Next 502 연결 실패 | MONITOR_API_URL이 감시 Flask 주소인지, 감시 /health, Next·API 로그 |
| Next 503 주소 미설정 | Next 서버의 MONITOR_API_URL |
| DB 기능 503 | 해당 Flask DB_* 여섯 값·해당 Supabase 프로젝트·서버 DB 로그 |
| 입력 400 | 제목·본문·상태 검증 안내, 기존 행 유지 |
| 로그인 401 | 계정 준비 DB·비밀번호 해시; 수신 401이면 두 EVENT_TOKEN 비교 |
| 변경 403 | Cookie·X-CSRF-Token과 현재 로그인 응답의 csrf_token, 새로고침 후 재시도 |

/health는 HTTP 프로세스 생존 검사이며 DB에 연결하지 않는다. DB 성공은 로그인·게시글·메모 저장/조회로 별도 확인한다. 로그인하지 않은 /api/auth/me도 DB 준비 증거가 아니다. 프록시 연결 실패는 502 JSON의 안내를 화면이 표시하며 기록 불러오기·메모 새로고침으로 재요청한다. 로그인 재시도도 먼저 현재 CSRF를 다시 읽는다. 실패를 저장 성공으로 표시하지 않는다.

## 검증·제출

```cmd
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pytest tests -q --basetemp .cache\pytest-local
cd monitor\next-frontend
npm ci
npm run lint
npm run build
npx playwright test tests/proxy.spec.js
```

실제 PostgreSQL 테스트는 CREATE DATABASE 권한의 실습 서버 TEST_ADMIN_DSN이 필요하며 없으면 해당 테스트만 skip한다. 기존 DB 대신 임의 이름의 새 테스트 DB 두 개를 사용한다. Docker 화면 테스트는 TEST_ACCOUNT_PASSWORD를 프로세스 환경으로 설정한 후 npm test로 실행한다. GENERAL_BASE_URL·MONITOR_BASE_URL로 테스트 주소를 지정할 수 있다. 저장한 테스트 메모의 재시작 확인은 scripts/verify_persistence.py 또는 수동 down/up으로 수행한다.

`python scripts/package.py`는 루트 mini-watch-cloud.zip을 생성한다. 앱 소스·Docker 설정·의존성/잠금·배포 SQL·비밀값 없는 예시·README·deployment-plan·수정 diff를 포함한다. 실제 .env·비밀번호·토큰·node_modules·.next·가상환경·캐시·DB 파일·.git는 제외한다. GitHub 제출은 day2-deploy 브랜치를 선택한다.

## 오류 수정 전후 실제 diff

아래는 재현 커밋 e3d22b3과 수정 커밋 8c29e2e의 비교다. 출력 끝 공백만 제거했다. 로그인·활성화 검사와 기존 기능을 유지하면서 오류 응답 부분 및 같은 요청의 검증만 바꿨다.

```diff
diff --git a/general/app.py b/general/app.py
index 2e35eae..61036c2 100644
--- a/general/app.py
+++ b/general/app.py
@@ -60,7 +60,8 @@ def create_app(config: dict | None = None) -> Flask:
         error = api_access_error()
         if error is not None:
             return error
-        result = 1 / 0
+        # The test endpoint now reports success instead of dividing by zero.
+        result = 1
         return jsonify(result=result)

     @app.errorhandler(HTTPException)
diff --git a/tests/test_cloud.py b/tests/test_cloud.py
index bcd94b7..30e2fc4 100644
--- a/tests/test_cloud.py
+++ b/tests/test_cloud.py
@@ -22,7 +22,7 @@ def test_health_does_not_claim_database_connection():
         assert create_monitor({'TESTING': True}).test_client().get('/health').status_code == 200


-def test_sentry_test_is_gated_and_reproduces_error():
+def test_sentry_test_is_gated_and_returns_normal_json():
     assert general_app().test_client().get('/api/sentry-test').status_code == 404
     app = general_app(ENABLE_SENTRY_TEST=True)
     client = app.test_client()
@@ -30,8 +30,9 @@ def test_sentry_test_is_gated_and_reproduces_error():
     with client.session_transaction() as session:
         session['user_id'] = 1
     with patch('auth_helpers.find_user_by_id', return_value={'id': 1}):
-        with pytest.raises(ZeroDivisionError):
-            client.get('/api/sentry-test')
+        response = client.get('/api/sentry-test')
+        assert response.status_code == 200
+        assert response.json == {'result': 1}


 def test_sentry_removes_sensitive_fields_and_configures_service(monkeypatch):
```
