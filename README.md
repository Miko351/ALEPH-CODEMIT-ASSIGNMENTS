# 일반·감시 미니프로젝트를 두 Compose로 실행하기

작업 폴더: `D:\ALEPH_Codemit\mini-watch-compose`

제출 브랜치: [mini-watch-compose](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/tree/mini-watch-compose)

이전 과제의 `monitor-dashboard/general`, `monitor-dashboard/monitor/backend`, `nextjs-notes/next-practice/mini-watch/monitor/next-frontend`를 이어서 사용했다. 강사 완성본을 복제하지 않았다. 과제 기준의 general, monitor/backend, monitor/next-frontend 폴더와 서비스 이름을 사용하며 각 Flask 내부 포트는 5000, Next.js 내부 포트는 3000으로 맞췄다. 기존 과제 폴더는 변경하지 않았다.

직접 완성한 파일은 두 Compose, 세 Dockerfile·.dockerignore, gateways 설정, 두 docker-init.sql, 계정 준비 도구와 README다. 일반 앱에 해시 기반 로그인·세션·게시글 접근 제한을 추가했다. 로그인 성공·실패의 event_kind를 감시에 전송·저장·조회하고 Next.js 요청 기록 표에 표시하도록 기존 코드도 연결했다. 감시 메모 CRUD·처리 상태·로그인 세션은 이어서 사용한다. API 함수, 화면 컴포넌트, Flask 라우터, SQL 저장소를 구분했다.

## 첫 실행 — Windows CMD

Docker Desktop의 Linux containers와 Docker Compose가 필요하다. 별도의 로컬 Python·Next 개발 서버를 켤 필요는 없다. 설정 예시에는 이 과제 전용 공개 실습값만 있으며 실제 서비스의 비밀번호나 토큰은 포함하지 않는다.

```cmd
cd /d D:\ALEPH_Codemit\mini-watch-compose
copy .env.example .env
docker network create m5d1-events
docker compose -f compose-general.yaml config --quiet
docker compose -f compose-monitor.yaml config --quiet
docker compose -f compose-monitor.yaml up -d --build
docker compose -f compose-monitor.yaml ps
curl -i http://localhost:8082/api/auth/me
```

공유 망은 처음에 한 번 만든다. 이미 있으면 `docker network inspect m5d1-events`로 확인하고 생성 단계를 건너뛴다. 두 YAML을 한 명령에 합치지 않는다. `name:`이 각각 m5d1-general, m5d1-monitor이므로 같은 폴더에서 실행해도 별도 프로젝트다.

감시 `/api/auth/me`가 **HTTP 200**을 반환할 때까지 기다린다. 로그인 전에는 `{"user":null}`이며 이 경로는 DB 연결도 확인한다. 기록·메모 API는 여전히 로그인 없이 호출하면 401이다. 이후 계정과 일반 프로젝트를 준비한다.

```cmd
docker compose -f compose-monitor.yaml exec monitor-api python create_user.py
docker compose -f compose-general.yaml up -d --build
docker compose -f compose-general.yaml exec general-api python create_user.py
docker compose -f compose-general.yaml ps
docker compose -f compose-general.yaml logs --tail=50 general-api
docker compose -f compose-monitor.yaml logs --tail=50 monitor-api monitor-web
```

| 서비스 | 접속 | 실습 계정 |
| --- | --- | --- |
| 일반 게시판 | http://localhost:8081 | student / Learn123! |
| 감시 대시보드·메모 | http://localhost:8082 | operator / Learn123! |

create_user.py는 비밀번호의 해시만 DB에 저장한다. 이미 같은 계정이 있으면 비밀번호를 바꾸지 않는다. 별도 실습 비밀번호를 사용할 경우 `docker compose -f compose-general.yaml exec -e PRACTICE_PASSWORD=YOUR_PRACTICE_PASSWORD general-api python create_user.py --username another`처럼 다른 계정을 만든다. 비밀번호를 Git 문서에 기록하지 않는다.

## 화면에서 확인하기

