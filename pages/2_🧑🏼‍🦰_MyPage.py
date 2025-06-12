import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.title("마이페이지 ☺️")

if 'username' in st.session_state:
    st.write()

    with st.expander("**오늘의 운동 기록**"):
        # 오늘의 날짜 설정
        today = datetime.today().date()

        # 오늘의 운동 기록 불러오기
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # 운동별 오늘의 기록 가져오기
        exercises = ["스쿼트", "사이드레터럴레이즈", "크런치"]
        exercise_counts = {}
        calories_burned = {}
        total_calories = 0.0

        # 운동별 칼로리 소모량 설정
        calorie_per_rep = {
            "스쿼트": 0.32,
            "사이드레터럴레이즈": 0.2,
            "크런치": 0.3
        }

        for exercise in exercises:
            exercise_mapping = {
                "스쿼트": "squat",
                "사이드레터럴레이즈": "side_lateral_raise",
                "크런치": "crunch"
            }
            selected_exercise = exercise_mapping[exercise]

            cursor.execute('''
                SELECT count FROM exercise_logs
                JOIN users ON exercise_logs.user_id = users.id
                WHERE users.username = ? AND exercise_logs.exercise_type = ? AND date = ?
            ''', (st.session_state['username'], selected_exercise, today))

            data = cursor.fetchone()
            count = data[0] if data else 0
            exercise_counts[exercise] = count

            # 각 운동별 칼로리 계산
            calories = count * calorie_per_rep[exercise]
            calories_burned[exercise] = calories
            total_calories += calories

        conn.close()

        st.subheader(f"오늘 소모된 총 칼로리🔥 : **{total_calories:.2f} kcal**")
        
        # 운동별 기록을 한 줄에 네모 박스로 표시
        columns = st.columns(len(exercises))
        for i, (exercise, count) in enumerate(exercise_counts.items()):
            with columns[i]:
                st.markdown(f"""
                    <div style="border: 2px solid #aaa; padding: 20px; border-radius: 5px; text-align: center;">
                        <h4>{exercise}</h4>
                        <p>{count}회</p>
                        <p>소모 칼로리: {calories_burned[exercise]:.2f} kcal</p>
                    </div>
                """, unsafe_allow_html=True)
                
    # 출석체크 기능
    with st.expander("**출석 체크**"):
        
        # 캘린더 표시 및 출석 기록 불러오기
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date FROM attendance_logs
            WHERE user_id = (SELECT id FROM users WHERE username = ?)
        ''', (st.session_state['username'],))
        
        attendance_data = cursor.fetchall()
        attendance_dates = [datetime.strptime(record[0], '%Y-%m-%d').date() for record in attendance_data]
        
        # 출석체크 버튼
        if st.button("오늘의 출석 체크하기 🗓️", help="누르면 출석이 체크됩니다!"):
            if today not in attendance_dates:
                cursor.execute('''
                    INSERT INTO attendance_logs (user_id, date)
                    VALUES ((SELECT id FROM users WHERE username = ?), ?)
                ''', (st.session_state['username'], today))
                conn.commit()
                st.success("오늘 출석체크 완료! 🎉")
                attendance_dates.append(today)
            else:
                st.info("오늘 이미 출석체크를 완료했습니다.")

        conn.close()
        
        # 현재 월 정보 표시
        current_month = today.strftime("%Y년 %m월")
        st.write(f"### {current_month} 출석체크 현황")
        # 출석 캘린더 생성
        calendar = pd.DataFrame({"출석": ["✅" if date in attendance_dates else "" for date in pd.date_range(start=today.replace(day=1), end=today)]}, 
                                index=pd.date_range(start=today.replace(day=1), end=today))
        
        st.dataframe(calendar)


    # 날짜별 운동 현황 확장
    with st.expander("**날짜별 운동 현황**"):
        
        # 운동 종류 선택
        exercise_type = st.selectbox("조회할 운동 종류를 선택하세요:", ["스쿼트", "사이드레터럴레이즈", "크런치"])
        selected_exercise = exercise_mapping[exercise_type]

        # 데이터베이스에서 운동 기록을 불러오기
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, count FROM exercise_logs
            JOIN users ON exercise_logs.user_id = users.id
            WHERE users.username = ? AND exercise_logs.exercise_type = ?
            ORDER BY date
        ''', (st.session_state['username'], selected_exercise))
        data = cursor.fetchall()
        conn.close()

        # DataFrame으로 변환
        df = pd.DataFrame(data, columns=['Date', 'Count'])
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        # 날짜 범위 설정 (기록이 있는 날의 최소, 최대 범위)
        if not df.empty:
            date_range = pd.date_range(start=df.index.min(), end=df.index.max())
            df = df.reindex(date_range, fill_value=0)  # 날짜 범위 내에서 기록 없는 날짜의 횟수를 0으로 채우기
            df.index.name = 'Date'

            # 막대그래프 생성
            st.bar_chart(df)
        else:
            st.write("아직 선택한 운동 기록이 없습니다.")
else:
    st.warning("로그인 후 마이페이지를 이용하세요.")






# import streamlit as st
# import sqlite3
# import pandas as pd
# from datetime import datetime

# st.title("마이페이지 ☺️")

# if 'username' in st.session_state:
#     st.write()
    
