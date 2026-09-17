import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("ai_tutor.db")


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT NOT NULL DEFAULT '',
            goal TEXT NOT NULL DEFAULT '',
            level TEXT NOT NULL DEFAULT 'Beginner'
        );
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            topic TEXT NOT NULL,
            mode TEXT NOT NULL,
            level TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL
        );
        """)


def get_profile():
    with connect() as db:
        row = db.execute("SELECT name, goal, level FROM profile WHERE id=1").fetchone()
    return dict(row) if row else {"name": "", "goal": "", "level": "Beginner"}


def save_profile(name, goal, level):
    with connect() as db:
        db.execute("""INSERT INTO profile(id,name,goal,level) VALUES(1,?,?,?)
        ON CONFLICT(id) DO UPDATE SET name=excluded.name, goal=excluded.goal, level=excluded.level""", (name.strip(), goal.strip(), level))


def save_session(session):
    with connect() as db:
        db.execute("""INSERT INTO sessions(created_at,topic,mode,level,prompt,response)
        VALUES(?,?,?,?,?,?)""", tuple(session[key] for key in ("timestamp", "topic", "mode", "level", "prompt", "response")))


def list_sessions(limit=25):
    with connect() as db:
        rows = db.execute("SELECT created_at as timestamp, topic, mode, level, prompt, response FROM sessions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(row) for row in rows]


def clear_sessions():
    with connect() as db:
        db.execute("DELETE FROM sessions")
