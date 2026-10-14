# 실제 게시판 요청으로 조회 기준과 원본 근거 확인하기

작업 폴더: `D:\ALEPH_Codemit\mini-watch-analysis`

제출 브랜치: [day3-analysis](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/tree/day3-analysis)

## 1. 구성·개념 설명

기존 mini-watch-cloud의 일반·감시 앱을 이어서 사용했다. 기존 폴더를 삭제하거나 다시 clone하지 않고 같은 Git 프로젝트의 worktree로 작업 위치만 분리했다. 계정·게시글·기록·메모·Docker 구성과 앞 과제의 보안·배포 코드를 유지했다. 새 클라우드 서비스는 만들지 않았다. deployment-plan.md는 이전 Day2 배포 참고 문서이며 이번 HTTP 분석의 실행·제출 기준은 이 README다.

| 단계 | 파일·함수와 역할 |
| --- | --- |
| 일반 응답 후 기록 | general/app.py:create_app의 `app.after_request(record_request)` |
| 출력·전송 | general/request_logging.py:record_request가 method·path·status_code·duration을 만들고 print로 stdout 출력, 별도로 requests.post로 감시 전송 |
| 수신·분류 | monitor/backend/routes/events.py:collect가 X-Event-Token을 확인하고 event_rules.py:make_event로 실제 응답 필드를 분류 |
| DB 저장 | repositories/events.py:create_event가 http_events에 INSERT. identity ID와 occurred_at DEFAULT CURRENT_TIMESTAMP는 DB 저장 과정에서 붙음 |
| 실제 캡처 | learning/capture_case.py:main이 일반 서비스에 로그인하고 실제 GET / N회·GET /training-missing 1회를 보낸 뒤 이번 ID 이후 DB 행을 읽음 |
| 정규화 | learning/normalize.py:normalize_event가 원본을 복사해 http-원본ID, source=http_live, kind=event_type을 만들고 실제 방법·경로·상태·수신시각을 보존 |
| 선택·문맥 | learning/http_rules.py:select_views와 find_following_errors |
| 관찰 구간·보고서 | learning/support.py:read_live → repositories/events.py:read_after → learning/report.py:build_report |
| API·화면 | routes/analysis.py:start/analyze와 Next components/AnalysisClient.js·api/analysis.js |

stdout JSON 출력과 HTTP POST는 서로 다른 동작이다. 터미널 출력만으로 감시 DB 저장 성공을 판단하지 않는다. 일반 MONITOR_URL은 공유 망의 `http://monitor-api:5000/api/events`이고, 두 Flask EVENT_TOKEN은 같은 개인 값이다. 일반만 토큰을 헤더로 보내고 감시가 비교한다. 토큰은 브라우저에 전달하지 않는다. 이전 로그인 실패/성공 분류도 login_failure/401·login_success/200으로 유지한다.

GET /의 200은 **post_list**, 없는 경로의 404는 **request_error**다. 분류는 입력의 임의 라벨을 신뢰하지 않고 make_event가 method·path·status_code로 정한다. 일반이 보낸 timestamp는 출력 시각이며 감시 occurred_at으로 저장하지 않는다. 새 기록의 occurred_at은 감시 DB가 수신·저장할 때 붙이는 시각이다. 기존 ID·기록 시각은 수정하지 않는다.

normalize_event는 원본 딕셔너리를 덮어쓰지 않는다. 원본 숫자 ID를 source_id에도 보존하고 `http-` 뒤 숫자로 대응시킨다. 원본에 없는 사용자·IP를 만들지 않는다. 정규화는 404를 버리지 않는다. select_views는 **GET · / · 200 · post_list** 네 조건을 전부 만족하는 행 목록을 반환하고, 횟수와 ID는 이 같은 목록에서 구한다.

판정은 `count >= threshold`다. find_following_errors는 전체 정규화 행 중 마지막 선택 조회의 수신시각과 **0 < gap <= 30초**인 404만 고른다. 조회가 없으면 오류 목록도 비운다. 이 오류는 문맥 근거로만 더한다. 통제한 12회 사례는 조회 12행과 뒤따른 404 1행이므로 **관찰값 12·근거 13**이다.

새 관찰 시작은 DB의 현재 MAX(id)를 after_id로 받고 화면의 이전 결과·reference_time을 초기화한다. DELETE·DB 초기화·볼륨 삭제를 하지 않는다. 첫 결과 요청 때 DB clock_timestamp를 reference_time으로 고정하고, **id > after_id 및 reference_time - 60초 <= occurred_at <= reference_time**을 함께 적용한다. 시작 후 60초 자동 수집 타이머가 아니다. 이후 기준만 10·20으로 바꾸면 같은 after_id·reference_time을 다시 보내므로 같은 행을 비교한다.

