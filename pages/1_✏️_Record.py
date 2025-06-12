# pages/2_Record.py
import streamlit as st
import sqlite3
from datetime import date

st.title("운동 기록장 🏃")
st.write()

if 'username' in st.session_state:
    # 운동 종류와 횟수 입력 섹션
    exercise_type = st.selectbox("운동 종류를 선택하세요 : ", ["스쿼트", "사이드레터럴레이즈", "크런치"])
    count = st.number_input(f"{exercise_type} 횟수를 입력하세요 : ", min_value=0, step=1)
    record_date = st.date_input("기록 날짜를 선택하세요 : ", date.today())

    # 기록 저장 버튼
    if st.button("기록 저장"):
        # 운동 타입을 영어로 변환하여 저장하기 위한 매핑
        exercise_mapping = {
            "스쿼트": "squat",
            "사이드레터럴레이즈": "side_lateral_raise",
            "크런치": "crunch"
        }
        selected_exercise = exercise_mapping[exercise_type]

        # 데이터베이스에 운동 횟수 저장
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT count FROM exercise_logs
            JOIN users ON exercise_logs.user_id = users.id
            WHERE users.username = ? AND exercise_logs.date = ? AND exercise_logs.exercise_type = ?
        ''', (st.session_state['username'], record_date, selected_exercise))
        result = cursor.fetchone()
        
        if result:
            new_count = result[0] + count
            cursor.execute('''
                UPDATE exercise_logs SET count = ? 
                WHERE date = ? AND user_id = (SELECT id FROM users WHERE username = ?) AND exercise_type = ?
            ''', (new_count, record_date, st.session_state['username'], selected_exercise))
        else:
            cursor.execute('''
                INSERT INTO exercise_logs (user_id, date, exercise_type, count) 
                VALUES ((SELECT id FROM users WHERE username = ?), ?, ?, ?)
            ''', (st.session_state['username'], record_date, selected_exercise, count))
        
        conn.commit()
        conn.close()
        st.success(f"{record_date}에 {exercise_type} {count}회가 저장되었습니다.")
else:
    st.warning("운동 횟수를 저장하려면 로그인하세요.")

