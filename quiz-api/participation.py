import sqlite3
from dataclasses import dataclass, asdict
from typing import Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "quiz.db")

@dataclass
class Participation:
    id: Optional[int]
    player: str
    score: int

    def to_dict(self):
        return asdict(self)

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None
    return conn

def insert_participation(player: str, answers: list[dict], score: int) -> int:
    """
    answers : liste de { "id_question": int, "id_answer": int }
    """
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")

        cur.execute(
            "INSERT INTO Participation (player, score) VALUES (?, ?)",
            (player, score)
        )
        pid = cur.lastrowid

        for a in answers:
            cur.execute(
                "INSERT INTO ParticipationAnswer (id_participation, id_question, id_answer) VALUES (?, ?, ?)",
                (pid, a["id_question"], a["id_answer"])
            )

        conn.commit()
        return pid, score
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def delete_all_participations():
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("BEGIN")
        cur.execute("DELETE FROM ParticipationAnswer")
        cur.execute("DELETE FROM Participation")
        conn.commit()
    finally:
        conn.close()

def get_all_scores():
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT player, score FROM Participation ORDER BY score DESC")
        return [{"playerName": row["player"], "score": row["score"]} for row in cur.fetchall()]
    finally:
        conn.close()
