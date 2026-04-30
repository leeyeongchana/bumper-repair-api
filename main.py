from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import json

# ── PostgreSQL (Supabase) ──────────────────────────────────────────────────────
# Render.com 환경변수 DATABASE_URL 에 Supabase 연결문자열을 설정하세요.
# 예) postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get("DATABASE_URL", "")

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id           SERIAL PRIMARY KEY,
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
    # photos 컬럼 없는 기존 테이블에 추가 (이미 있으면 무시)
    try:
        cur.execute("ALTER TABLE records ADD COLUMN IF NOT EXISTS photos TEXT")
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
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
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
    new_id = cur.fetchone()[0]
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
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    q = "SELECT * FROM records WHERE 1=1"
    params = []
    if date:
        q += " AND date=%s"; params.append(date)
    if factory:
        q += " AND factory=%s"; params.append(factory)
    q += " ORDER BY submitted_at DESC LIMIT %s"
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
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT date, COUNT(*) as cnt
        FROM records
        WHERE SUBSTRING(date,1,4)=%s AND SUBSTRING(date,6,2)=%s
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
    cur.execute("DELETE FROM records WHERE id=%s", (record_id,))
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
