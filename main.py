from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── SQLite (로컬 파일) ─────────────────────────────────────────────────────────
# 별도 DB 서버 없이 작동. main.py와 같은 폴더의 bumper_log.db 파일을 사용.
import sqlite3

DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "bumper_log.db"))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            factory           TEXT,
            model             TEXT,
            position          TEXT,
            cno               TEXT,
            color             TEXT,
            action            TEXT,
            defect            TEXT,
            defect_sub        TEXT,
            resp              TEXT,
            memo              TEXT,
            markers           TEXT,
            photos            TEXT,
            submitted_at      TEXT,
            date              TEXT,
            submitted_by_id   TEXT,
            submitted_by_name TEXT,
            submitted_by_dept TEXT
        )
    """)
    # 기존 테이블에 누락된 컬럼이 있으면 ALTER로 추가
    cur.execute("PRAGMA table_info(records)")
    existing_cols = {row[1] for row in cur.fetchall()}
    for col, typ in [
        ("photos",            "TEXT"),
        ("submitted_by_id",   "TEXT"),
        ("submitted_by_name", "TEXT"),
        ("submitted_by_dept", "TEXT"),
    ]:
        if col not in existing_cols:
            try:
                cur.execute(f"ALTER TABLE records ADD COLUMN {col} {typ}")
            except Exception:
                pass
    conn.commit()
    cur.close()
    conn.close()

init_db()

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(title="범퍼 수정일지 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Record(BaseModel):
    factory:           str = ""
    model:             str = ""
    position:          str = ""
    cno:               str = ""
    color:             str = ""
    action:            str = ""
    defect:            str = ""
    defect_sub:        str = ""
    resp:              str = ""
    memo:              str = ""
    markers:           list = []
    photos:            list = []
    submitted_by_id:   str = ""
    submitted_by_name: str = ""
    submitted_by_dept: str = ""

# ── 제출 ───────────────────────────────────────────────────────────────────────
@app.post("/submit")
async def submit_record(record: Record):
    now = datetime.now()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO records
        (factory, model, position, cno, color, action, defect, defect_sub,
         resp, memo, markers, photos, submitted_at, date,
         submitted_by_id, submitted_by_name, submitted_by_dept)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        record.factory, record.model, record.position,
        record.cno, record.color, record.action,
        record.defect, record.defect_sub,
        record.resp, record.memo,
        json.dumps(record.markers, ensure_ascii=False),
        json.dumps(record.photos, ensure_ascii=False),
        now.isoformat(),
        now.strftime("%Y-%m-%d"),
        record.submitted_by_id,
        record.submitted_by_name,
        record.submitted_by_dept,
    ))
    new_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return {"ok": True, "message": "저장 완료", "id": new_id}

# ── 조회 ───────────────────────────────────────────────────────────────────────
@app.get("/records")
def get_records(
    date:    Optional[str] = Query(None),
    factory: Optional[str] = Query(None),
    limit:   int = Query(200),
):
    conn = get_db()
    cur = conn.cursor()
    q = "SELECT * FROM records WHERE 1=1"
    params = []
    if date:
        q += " AND date=?"; params.append(date)
    if factory:
        q += " AND factory=?"; params.append(factory)
    q += " ORDER BY submitted_at DESC LIMIT ?"
    params.append(limit)
    cur.execute(q, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d['markers'] = json.loads(d.get('markers') or '[]')
        d['photos'] = json.loads(d.get('photos') or '[]')
        result.append(d)
    return result

# ── 월별 요약 ──────────────────────────────────────────────────────────────────
@app.get("/records/summary")
def get_summary(
    year:  int = Query(datetime.now().year),
    month: int = Query(datetime.now().month),
):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT date, COUNT(*) as cnt
        FROM records
        WHERE substr(date,1,4)=? AND substr(date,6,2)=?
        GROUP BY date
    """, (str(year), str(month).zfill(2)))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {r["date"]: r["cnt"] for r in rows}

# ── 단건 삭제 ──────────────────────────────────────────────────────────────────
@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM records WHERE id=?", (record_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"ok": True}