1. 일반 8081의 로그인 화면에서 student와 틀린 비밀번호를 입력한다. 오류 안내와 401이 발생한다.
2. student / Learn123!로 다시 로그인한다. 200 응답 뒤 게시글 목록으로 이동한다. 세션 없이 게시글 주소를 열면 로그인 화면으로 이동한다. 목록·상세·작성·수정·삭제 화면은 기존 링크와 버튼으로 연결된다.
3. 감시 8082에서 operator / Learn123!로 로그인하고 **기록 불러오기**를 누른다. `/auth/login`의 login_failure·401과 login_success·200을 확인한다. 표에는 종류·메서드·경로·상태·시각이 표시된다. 검색 칸에 login_failure, 401 또는 경로를 입력해 필터링할 수 있다.
4. 관찰 메모 제목 **Docker 점검**, 내용 **로그인 실패와 성공을 확인했다**를 입력해 DB 저장한다. 목록에서 상세를 확인하고 브라우저 새로고침 후 **새로고침**으로 같은 메모를 다시 조회한다. `/notes` 링크에서도 같은 DB 메모를 사용한다.
5. 수정·삭제는 대상 ID만 처리한다. 수정·삭제 취소는 데이터를 유지한다. 빈 제목·내용은 서버에서 400, 없는 ID는 404이며 화면에서 오류를 안내한다.

MONITOR_URL은 컨테이너 내부의 `http://monitor-api:5000/api/events`다. 일반 요청의 after_request에서 requests.post로 메타데이터를 보내고 감시 collector가 PostgreSQL에 커밋한다. 비밀번호·폼 본문·쿼리 문자열은 기록하지 않는다. 기록 전송에 실패하면 일반 서비스는 계속 응답하지만 해당 기록을 나중에 재전송하지 않으므로, 감시를 먼저 준비하고 실패·성공 실험을 새로 진행한다.

## 데이터 보존과 종료·재실행

```cmd
docker compose -f compose-general.yaml down
docker compose -f compose-monitor.yaml down
docker compose -f compose-monitor.yaml up -d
curl -i http://localhost:8082/api/auth/me
docker compose -f compose-general.yaml up -d
```

다시 로그인해 이전 기록과 Docker 점검 메모를 불러온다. 일반 DB의 m5d1-general_general-data, 감시 DB의 m5d1-monitor_monitor-data named volume은 각각 PostgreSQL 17의 실제 저장 경로 `/var/lib/postgresql/data`에 연결되어 있다. 위 down은 볼륨을 보존한다. **자료를 유지하려면 down에 -v를 붙이지 않는다.** 초기 SQL은 빈 DB 볼륨의 첫 시작에 실행된다. SQL을 수정한 뒤 기존 볼륨을 재시작하는 것만으로는 새 SQL이 적용되지 않는다. 데이터 삭제 대신 필요한 ALTER 등 별도 마이그레이션을 실행한다.

## 서비스·망·포트 구성

| 서비스 | 참여하는 망 | 내부 포트 | PC 공개 포트 |
| --- | --- | --- | --- |
| general-gateway | 일반 web | 80 | 8081 |
| general-api | 일반 web, 일반 data, m5d1-events | 5000 | 없음 |
| general-db | 일반 data | 5432 | 없음 |
| monitor-gateway | 감시 web | 80 | 8082 |
| monitor-web | 감시 web | 3000 | 없음 |
| monitor-api | 감시 web, 감시 data, m5d1-events | 5000 | 없음 |
| monitor-db | 감시 data | 5432 | 없음 |

일반·감시 web/data는 프로젝트별 망이며 `internal: true`다. DB는 자기 data 망에만 참여한다. 각 API의 DB_HOST는 자기 DB 서비스 이름이고 포트·DB 이름·계정·비밀번호는 자기 DB 설정과 일치한다. DB 연결은 psycopg, SQL 입력은 매개변수 바인딩을 사용한다. general/sql/docker-init.sql에 posts·users가, monitor/backend/sql/docker-init.sql에 users·events·notes·처리 상태·event_kind가 준비된다.

두 API만 events 공유 망에 참여하며 두 파일 모두 `external: true`, 실제 `name: m5d1-events`를 선언한다. YAML 안의 같은 별칭(events)만 쓰면 기본적으로 프로젝트마다 별도 망이 생긴다. 같은 실제 외부 망을 지정하고 서비스 networks에도 참여시켜야 서로의 서비스 이름으로 연결할 수 있다. 다른 Compose의 서비스는 depends_on에 넣지 않았다.

일반 gateway는 모든 경로를 general-api:5000으로 전달한다. 감시 gateway는 `/api/`를 monitor-api:5000으로 전달하고 나머지 화면·정적 자원을 monitor-web:3000으로 전달한다. proxy_pass에 경로를 덧붙이지 않아 `/api` 접두사를 유지한다. Next.js 브라우저의 fetch는 상대 `/api/...`를 사용하며 localhost나 PC 공개 포트를 컨테이너 간 주소로 사용하지 않는다. 로그인 쿠키는 화면과 같은 origin으로 전달된다. 일반·감시 쿠키 이름도 다르다.