build_report는 HTTP 카드 하나만 반환한다. 관찰값·기준·판정·이유, 조회 ID·뒤따른 오류 ID, 같은 행에서 만든 evidence와 records를 제공한다. 화면의 근거 표는 ID·수신시각·방법·경로·상태·종류를 표시한다. http- 뒤 숫자는 DB SELECT의 원본 ID다. 시간상 같은 서비스에서 뒤따른 기록일 뿐 동일 사용자·IP·인과관계·침해를 확정하지 않는다. 기준 미해당도 정상 입증이 아니다. PCAP·IOC는 이 카드에 섞지 않는다.

## 2. 실행 방법

명령은 위 프로젝트 루트의 Windows CMD 기준이다. Docker Desktop과 기존 일반·감시 DB·계정을 사용한다. 새 PC의 빈 DB는 기존 SQL·create_user.py로 준비할 수 있으며 실제 비밀번호·키·토큰을 제출하지 않는다.

루트 .env는 GENERAL_DB_PASSWORD·MONITOR_DB_PASSWORD, 별도의 GENERAL_SECRET_KEY·MONITOR_SECRET_KEY, 공유 EVENT_TOKEN을 사용한다. 이미 설정이 있으면 유지하고 예시로 덮어쓰지 않는다. 새 로컬 설정만 필요하면 `python scripts\configure_local.py`로 Git에서 제외된 개인 값을 생성한다. 각 Flask .env.example의 DB_*·SSL·세션 설정도 유지했다.

Compose의 일반·감시는 별도 프로젝트다. 공유 망 m5d1-events가 이미 있으면 생성하지 않는다. 다른 폴더의 같은 m5d1 프로젝트가 실행 중이면 그 실행 위치를 확인하고 이 폴더로 이어서 실행한다. 기존 DB 비밀번호는 바꾸지 않는다. **down -v, DB 삭제, 기록 삭제로 관찰을 새로 만들지 않는다.**

```cmd
cd /d D:\ALEPH_Codemit\mini-watch-analysis
docker network create m5d1-events
docker compose -f compose-monitor.yaml up -d monitor-db
docker compose -f compose-monitor.yaml exec -T monitor-db psql -v ON_ERROR_STOP=1 -U monitor -d monitor < monitor\backend\sql\day3-analysis.sql
docker compose -f compose-general.yaml config --quiet
docker compose -f compose-monitor.yaml config --quiet
docker compose -f compose-monitor.yaml up -d --build
docker compose -f compose-general.yaml up -d --build
```

day3-analysis.sql은 event_type 열과 DB 저장 시각 기본값만 추가하며 기존 행은 실제 응답 필드로 분류한다. ID·occurred_at·계정·게시글·메모는 지우지 않는다. 새 DB의 docker-init.sql·deploy.sql에는 이 설정도 포함되어 있다. 최초 감시 DB가 아직 준비 중이면 healthy 상태를 확인한 뒤 SQL을 실행한다.

계정이 없다면 각각 `docker compose -f compose-general.yaml exec general-api python create_user.py`, `docker compose -f compose-monitor.yaml exec monitor-api python create_user.py`로 준비한다. 기본 이름은 student·operator이며 비밀번호를 직접 입력한다. 기존 같은 계정은 바꾸지 않는다. 일반 화면은 http://localhost:8081, 감시 화면은 http://localhost:8082다.

monitor-api에는 GENERAL_URL=http://general-api:5000이 연결되어 실제 로컬 일반 요청을 만든다. 분석 API는 기존 로그인과 CSRF를 검사한다. GET /api/analysis는 threshold 정수 1~10000, after_id 0 이상의 정수, 시간대 있는 ISO reference_time을 검증한다. 잘못된 인수는 400이며 로그인 없는 요청은 401이다. 새 관찰 POST의 CSRF가 없으면 403이다. Next 프록시도 /analysis·/analysis/start를 허용하며 Cookie·CSRF·Set-Cookie·상태를 유지한다.

### 같은 observation.json 준비: 4회 사례

캡처 계정은 일반 서비스 계정이다. CMD의 CAPTURE_PASSWORD에 개인 비밀번호를 설정하고 아래 실행이 끝나면 지운다. 값은 코드·문서·제출 파일에 기록하지 않는다. 일반 계정 이름이 student가 아니면 CAPTURE_USERNAME도 설정하고 exec에 `-e CAPTURE_USERNAME`을 추가한다.

```cmd
if not exist monitor\backend\learning\data mkdir monitor\backend\learning\data
docker compose -f compose-monitor.yaml exec -T -e CAPTURE_PASSWORD monitor-api python -m learning.capture_case 4 > monitor\backend\learning\data\observation-next.json && move /Y monitor\backend\learning\data\observation-next.json monitor\backend\learning\data\observation.json
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.lesson2
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.lesson3
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.lesson4 --threshold 10
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.lesson5 --threshold 10
```

