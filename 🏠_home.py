# home.py
import streamlit as st
import sqlite3
import hashlib

# 비밀번호 암호화 함수
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 데이터베이스 연결 함수
def connect_db():
    return sqlite3.connect('database.db')

# 회원가입 함수
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        st.success("회원가입 성공! 로그인해 주세요.")
    except sqlite3.IntegrityError:
        st.error("이미 존재하는 사용자 이름입니다.")
    finally:
        conn.close()

# 로그인 함수
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

# 메인 페이지
st.title("🏋️ 홈트메이트 ")

# 로그인 또는 회원가입 선택
menu = st.sidebar.selectbox("메뉴 선택", ["Home", "로그인", "회원가입"])

if menu == "Home":
    st.write("")
    st.subheader("졸업 프로젝트로 진행한 운동 기록 & 카운팅 앱입니다.")
    
    st.write("이 애플리케이션은 다음과 같은 기능을 제공합니다:")
    
    # 기능 소개
    st.markdown("""
    - **실시간 운동 카운트**: 스쿼트, 사이드 래터럴 레이즈, 크런치와 같은 운동의 실시간 횟수를 세어줍니다.
    - **개인 맞춤 기록**: 운동 횟수와 날짜별로 기록을 저장하여 개인화된 기록 페이지에서 조회할 수 있습니다.
    - **자세 교정 피드백**: 운동 자세가 정확하지 않으면 교정을 위한 피드백을 제공합니다.
    - **사용자 관리**: 로그인과 회원가입 기능을 통해 개인화된 경험을 제공합니다.
    """)

    st.write("지금 바로 운동을 시작해보세요! 좌측 메뉴에서 **로그인** 또는 **회원가입** 하여 개인화된 서비스를 이용하세요.")
    

elif menu == "회원가입":
    st.write("")
    st.subheader("회원가입하여 홈트메이트의 멤버가 되어주세요!")
    st.write("")
    new_username = st.text_input("사용자 이름")
    new_password = st.text_input("비밀번호", type="password")
    if st.button("회원가입"):
        if new_username and new_password:
            register_user(new_username, new_password)
        else:
            st.error("모든 필드를 입력해 주세요.")

elif menu == "로그인":
    st.write("")
    st.subheader("로그인해서 운동 기록을 남겨보세요!")
    st.write("")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")
    if st.button("LogIn"):
        user = login_user(username, password)
        if user:
            st.success(f"환영합니다, {username}님!")
            st.session_state['username'] = username
            st.session_state['logged_in'] = True
        else:
            st.error("잘못된 사용자 이름 또는 비밀번호입니다.")