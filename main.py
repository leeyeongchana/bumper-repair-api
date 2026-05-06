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

DB_PATH = os.path.join(BASE_DIR, "bumper_log.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            factory      TEXT,
            model        TEXT,
            position     TEXT,
            cno          TEXT,
            color        TEXT,
            action       TEXT,
            defect       TEXT,
            defect_sub   TEXT,
            resp         TEXT,
            memo         TEXT,
            markers      TEXT,
            photos       TEXT,
            submitted_at TEXT,
            date         TEXT
        )
    """)
    # photos 컬럼 없는 기존 테이블에 추가 (SQLite는 IF NOT EXISTS 미지원이라 컬럼 존재 여부 확인)
    cur.execute("PRAGMA table_info(records)")
    existing_cols = {row[1] for row in cur.fetchall()}
    if "photos" not in existing_cols:
        try:
            cur.execute("ALTER TABLE records ADD COLUMN photos TEXT")
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
    factory:    str = ""
    model:      str = ""
    position:   str = ""
    cno:        str = ""
    color:      str = ""
    action:     str = ""
    defect:     str = ""
    defect_sub: str = ""
    resp:       str = ""
    memo:       str = ""
    markers:    list = []
    photos:     list = []

# ── 제출 ───────────────────────────────────────────────────────────────────────
@app.post("/submit")
async def submit_record(record: Record):
    now = datetime.now()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO records
        (factory, model, position, cno, color, action, defect, defect_sub,
         resp, memo, markers, photos, submitted_at, date)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        record.factory, record.model, record.position,
        record.cno, record.color, record.action,
        record.defect, record.defect_sub,
        record.resp, record.memo,
        json.dumps(record.markers, ensure_ascii=False),
        json.dumps(record.photos, ensure_ascii=False),
        now.isoformat(),
        now.strftime("%Y-%m-%d"),
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
