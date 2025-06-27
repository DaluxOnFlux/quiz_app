from __future__ import annotations
import sqlite3
from dataclasses import dataclass, asdict
from typing import Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "quiz.db")



@dataclass
class Question:
    id: Optional[int]     
    position: int
    title: str
    text: str
    image: str            

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_row(row: sqlite3.Row) -> "Question":
        return Question(
            id=row["id"],
            position=row["position"],
            title=row["title"],
            text=row["text"],
            image=row["image"],
        )

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None      
    return conn


def _shift_positions(conn: sqlite3.Connection, start: int, end: int, delta: int) -> None:
    cur = conn.cursor()

    if delta == +1:
        cur.execute(
            "SELECT id, position FROM Question WHERE position BETWEEN ? AND ? ORDER BY position DESC",
            (start, end),
        )
    else: 
        cur.execute(
            "SELECT id, position FROM Question WHERE position BETWEEN ? AND ? ORDER BY position ASC",
            (start, end),
        )

    for row in cur.fetchall():
        cur.execute("UPDATE Question SET position = ? WHERE id = ?", (row["position"] + delta, row["id"]))

def insert(q: Question) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")

        _shift_positions(conn, q.position, 10_000_000, +1) 

        cur.execute(
            "INSERT INTO Question (position, title, text, image) VALUES (?, ?, ?, ?)",
            (q.position, q.title, q.text, q.image),
        )
        qid = cur.lastrowid
        conn.commit()
        return qid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_by_position(pos: int) -> Optional[Question]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Question WHERE position = ?", (pos,))
        row = cur.fetchone()
        return Question.from_row(row) if row else None
    finally:
        conn.close()


def get_by_id(qid: int) -> Optional[Question]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Question WHERE id = ?", (qid,))
        row = cur.fetchone()
        return Question.from_row(row) if row else None
    finally:
        conn.close()


def update(qid: int, q: Question) -> bool:
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")

        cur.execute("SELECT position FROM Question WHERE id = ?", (qid,))
        row = cur.fetchone()
        if not row:
            conn.rollback()
            return False

        old_pos = row["position"]
        new_pos = q.position

        if new_pos != old_pos:
            cur.execute("UPDATE Question SET position = -1 WHERE id = ?", (qid,))

            if new_pos < old_pos:
                _shift_positions(conn, new_pos, old_pos - 1, +1)
            else:
                _shift_positions(conn, old_pos + 1, new_pos, -1)

            cur.execute("""
                UPDATE Question
                   SET position = ?, title = ?, text = ?, image = ?
                 WHERE id = ?
            """, (new_pos, q.title, q.text, q.image, qid))

        else:
            cur.execute("""
                UPDATE Question
                   SET title = ?, text = ?, image = ?
                 WHERE id = ?
            """, (q.title, q.text, q.image, qid))

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()




def delete_all() -> None:
    conn = _get_conn()
    try:
        conn.execute("DELETE FROM Question")
        conn.commit()
    finally:
        conn.close()

def delete_by_id(qid: int) -> bool:
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        cur.execute("SELECT position FROM Question WHERE id = ?", (qid,))
        row = cur.fetchone()
        if not row:
            conn.rollback()
            return False

        pos = row["position"]

        cur.execute("DELETE FROM Question WHERE id = ?", (qid,))
        if cur.rowcount != 1:
            conn.rollback()
            return False

        _shift_positions(conn, pos + 1, 10_000_000, -1)

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