## 설정·실행·연결 점검

```cmd
docker compose -f compose-general.yaml config --quiet
docker compose -f compose-monitor.yaml config --quiet
docker compose -f compose-general.yaml ps
docker compose -f compose-monitor.yaml ps
docker network inspect m5d1-events
docker compose -f compose-general.yaml exec general-api getent hosts monitor-api
docker compose -f compose-general.yaml logs --tail=100 general-api
docker compose -f compose-monitor.yaml logs --tail=100 monitor-api
```

config는 YAML·변수·서비스 참조의 유효성, ps는 컨테이너 실행과 DB/API/Next.js 건강 상태, inspect는 공유 망에 두 API만 참여했는지, getent는 감시 API 이름이 IP로 해석되는지 확인한다. 이름 조회 성공은 HTTP 처리·DB 인증·SQL 성공을 보장하지 않는다. `/api/auth/me`의 200은 감시 HTTP·DB 준비를 확인하며, 실제 로그인 실험 후 기록 불러오기는 전송·수신·DB 저장·조회·화면 표시까지 확인한다. 로그에서 DB 접속 오류나 전송 실패를 확인한다.

Docker 설정 개선으로 monitor-web에 Node.js fetch 기반 HTTP healthcheck를 추가하고 monitor-gateway가 service_healthy를 기다리도록 변경했다. 단순히 프로세스가 시작된 시점에 gateway를 여는 대신 Next.js가 실제 200 응답을 반환한 뒤 시작한다. 이 개선의 diff와 PR 이력은 아래 Git 기록에 남긴다.

## 심화: 공유 망 분리와 복구

PowerShell에서는 실행 중인 일반 API ID를 변수로 받아 다음과 같이 실험한다.

```powershell
$generalApiId = docker compose -f compose-general.yaml ps -q general-api
docker network disconnect m5d1-events $generalApiId
docker compose -f compose-general.yaml exec general-api getent hosts monitor-api
docker network connect --alias general-api m5d1-events $generalApiId
docker compose -f compose-general.yaml exec general-api getent hosts monitor-api
docker network inspect m5d1-events
```

분리하면 monitor-api와 공통 망이 없어 이름 조회·기록 전달이 실패하지만 자기 DB·gateway 망은 유지된다. 복구 뒤 IP 조회와 새 로그인 실패·성공을 확인한다. 끊긴 동안의 기록은 자동 재전송되지 않는다. 최종 Compose는 두 API를 공유 망에 참여시키는 상태로 유지한다. 이미 분리된 경우 disconnect를 반복하지 않는다.

## 심화: restart와 rebuild

Flask Dockerfile은 COPY로 소스를 이미지에 넣는다. Compose에는 앱 소스를 덮어쓰는 bind mount가 없으며 SQL·gateway 설정만 읽기 전용 bind mount, DB만 named volume이다. 따라서 로컬 Python 수정 후 restart만 하면 이전 이미지의 소스로 다시 실행된다. 다음 명령으로 변경 소스를 이미지·컨테이너에 반영한다.

```cmd
docker compose -f compose-general.yaml up -d --build general-api
docker compose -f compose-monitor.yaml up -d --build monitor-api
docker compose -f compose-monitor.yaml up -d --build monitor-web
```

Next Dockerfile은 npm ci → npm run build → 개발 의존성 제거 후 빌드 결과를 복사하며 npm run start로 0.0.0.0:3000에서 실행한다. Next 소스 수정도 rebuild가 필요하다. Nginx의 읽기 전용 설정 파일을 수정했다면 해당 gateway를 restart하여 설정을 다시 읽는다. DB 볼륨은 위 이미지 재빌드로 삭제되지 않는다.

## 심화: DB 망 분리

```cmd
docker compose -f compose-general.yaml exec general-api getent hosts general-db
docker compose -f compose-general.yaml exec general-api getent hosts monitor-db
docker compose -f compose-general.yaml exec general-api python -c "from app import create_app; from db import connect_db; app=create_app(); app.app_context().push(); print(connect_db().execute('SELECT 1').fetchone())"
```

general-db는 같은 일반 data 망에 있으므로 이름 조회가 된다. monitor-db는 감시 data 망에만 있으므로 일반 API에서 조회되지 않는 것이 예상된다. 두 DB를 공유 망에 넣지 않는다. 이름 조회는 DNS 단계, DB 계정·비밀번호 확인은 PostgreSQL 인증 단계, SELECT 1은 실제 SQL 실행 단계다. IP를 안다고 DB 접근 권한까지 생기지 않는다.

