# db_init.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "quiz.db")

def rebuild_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS ParticipationAnswer;
    DROP TABLE IF EXISTS Participation;
    DROP TABLE IF EXISTS Answer;
    DROP TABLE IF EXISTS Question;

    CREATE TABLE Question (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position INTEGER NOT NULL UNIQUE,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        image TEXT NOT NULL
    );

    CREATE TABLE Answer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        is_correct BOOLEAN NOT NULL,
        id_question INTEGER NOT NULL,
        FOREIGN KEY (id_question) REFERENCES Question(id)
    );

    CREATE TABLE Participation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player TEXT NOT NULL,
        score INTEGER NOT NULL
    );

    CREATE TABLE ParticipationAnswer (
        id_participation INTEGER,
        id_question INTEGER,
        id_answer INTEGER,
        FOREIGN KEY (id_participation) REFERENCES Participation(id),
        FOREIGN KEY (id_question) REFERENCES Question(id),
        FOREIGN KEY (id_answer) REFERENCES Answer(id)
    );
    """)

    conn.commit()
    conn.close()