CAPTURE_PASSWORD는 `set CAPTURE_PASSWORD=개인값` 형태로 본인 CMD에만 설정하며 셸 기록·제출 문서에 실제 값을 복사하지 않는다. -e는 해당 프로세스 환경을 전달한다. -T는 터미널 장식을 제외한다. `&& move /Y`는 캡처 성공 때만 기존 observation.json을 교체한다. 실패했으면 다음 명령을 실행하지 않고 이전 파일을 이번 결과로 쓰지 않는다. 모든 lesson2~5는 **같은 learning/data/observation.json**을 읽는다. 이 폴더는 호스트에서 준비하며 컨테이너에는 read-only로 연결된다. 캡처 프로그램은 JSON을 stdout으로만 내보내고 컨테이너 원본 폴더에 쓰지 않는다.

### 코드 반영과 12회 화면 비교

최초 빌드 후 Python 분석 소스는 read-only bind mount로 읽으므로 변경 후 API restart, Next 화면은 이미지 rebuild가 필요하다. Python 의존성 변경은 API 이미지도 --build한다.

```cmd
docker compose -f compose-general.yaml restart general-api
docker compose -f compose-monitor.yaml restart monitor-api
docker compose -f compose-monitor.yaml up -d --build monitor-web
docker compose -f compose-monitor.yaml restart monitor-gateway
```

1. 감시 화면에서 기존 operator 계정으로 로그인하고 기준 10, **새 관찰 시작**을 누른다.
2. 다른 탭에서 일반 게시판을 새로고침하지 말고 다음 12회 캡처를 실행한다.

```cmd
docker compose -f compose-monitor.yaml exec -T -e CAPTURE_PASSWORD monitor-api python -m learning.capture_case 12 > monitor\backend\learning\data\observation-next.json && move /Y monitor\backend\learning\data\observation-next.json monitor\backend\learning\data\observation.json
```

3. 성공했다면 요청을 만든 뒤 **1분 안에 첫 결과 불러오기**를 누르고 근거 보기를 펼친다.
4. 새 관찰을 다시 시작하지 않고 기준만 20으로 바꿔 결과를 불러온다. 관찰값·기준시각·근거 ID는 같고 판정만 달라져야 한다. 기준을 10으로 복구한다.
5. 다시 새 관찰을 시작하고 일반 요청 없이 결과를 불러온다. 이전 DB 행을 삭제하지 않아도 ID 경계 뒤 조회가 없으므로 0·빈 근거가 된다.
6. 기본 화면으로 돌아가려면 다시 새 관찰 → 12회 캡처 → 즉시 기준 10 결과를 진행한다. 종료 후 `set CAPTURE_PASSWORD=`로 개인 프로세스 값을 지운다.

파일 실습은 observation.json을 읽지만 화면은 해당 구간의 감시 DB를 직접 읽는다. 캡처는 로그인 완료 **이후**의 ID를 경계로 저장한다. 화면 관찰에 캡처용 로그인 행이 들어올 수 있지만 조회 선택에서 제외되므로 12·13 해석은 같고 근거 ID는 캡처 원본에 대응한다.

캡처 실패·예상과 다른 개수·60초 경과가 있으면 아래 로그를 확인한 뒤 **새 관찰 → 새 캡처 → 즉시 첫 결과**로 재시도한다. 0이나 13에 맞추려고 JSON 숫자·DB를 수정하지 않는다. 전송 실패 기록은 자동 재전송하지 않는다.

```cmd
docker compose -f compose-general.yaml logs --tail 20 general-api
docker compose -f compose-monitor.yaml logs --tail 20 monitor-api
docker compose -f compose-monitor.yaml exec monitor-db psql -U monitor -d monitor -c "SELECT id, occurred_at, method, path, status_code, event_type FROM http_events ORDER BY id DESC LIMIT 15;"
```

표의 http-ID 뒤 숫자와 이 SELECT의 id를 비교한다. SELECT는 기존 행이 남아 있는지 확인하기 위한 조회이며 수정 명령이 아니다.

## 3. 예상 결과와 실제 확인 상태

아래는 다른 일반 요청이 없고 첫 결과가 시간 안에 조회된 통제 사례의 예상이다. 모든 상황에서 근거 13을 고정하는 규칙이 아니다.

| 사례 | 관찰값·판정 | 근거 해석 |
| --- | --- | --- |
| 4회 + 404, 기준 10 | 원본 5·조회 4·False | 정규화는 404를 보존, 조회 선택에서만 제외 |
| 12회 + 404, 기준 10 | 12·검토 후보 | 조회 12 + 뒤따른 404 1 = 13행 |
| 같은 구간 기준 20 | 12·기준 미해당 | 같은 reference_time·after_id·13행 ID 유지 |
| 같은 구간 기준 10 복구 | 12·검토 후보 | 요청 사실이 아닌 비교 조건 변경 |
| 새 관찰 뒤 요청 없음 | 0·기준 미해당·빈 근거 | 이전 DB 행은 보존되고 ID 경계만 변경 |

