# ALEPH 회원가입

Python FastAPI + SQLAlchemy 백엔드와 Next.js App Router 프론트로 구현한 회원가입입니다. 이름, 이메일, 비밀번호와 비밀번호 확인을 입력하면 SQLite 파일 DB에 회원이 저장됩니다.

## GitHub 소스

공통 과제 저장소의 [sign-up 브랜치](https://github.com/Miko351/ALEPH-CODEMIT-ASSIGNMENTS/tree/sign-up)에 이 프로젝트의 소스를 보관합니다. 이 로컬 폴더의 `origin`은 해당 저장소이며 작업 브랜치는 `sign-up`입니다. 실제 환경 설정, 회원 DB와 설치 캐시는 업로드하지 않습니다.

## 업로드용 ZIP

`D:\ALEPH_Codemit\sign-up\sign-up.zip`을 업로드하면 됩니다. 압축을 풀면 `sign-up/` 폴더 안에 백엔드·프론트·실행 안내가 들어 있습니다. 소스, 테스트, 의존성 lock 파일, `.env.example`을 포함하고 비밀키가 있는 `.env`, 회원 DB, 가상환경, `node_modules`, 빌드 결과, 캐시는 제외합니다. 다른 PC에서는 아래 설치 명령과 키 생성 명령을 실행하면 새 DB가 자동 생성됩니다.

ZIP을 다시 만들려면 프로젝트 루트에서 `python scripts/package.py`를 실행하세요. 아래 명령의 경로는 압축을 푼 위치에 맞게 변경할 수 있습니다.

## 요구사항 충족 방식

| 필수 항목 | 구현 |
| --- | --- |
| 문법 오류 없음 | Python 컴파일, API 테스트, TypeScript 검사, ESLint, Next.js 빌드로 검증 |
| 회원정보 암호화 저장 | 이름·이메일은 Fernet 인증 암호화, 비밀번호는 Argon2id 단방향 해시 |
| DB 저장 | SQLite `members.db`에 영구 저장; DB 경로는 환경변수로 설정 |
| Python | `backend/app`의 API·서비스·보안·DB 로직 |
| SQLAlchemy ORM | 선언형 `Member` 모델, Session과 Repository로 저장 |
| Next.js 프론트 | App Router + React + TypeScript |
| 디렉터리·모듈 분리 | 백엔드 계층과 프론트 페이지·컴포넌트·통신·검증 분리 |

프론트는 Next.js에 맞는 TypeScript로 작성했고 백엔드는 Python입니다. 비밀번호는 복호화가 가능한 암호화 대신 단방향 해시로 보관합니다. 이름·이메일 원문과 비밀번호 원문은 DB에 저장하지 않습니다. 이메일 중복 검사는 별도 비밀키를 사용하는 HMAC-SHA256 값으로 처리하며 DB의 UNIQUE 제약으로 동시 가입도 차단합니다. UUID와 가입 시각은 메타데이터로 평문 저장합니다.

## 실행 (Windows PowerShell)

Python 3.11 이상, Node.js 20.9 이상이 필요합니다. 아래 명령은 프로젝트 루트에서 실행합니다.

백엔드:

```powershell
cd D:\ALEPH_Codemit\sign-up\backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock.txt
.\.venv\Scripts\python.exe scripts/init_env.py
.\.venv\Scripts\python.exe -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000 --reload
```

다른 터미널에서 프론트:

```powershell
cd D:\ALEPH_Codemit\sign-up\frontend
npm.cmd ci
Copy-Item .env.example .env.local
npm.cmd run dev
```

접속: [회원가입 화면](http://127.0.0.1:3000), [API 문서](http://127.0.0.1:8000/docs), [상태 확인](http://127.0.0.1:8000/api/health).

`init_env.py`는 기존 `.env`를 덮어쓰지 않습니다. 이미 생성되어 있으면 그대로 실행할 수 있습니다. `backend/.env`의 두 키는 서버에만 보관하고 DB와 함께 백업해야 기존 개인정보를 복호화하고 중복 여부를 확인할 수 있습니다. DB 생성 후 키를 새로 생성하거나 교체하면 기존 데이터에 접근할 수 없으므로 데이터·인덱스 재암호화 절차가 필요합니다. 프론트에는 공개 API 주소만 설정합니다. 운영 배포 시 HTTPS와 별도 비밀키 관리를 적용하세요.

## 구조

```text
backend/
  app/
    api/            # HTTP 라우터
    core/           # 설정, 개인정보 암호화, 비밀번호 해시
    db/             # ORM Base, 엔진, 요청별 Session
    models/         # SQLAlchemy 회원 모델
    schemas/        # 입력 검증, 응답 스키마
    repositories/   # 조회·저장
    services/       # 회원가입 로직
    main.py         # 앱 조립, CORS, DB 초기화
  scripts/          # 로컬 키 생성, E2E 전용 API
  tests/            # API·암호화·DB 통합 테스트
frontend/
  src/
    app/            # 페이지, 레이아웃, 스타일
    components/
      signup/       # 회원가입 폼
      ui/           # 공용 필드, 아이콘
    lib/            # API 호출, 폼 검증
  tests/            # 데스크톱·모바일 브라우저 통합 테스트
```

## API

`POST /api/auth/register`

```json
{"name":"홍길동","email":"member@example.com","password":"correct-horse-123"}
```

- `201`: 회원 ID, 이름, UTC 가입 시각 반환. 비밀번호·해시·암호화된 데이터는 반환하지 않습니다.
- `409`: 정규화된 이메일 중복. 이메일의 앞뒤 공백과 대소문자를 동일하게 처리합니다.
- `422`: 이름 2~80자, 유효한 이메일 254자 이내, 공백만이 아닌 비밀번호 10~128자 등 입력 검증 실패. 오류 응답에 입력 원문을 포함하지 않습니다.

비밀번호 확인은 프론트에서 검사하고 API에 전송하지 않습니다. 서버는 나머지 필드를 독립적으로 재검증합니다. 가입 성공, 입력 오류, 중복 이메일, 통신 오류, 전송 중 상태 및 재시도를 지원합니다. 로그인·이메일 인증은 이번 회원가입 범위에 포함하지 않습니다.

## 검증

API·DB 통합 테스트 12개, 데스크톱·모바일 E2E 테스트 8개를 통과했습니다. TypeScript 검사, ESLint, Next.js 프로덕션 빌드도 검증했습니다.

```powershell
cd D:\ALEPH_Codemit\sign-up\backend
.\.venv\Scripts\python.exe -m compileall -q app scripts tests
.\.venv\Scripts\python.exe -m pytest -q

cd D:\ALEPH_Codemit\sign-up\frontend
npm.cmd run lint
npm.cmd run typecheck
npm.cmd run build
$env:PLAYWRIGHT_BROWSERS_PATH = 'D:\ALEPH_Codemit\sign-up\.cache\ms-playwright'
npx.cmd playwright install chromium
npm.cmd run test:e2e
```

E2E 테스트는 3001·8001 포트에서 프론트와 백엔드를 직접 실행합니다. 임시 DB와 테스트 전용 임시 키를 사용하므로 실제 회원 DB를 변경하지 않습니다. 테스트 종료 시 서버도 종료됩니다. API 테스트 역시 임시 DB를 사용하며 실제 DB 파일에 개인정보·비밀번호 원문이 없는지, 새 DB 연결에서도 회원이 유지되는지 검사합니다.

의존성은 프론트 `package-lock.json`, 백엔드 `requirements-dev.lock.txt`에 고정합니다. 신규 패키지를 조정할 때만 범위가 지정된 `requirements-dev.txt`를 사용해 설치 후 lock 파일을 갱신하세요. 현재 초기 DB 생성은 `create_all`을 사용합니다. 기존 테이블 구조를 변경해야 하는 경우 Alembic 마이그레이션을 추가하세요.

참고한 공식 문서: [FastAPI 비밀번호 해시](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [Fernet 인증 암호화](https://cryptography.io/en/latest/fernet/), [SQLAlchemy 선언형 모델](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html), [Next.js 설치](https://nextjs.org/docs/app/getting-started/installation).
