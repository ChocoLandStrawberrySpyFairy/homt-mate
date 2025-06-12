# create_database.py
import sqlite3

# 데이터베이스 파일을 만듭니다.
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 사용자 정보를 저장할 테이블 생성 (아이디, 비밀번호, 이름 등)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# 운동 기록을 저장할 테이블 생성 (사용자 ID, 날짜, 운동 종류, 횟수)
cursor.execute('''
CREATE TABLE IF NOT EXISTS exercise_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    exercise_type TEXT,
    count INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# 출석 기록을 저장할 테이블 생성 (사용자 ID, 날짜)
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

conn.commit()
conn.close()

print("Database and tables created successfully.")
