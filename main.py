from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3, os, shutil, uuid
from datetime import datetime, date
from typing import Optional
import json

app = FastAPI(title="범퍼 수정일지 API")

# CORS 설정 (모든 기기에서 접근 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 이미지 저장 폴더
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 정적 파일 서빙 (업로드된 이미지)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ── DB 초기화 ──────────────────────────────────────────
def get_db():
    conn = sqlite3.connect("bumper.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            factory     TEXT NOT NULL,
            model       TEXT NOT NULL,
            position    TEXT NOT NULL,
            cno         TEXT,
            color       TEXT,
            defect      TEXT,
            defect_sub  TEXT,
            action      TEXT,
            resp        TEXT,
            note        TEXT,
            photo_paths TEXT,        -- JSON 배열
            submitted_at TEXT NOT NULL,
            date        TEXT NOT NULL  -- YYYY-MM-DD (조회용)
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ── 유틸 ───────────────────────────────────────────────
def row_to_dict(row):
    d = dict(row)
    d["photos"] = json.loads(d.pop("photo_paths") or "[]")
    return d

# ── 엔드포인트 ─────────────────────────────────────────

@app.post("/submit")
async def submit_record(
    factory:    str = Form(...),
    model:      str = Form(...),
    position:   str = Form(...),
    cno:        str = Form(""),
    color:      str = Form(""),
    defect:     str = Form(""),
    defect_sub: str = Form(""),
    action:     str = Form(""),
    resp:       str = Form(""),
    note:       str = Form(""),
    photos: list[UploadFile] = File(default=[]),
):
    # 이미지 저장
    saved_paths = []
    for photo in photos:
        if photo.filename:
            ext = os.path.splitext(photo.filename)[1] or ".jpg"
            fname = f"{uuid.uuid4().hex}{ext}"
            fpath = os.path.join(UPLOAD_DIR, fname)
            with open(fpath, "wb") as f:
                shutil.copyfileobj(photo.file, f)
            saved_paths.append(f"/uploads/{fname}")

    now = datetime.now()
    conn = get_db()
    conn.execute("""
        INSERT INTO records
        (factory, model, position, cno, color, defect, defect_sub,
         action, resp, note, photo_paths, submitted_at, date)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        factory, model, position, cno, color, defect, defect_sub,
        action, resp, note,
        json.dumps(saved_paths),
        now.isoformat(),
        now.strftime("%Y-%m-%d"),
    ))
    conn.commit()
    conn.close()

    return {"ok": True, "message": "저장 완료"}


@app.get("/records")
def get_records(
    date:    Optional[str] = Query(None),   # YYYY-MM-DD
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
    return [row_to_dict(r) for r in rows]


@app.get("/records/summary")
def get_summary(
    year:  int = Query(datetime.now().year),
    month: int = Query(datetime.now().month),
):
    """달력용: 해당 월의 날짜별 건수 반환"""
    conn = get_db()
    rows = conn.execute("""
        SELECT date, COUNT(*) as cnt
        FROM records
        WHERE strftime('%Y', date)=? AND strftime('%m', date)=?
        GROUP BY date
    """, (str(year), str(month).zfill(2))).fetchall()
    conn.close()
    return {r["date"]: r["cnt"] for r in rows}


@app.get("/records/{record_id}")
def get_record(record_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM records WHERE id=?", (record_id,)).fetchone()
    conn.close()
    if not row:
        return {"error": "not found"}
    return row_to_dict(row)


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