# ── 전체 삭제 (테스트 데이터 초기화용) ────────────────────────────────────────
@app.delete("/records")
def delete_all_records():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM records")
    conn.commit()
    cur.close()
    conn.close()
    return {"ok": True, "message": "전체 삭제 완료"}

# ── 헬스체크 ──────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}

# ── 사번 로그인 프록시 ────────────────────────────────────────────────────────
# selfservice.icams.co.kr 의 ERP 인증 API를 서버에서 대리 호출.
# API 키와 주민등록번호 같은 민감 정보는 클라이언트로 노출하지 않음.
import urllib.request as _urlreq
import urllib.error as _urlerr

ICAMS_BASE = os.environ.get("ICAMS_BASE", "https://selfservice.icams.co.kr")
ICAMS_API_KEY = os.environ.get("ICAMS_API_KEY", "6147")
# 초기 운영 단계: 사번 == 비밀번호 입력 시 임시 통과 (env로 끌 수 있음)
ALLOW_INITIAL_LOGIN = os.environ.get("ALLOW_INITIAL_LOGIN", "1") == "1"
SENSITIVE_KEY_HINTS = ("resident", "rrn", "ssn", "registration", "regnumber", "regno", "socialsecurity")

def _strip_sensitive(d):
    if not isinstance(d, dict):
        return d
    cleaned = {}
    for k, v in d.items():
        kl = k.lower().replace("_", "")
        if any(h in kl for h in SENSITIVE_KEY_HINTS):
            continue
        cleaned[k] = _strip_sensitive(v) if isinstance(v, dict) else v
    return cleaned

def _normalize_employee(emp):
    """ICAMS 응답의 다양한 부서/이름 키를 표준 키(name, department)로 정규화."""
    if not isinstance(emp, dict):
        return emp
    if not emp.get("department"):
        for k in ("deptName", "departmentName", "departmentNm", "deptNm",
                  "dept", "department_name", "dept_name", "부서", "부서명"):
            v = emp.get(k)
            if v:
                emp["department"] = v
                break
    if not emp.get("name"):
        for k in ("employeeName", "userName", "empName", "empNm",
                  "employee_name", "user_name", "이름", "성명"):
            v = emp.get(k)
            if v:
                emp["name"] = v
                break
    return emp

class LoginPayload(BaseModel):
    employeeId: str = ""
    password:   str = ""

@app.post("/auth/login")
async def auth_login(payload: LoginPayload):
    if not payload.employeeId or not payload.password:
        return {"authenticated": False, "error": "사번과 비밀번호를 입력해주세요"}

    # 1) ICAMS 인증 서버에 먼저 시도 — 성공하면 실제 사원 정보 사용
    body = json.dumps({
        "employeeId": payload.employeeId,
        "password":   payload.password,
    }).encode("utf-8")
    req = _urlreq.Request(
        ICAMS_BASE + "/api/erp/login",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key":    ICAMS_API_KEY,
        },
        method="POST",
    )
    upstream_failed = False
    try:
        with _urlreq.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw) if raw else {}
        if isinstance(data, dict) and data.get("authenticated"):
            employee = _normalize_employee(_strip_sensitive(data.get("employee") or {}))
            return {"authenticated": True, "employee": employee}
        upstream_failed = True  # 200이지만 인증 실패
    except _urlerr.HTTPError as e:
        upstream_failed = (e.code == 401)
        if not upstream_failed:
            return {"authenticated": False, "error": f"인증 서버 오류 ({e.code})"}
    except Exception:
        upstream_failed = True  # 네트워크 오류도 폴백 허용

    # 2) 초기 운영 폴백: 사번 == 비밀번호 입력 시 임시 통과
    if ALLOW_INITIAL_LOGIN and payload.employeeId == payload.password:
        return {
            "authenticated": True,
            "employee": {
                "employeeId": payload.employeeId,
                "name":       f"사번 {payload.employeeId}",
                "department": "",
                "_initialLogin": True,
            },
        }

    return {"authenticated": False, "error": "사번 또는 비밀번호가 올바르지 않습니다"}

# ── HTML 페이지 라우트 ────────────────────────────────────────────────────────
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse(os.path.join(BASE_DIR, "dashboard.html"))

# ── 정적 파일 (CSS/JS 등) ─────────────────────────────────────────────────────
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ── 직접 실행 진입점 ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