## 로컬 검증과 Git 제출

현재 PC에는 Docker가 없어 사용자가 직접 설치하기로 했다. 따라서 Docker build/up, config --quiet, gateway 동작, 공유 망 DNS, down/up 볼륨 보존은 **아직 실제 실행하지 않았다**. 위 명령은 Docker 설치 후 수행할 절차다. 이 문서는 컨테이너 실행 완료를 주장하지 않는다.

로컬에서는 Next.js lint·production build를 통과했고, PyYAML 설정 검사·Python 문법·빌드 경로 검사 및 별도 PostgreSQL 테스트 DB에서 로그인·기록 저장·메모 CRUD·Flask 앱 재생성 후 데이터 조회 테스트 3개를 통과했다. 해당 테스트의 기록 전송은 Flask 테스트 클라이언트로 collector에 전달하며 Docker 네트워크 전송 검증을 대신하지 않는다. 기존 과제 DB 자료는 변경하지 않았다.

```cmd
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pytest tests -q --basetemp .cache\pytest-local
cd monitor\next-frontend
npm ci
npm run lint
npm run build
```

PostgreSQL 통합 테스트는 CREATE DATABASE 권한이 있는 실습 서버의 TEST_ADMIN_DSN 환경 변수가 필요하며 없으면 해당 테스트만 skip한다. 임의 접미사의 새 테스트 DB 두 개만 생성하며 기존 DB는 수정하지 않는다. 생성한 테스트 DB는 조회 확인을 위해 보존한다. 실제 접속 비밀번호가 든 환경 변수나 .env는 Git에서 제외한다.

Docker 적용 커밋과 개선 PR은 아래 Git 기록 절에 식별자·변경 내용을 남긴다. 모든 파일은 로컬 작성·검증·커밋 후 같은 저장소의 mini-watch-compose 브랜치에 업로드한다. main과 파일 없는 default에는 앱 소스를 넣지 않는다.

ZIP은 scripts/package.py로 생성하며 소스·Compose·Dockerfile·.dockerignore·SQL·설정 예시·requirements·package-lock·README·테스트를 포함한다. .env·DB 데이터·가상환경·node_modules·.next·캐시·.git는 제외한다.