**직접 확인한 상태 — 2026-10-14:** Python 테스트 20개, 실제 Docker 브라우저·프록시 테스트 5개가 모두 통과했다. 4회 캡처의 원본 5행·조회 4행, 12회 카드의 12·검토 후보·13행, 같은 ID/기준시각에서 기준 20의 미해당, 기준 10 복구, 실제 10회 경계의 10·후보·11행, 새 관찰 후 0·빈 근거와 기존 DB 행 보존을 확인했다. Next lint·production build도 통과했다. PCAP 생성·다시 읽기에서 5초 5개/360바이트·1초 2개/114바이트와 IOC True/False를 직접 확인했다.

이 확인에서는 기존 Day2의 m5d2 프로젝트·DB·계정을 유지하고 8181/8182 포트로 이어 실행했다. 제출 Compose 기본값은 기존 m5d1·8081/8082다. 앱·연결 역할은 같고 실행 위치/포트만 개인 캐시의 로컬 설정으로 맞췄다. 실제 비밀값·실행 중 원본 JSON·로그·스크린샷·DB 덤프는 제출하지 않는다. 이전 Day2의 클라우드 배포 상태는 이번 과제에서 새로 완료했다고 주장하지 않는다.

## 선택 실습

**PCAP 독립 실습:** `docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.educational_pcap`. Scapy로 보내지 않는 교육용 Ethernet/IP/UDP 패킷 6개를 만들고 임시 PCAP에 저장한 후 다시 읽는다. 첫 패킷 기준 [0,5)초는 5개·360바이트, [0,1)초는 2개·114바이트다. 1초로 줄이면 같은 파일에서 선택한 시간 범위만 줄어든다. 생성·읽기·선택은 educational_pcap.py의 create_packets/main/summarize에 있다. 실제 게시판 캡처가 아니며 HTTP 카드 입력으로 사용하지 않는다. 소스 폴더는 read-only이므로 PCAP은 임시 폴더에 만든다.

**IOC 일치:** `docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.ioc_example`. 문서용 지표 203.0.113.7에 같은 문자열은 True, 203.0.113.8은 False다. IP 예제는 [RFC 5737 문서용 주소](https://www.rfc-editor.org/info/rfc5737/)이며 실제 HTTP 원본에 IP가 없으므로 사용자를 식별하거나 실제 요청과 연결하지 않는다.

**기준 경계:** 기준 10·새 관찰 → capture_case 10 → 1분 안에 결과. `10 >= 10`이므로 검토 후보이며 조회 10 + 404 1 = 근거 11행이다. 확인 후 새 관찰 → capture_case 12 → 기준 10 결과로 기본 사례를 복구한다. 파일 숫자를 바꾸는 방식으로 확인하지 않는다.

**AI 후보 코드 검토:** 실제 로그나 비밀값을 외부 AI에 보내지 않고 요구사항만으로 아래 순수 후보를 비교했다.

```python
# 비교용 거절 후보: 이 코드는 실제 분석에 사용하지 않는다.
def candidate(rows, threshold):
    selected = [r for r in rows if r['path'] == '/']
    return {'count': len(selected), 'candidate': len(selected) > threshold,
            'evidence': [r['id'] for r in rows]}
```

거절 이유: method·200·post_list 검사가 없고 `/`의 404도 횟수에 더할 수 있다. `>`는 10회 경계를 누락한다. 모든 행의 ID를 붙여 횟수와 근거가 불일치하고 마지막 조회 뒤 0<gap<=30 검사도 없다. 현재 http_rules.py·report.py는 네 조건으로 같은 views 목록을 만들고 >=, 마지막 수신시각의 404 문맥, views+following에서 ID와 records를 함께 구한다. 이 요구에 맞게 수정한 구현을 채택했다. 이 문서의 후보는 비교 설명용이며 UI/API의 계산에 쓰지 않는다.

제출은 이 폴더의 앱·Compose·gateway·Dockerfile·의존성·잠금 파일·기존 SQL·README를 포함한다. `python scripts/package.py`로 mini-watch-analysis.zip을 만들며 실제 .env·개인 비밀값·observation.json·로그·PCAP·DB 파일·설치물·캐시는 제외한다. GitHub 제출은 day3-analysis 브랜치를 선택한다. Git 이력·공개 클라우드 주소·새 검사 스크립트·스크린샷은 필수 증빙으로 요구하지 않는다.
