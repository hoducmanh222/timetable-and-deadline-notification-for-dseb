import sqlite3

def initialize_db():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY,
            day TEXT,
            subject TEXT,
            time TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deadlines (
            id INTEGER PRIMARY KEY,
            subject_id INTEGER,
            date TEXT,
            deadline TEXT,
            FOREIGN KEY(subject_id) REFERENCES timetable(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_subject_to_db(day, subject, time):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO timetable (day, subject, time) VALUES (?, ?, ?)', (day, subject, time))
    conn.commit()
    conn.close()

def get_subjects_from_db():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM timetable')
    subjects = cursor.fetchall()
    conn.close()
    return subjects

def add_deadline_to_db(subject_id, date, deadline):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO deadlines (subject_id, date, deadline) VALUES (?, ?, ?)', (subject_id, date, deadline))
    conn.commit()
    conn.close()

def get_deadlines_from_db():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM deadlines')
    deadlines = cursor.fetchall()
    conn.close()
    return deadlines

def get_subject_id(subject_text):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM timetable WHERE subject = ?', (subject_text,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def get_subject_text(subject_id):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT subject FROM timetable WHERE id = ?', (subject_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None