참고: [Docker Compose 네트워크](https://docs.docker.com/compose/how-tos/networking/), [건강 상태와 시작 순서](https://docs.docker.com/compose/how-tos/startup-order/), [Docker volumes](https://docs.docker.com/reference/compose-file/volumes/), [Next.js Docker 배포](https://nextjs.org/docs/app/getting-started/deploying).

## Git 적용 커밋·개선 PR 기록

- Docker 기본 구현: `ecac6097db9db4b6377dc7bf875607320086f69d` — 두 Compose, Dockerfile·Nginx·SQL·DB 볼륨·로그인 기록·감시 화면과 실행 안내를 추가.
- 개선 작업 브랜치: `feature/compose-web-health`. 로컬 수정·배포 계약 테스트 후 커밋·push.
- 개선 커밋: `46eeb82bf7f8cfbd3f6fbc785448ae621156a409` — Next.js HTTP healthcheck와 gateway 준비 대기를 추가. 변경 파일: compose-monitor.yaml, tests/test_deployment.py, README.md.
- PR: [https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/7](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/pull/7). base=`mini-watch-compose`, 상태 `MERGED`, 병합 시각 `2026-10-13T03:56:45Z`.
- merge commit: `49503741dcc4b3825e933cf52be392b2cc639cda`. 부모 2개인 merge commit으로 병합했다. 로컬 mini-watch-compose에서 pull --ff-only 후 완료한 개선 브랜치를 로컬·원격에서 삭제.

실제 PR diff를 읽어 확인한 검토 내용은 PR 본문에도 남겼다. 아래는 해당 본문이다. 외부 리뷰어의 승인이라고 주장하지 않고 작성자가 변경 내용을 점검한 기록이다.

```text
감시 gateway가 Next.js 프로세스 생성 직후 시작하면 HTTP 준비 전에 일시적인 502가 발생할 수 있습니다. monitor-web에 Node.js fetch 기반 HTTP healthcheck를 추가하고 monitor-gateway의 의존 조건을 service_healthy로 변경했습니다.

직접 diff 검토: 상태 확인은 monitor-web 컨테이너 자신의 127.0.0.1:3000을 대상으로 하며 컨테이너 간 주소에는 기존 서비스 이름을 유지합니다. 추가 도구 설치 없이 기본 Node.js로 검사합니다. DB·외부 공유 망·공개 포트·볼륨 설정은 변경하지 않습니다. README 설명과 배포 계약 테스트를 함께 갱신했습니다.

검증: tests/test_deployment.py 2 passed. 기존 앱의 Next.js lint/build 및 PostgreSQL 앱 테스트 3개 통과. 이 PC에는 Docker가 없어 사용자가 설치를 맡았으며 실제 Docker build/up과 컨테이너 HTTP healthcheck는 아직 실행하지 않았습니다.
```

ZIP에서도 개선 내용을 확인하도록 실제 개선 커밋의 diff를 아래에 포함한다. 출력 끝 공백만 제거했다.

```diff
diff --git a/README.md b/README.md
index 7300873..97e81c4 100644
--- a/README.md
+++ b/README.md
@@ -96,7 +96,9 @@ docker compose -f compose-general.yaml logs --tail=100 general-api
 docker compose -f compose-monitor.yaml logs --tail=100 monitor-api
 ```

-config는 YAML·변수·서비스 참조의 유효성, ps는 컨테이너 실행과 DB/API 건강 상태, inspect는 공유 망에 두 API만 참여했는지, getent는 감시 API 이름이 IP로 해석되는지 확인한다. 이름 조회 성공은 HTTP 처리·DB 인증·SQL 성공을 보장하지 않는다. `/api/auth/me`의 200은 감시 HTTP·DB 준비를 확인하며, 실제 로그인 실험 후 기록 불러오기는 전송·수신·DB 저장·조회·화면 표시까지 확인한다. 로그에서 DB 접속 오류나 전송 실패를 확인한다.
+config는 YAML·변수·서비스 참조의 유효성, ps는 컨테이너 실행과 DB/API/Next.js 건강 상태, inspect는 공유 망에 두 API만 참여했는지, getent는 감시 API 이름이 IP로 해석되는지 확인한다. 이름 조회 성공은 HTTP 처리·DB 인증·SQL 성공을 보장하지 않는다. `/api/auth/me`의 200은 감시 HTTP·DB 준비를 확인하며, 실제 로그인 실험 후 기록 불러오기는 전송·수신·DB 저장·조회·화면 표시까지 확인한다. 로그에서 DB 접속 오류나 전송 실패를 확인한다.
+
+Docker 설정 개선으로 monitor-web에 Node.js fetch 기반 HTTP healthcheck를 추가하고 monitor-gateway가 service_healthy를 기다리도록 변경했다. 단순히 프로세스가 시작된 시점에 gateway를 여는 대신 Next.js가 실제 200 응답을 반환한 뒤 시작한다. 이 개선의 diff와 PR 이력은 아래 Git 기록에 남긴다.

 ## 심화: 공유 망 분리와 복구

diff --git a/compose-monitor.yaml b/compose-monitor.yaml
index 9340e1d..abe7f9c 100644
--- a/compose-monitor.yaml
+++ b/compose-monitor.yaml
@@ -42,6 +42,12 @@ services:
     environment:
       NODE_ENV: production
       NEXT_TELEMETRY_DISABLED: "1"
+    healthcheck:
+      test: [CMD, node, -e, "fetch('http://127.0.0.1:3000').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]
+      interval: 5s
+      timeout: 3s
+      retries: 20
+      start_period: 10s
     networks: [monitor-web]
     restart: unless-stopped
   monitor-gateway:
@@ -53,7 +59,7 @@ services:
       monitor-api:
         condition: service_healthy
       monitor-web:
-        condition: service_started
+        condition: service_healthy
     networks: [monitor-web]
     restart: unless-stopped
 volumes:
diff --git a/tests/test_deployment.py b/tests/test_deployment.py
index 45b1a49..592c668 100644
--- a/tests/test_deployment.py
+++ b/tests/test_deployment.py
@@ -45,6 +45,9 @@ def test_compose_isolation_and_persistence():
         assert (ROOT / sql_mount.split(':')[0]).is_file()
     general = yaml.safe_load((ROOT / 'compose-general.yaml').read_text())
     assert general['services']['general-api']['environment']['MONITOR_URL'] == 'http://monitor-api:5000/api/events'
+    monitor = yaml.safe_load((ROOT / 'compose-monitor.yaml').read_text())
+    assert monitor['services']['monitor-gateway']['depends_on']['monitor-web']['condition'] == 'service_healthy'
+    assert monitor['services']['monitor-web']['healthcheck']['test'][:2] == ['CMD', 'node']


 def test_build_commands_and_gateway_routes():
```