#     with st.expander("**오늘의 운동 기록**"):
#         # 오늘의 날짜 설정
#         today = datetime.today().date()

#         # 오늘의 운동 기록 불러오기
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
        
#         # 운동별 오늘의 기록 가져오기
#         exercises = ["스쿼트", "사이드레터럴레이즈", "크런치"]
#         exercise_counts = {}
#         calories_burned = {}
#         total_calories = 0.0

#         # 운동별 칼로리 소모량 설정
#         calorie_per_rep = {
#             "스쿼트": 0.32,
#             "사이드레터럴레이즈": 0.2,
#             "크런치": 0.3
#         }

#         for exercise in exercises:
#             exercise_mapping = {
#                 "스쿼트": "squat",
#                 "사이드레터럴레이즈": "side_lateral_raise",
#                 "크런치": "crunch"
#             }
#             selected_exercise = exercise_mapping[exercise]

#             cursor.execute('''
#                 SELECT count FROM exercise_logs
#                 JOIN users ON exercise_logs.user_id = users.id
#                 WHERE users.username = ? AND exercise_logs.exercise_type = ? AND date = ?
#             ''', (st.session_state['username'], selected_exercise, today))

#             data = cursor.fetchone()
#             count = data[0] if data else 0
#             exercise_counts[exercise] = count

#             # 각 운동별 칼로리 계산
#             calories = count * calorie_per_rep[exercise]
#             calories_burned[exercise] = calories
#             total_calories += calories

#         conn.close()

#         st.header(f"오늘 소모된 총 칼로리🔥 : **{total_calories:.2f} kcal**", divider="gray")
        
#         # 운동별 기록을 한 줄에 네모 박스로 표시
#         columns = st.columns(len(exercises))
#         for i, (exercise, count) in enumerate(exercise_counts.items()):
#             with columns[i]:
#                 st.markdown(f"""
#                     <div style="border: 2px solid #aaa; padding: 20px; border-radius: 5px; text-align: center;">
#                         <h4>{exercise}</h4>
#                         <p>{count}회</p>
#                         <p>소모 칼로리: {calories_burned[exercise]:.2f} kcal</p>
#                     </div>
#                 """, unsafe_allow_html=True)
                
#     # 출석체크 기능
#     with st.expander("**출석체크**"):
        
#         # 캘린더 표시 및 출석 기록 불러오기
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             SELECT date FROM attendance_logs
#             WHERE user_id = (SELECT id FROM users WHERE username = ?)
#         ''', (st.session_state['username'],))
        
#         attendance_data = cursor.fetchall()
#         attendance_dates = [datetime.strptime(record[0], '%Y-%m-%d').date() for record in attendance_data]
        
#         # 출석체크 버튼
#         if st.button("오늘의 출석 체크하기 🗓️", help="누르면 출석이 체크됩니다!"):
#             if today not in attendance_dates:
#                 cursor.execute('''
#                     INSERT INTO attendance_logs (user_id, date)
#                     VALUES ((SELECT id FROM users WHERE username = ?), ?)
#                 ''', (st.session_state['username'], today))
#                 conn.commit()
#                 st.success("오늘 출석체크 완료! 🎉")
#                 attendance_dates.append(today)
#             else:
#                 st.info("오늘 이미 출석체크를 완료했습니다.")

#         conn.close()
        
#         # 현재 월 정보 표시
#         current_month = today.strftime("%Y년 %m월")
#         st.write(f"### {current_month} 출석체크 현황")
#         # 출석 캘린더 생성
#         calendar = pd.DataFrame({"출석": ["✅" if date in attendance_dates else "" for date in pd.date_range(start=today.replace(day=1), end=today)]}, 
#                                 index=pd.date_range(start=today.replace(day=1), end=today))
        
#         st.dataframe(calendar)


#     # 날짜별 운동 현황 확장
#     with st.expander("**날짜별 운동 현황**"):
        
#         # 운동 종류 선택
#         exercise_type = st.selectbox("조회할 운동 종류를 선택하세요:", ["스쿼트", "사이드레터럴레이즈", "크런치"])
#         selected_exercise = exercise_mapping[exercise_type]

#         # 데이터베이스에서 운동 기록을 불러오기
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute('''
#             SELECT date, count FROM exercise_logs
#             JOIN users ON exercise_logs.user_id = users.id
#             WHERE users.username = ? AND exercise_logs.exercise_type = ?
#             ORDER BY date
#         ''', (st.session_state['username'], selected_exercise))
#         data = cursor.fetchall()
#         conn.close()

#         # DataFrame으로 변환
#         df = pd.DataFrame(data, columns=['Date', 'Count'])
#         df['Date'] = pd.to_datetime(df['Date'])
#         df.set_index('Date', inplace=True)

#         # 날짜 범위 설정 (기록이 있는 날의 최소, 최대 범위)
#         if not df.empty:
#             date_range = pd.date_range(start=df.index.min(), end=df.index.max())
#             df = df.reindex(date_range, fill_value=0)  # 날짜 범위 내에서 기록 없는 날짜의 횟수를 0으로 채우기
#             df.index.name = 'Date'

#             # 막대그래프 생성
#             st.bar_chart(df)
#         else:
#             st.write("아직 선택한 운동 기록이 없습니다.")
# else:
#     st.warning("로그인 후 마이페이지를 이용하세요.")



