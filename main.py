from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, os
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import json

app = FastAPI(title="범퍼 수정일지 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect("bumper.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
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
            submitted_at TEXT,
            date         TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

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

@app.post("/submit")
async def submit_record(record: Record):
    now = datetime.now()
    conn = get_db()
    conn.execute("""
        INSERT INTO records
        (factory, model, position, cno, color, action, defect, defect_sub,
         resp, memo, markers, submitted_at, date)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        record.factory, record.model, record.position,
        record.cno, record.color, record.action,
        record.defect, record.defect_sub,
        record.resp, record.memo,
        json.dumps(record.markers, ensure_ascii=False),
        now.isoformat(),
        now.strftime("%Y-%m-%d"),
    ))
    conn.commit()
    conn.close()
    return {"ok": True, "message": "저장 완료"}

@app.get("/records")
def get_records(
    date:    Optional[str] = Query(None),
    factory: Optional[str] = Query(None),
    limit:   int = Query(200),
):
    conn = get_db()
    q = "SELECT * FROM records WHERE 1=1"
    params = []
    if date:
        q += " AND date=?"; params.append(date)
    if factory:
        q += " AND factory=?"; params.append(factory)
    q += " ORDER BY submitted_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(q, params).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d['markers'] = json.loads(d.get('markers') or '[]')
        result.append(d)
    return result

@app.get("/records/summary")
def get_summary(
    year:  int = Query(datetime.now().year),
    month: int = Query(datetime.now().month),
):
    conn = get_db()
    rows = conn.execute("""
        SELECT date, COUNT(*) as cnt
        FROM records
        WHERE strftime('%Y', date)=? AND strftime('%m', date)=?
        GROUP BY date
    """, (str(year), str(month).zfill(2))).fetchall()
    conn.close()
    return {r["date"]: r["cnt"] for r in rows}

@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    conn = get_db()
    conn.execute("DELETE FROM records WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    return {"ok": True}

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}
