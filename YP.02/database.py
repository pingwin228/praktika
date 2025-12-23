# database.py
import sqlite3
from datetime import date

DB_NAME = "diary.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        date TEXT NOT NULL,
        grade INTEGER CHECK(grade BETWEEN 1 AND 5),
        type TEXT,
        comment TEXT,
        FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS homeworks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        issue_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        text TEXT NOT NULL,
        completed INTEGER DEFAULT 0,  -- 0 = нет, 1 = да
        completed_date TEXT,
        FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)
    
    # Индексы для оптимизации
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_homeworks_subject ON homeworks(subject_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_homeworks_due ON homeworks(due_date)")
    
    conn.commit()
    conn.close()

# ======= Предметы =======
def add_subject(name):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_subjects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_subject(subject_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    conn.commit()
    conn.close()

# ======= Оценки =======
def add_grade(subject_id, date_str, grade, type_, comment=""):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO grades (subject_id, date, grade, type, comment)
    VALUES (?, ?, ?, ?, ?)
    """, (subject_id, date_str, grade, type_, comment))
    conn.commit()
    conn.close()

def get_grades_by_subject(subject_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grades WHERE subject_id = ? ORDER BY date DESC", (subject_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_grades():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT g.*, s.name as subject_name 
    FROM grades g JOIN subjects s ON g.subject_id = s.id 
    ORDER BY g.date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

# ======= Домашние задания =======
def add_homework(subject_id, issue_date, due_date, text):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO homeworks (subject_id, issue_date, due_date, text)
    VALUES (?, ?, ?, ?)
    """, (subject_id, issue_date, due_date, text))
    conn.commit()
    conn.close()

def get_homeworks(subject_id=None):
    conn = connect_db()
    cursor = conn.cursor()
    if subject_id:
        cursor.execute("""
        SELECT h.*, s.name as subject_name 
        FROM homeworks h JOIN subjects s ON h.subject_id = s.id 
        WHERE h.subject_id = ? ORDER BY due_date
        """, (subject_id,))
    else:
        cursor.execute("""
        SELECT h.*, s.name as subject_name 
        FROM homeworks h JOIN subjects s ON h.subject_id = s.id 
        ORDER BY due_date
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def toggle_homework_completed(hw_id, completed):
    conn = connect_db()
    cursor = conn.cursor()
    completed_date = date.today().isoformat() if completed else None
    cursor.execute("""
    UPDATE homeworks SET completed = ?, completed_date = ? WHERE id = ?
    """, (1 if completed else 0, completed_date, hw_id))
    conn.commit()
    conn.close()

def delete_homework(hw_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM homeworks WHERE id = ?", (hw_id,))
    conn.commit()
    conn.close()