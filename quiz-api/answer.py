from dataclasses import dataclass, asdict
import sqlite3
from typing import Optional

DB_PATH = "quiz.db"

@dataclass
class Answer:
    id: Optional[int]
    text: str
    is_correct: bool
    id_question: int

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "isCorrect": self.is_correct,
            "id_question": self.id_question
        }

    @staticmethod
    def from_row(row: sqlite3.Row) -> "Answer":
        return Answer(
            id=row["id"],
            text=row["text"],
            is_correct=bool(row["is_correct"]),
            id_question=row["id_question"]
        )

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None
    return conn

def insert(answer: Answer) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        cur.execute(
            "INSERT INTO Answer (text, is_correct, id_question) VALUES (?, ?, ?)",
            (answer.text, int(answer.is_correct), answer.id_question),
        )
        aid = cur.lastrowid
        conn.commit()
        return aid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_all_by_question(qid: int) -> list[Answer]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Answer WHERE id_question = ?", (qid,))
        return [Answer.from_row(row) for row in cur.fetchall()]
    finally:
        conn.close()
