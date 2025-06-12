import av
import streamlit as st
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
import cv2
import mediapipe as mp
import numpy as np
from utils import *

# Mediapipe Pose 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

st.title("Crunch Asist")
st.subheader(" 배에 초콜릿을 만들어보자! 🍫")

# 크런치 카운트와 동작 상태 초기화
correct_counter = 0
stage = None  # 'down' 또는 'up' 상태 저장

# 비디오 프레임을 처리하고 카운팅하는 콜백 함수
def video_frame_callback(frame: av.VideoFrame):
    global correct_counter, stage

    frame = frame.to_ndarray(format="rgb24")
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # 포즈 추출
    results = pose.process(image)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        landmarks = results.pose_landmarks.landmark

        # 어깨, 골반, 무릎 좌표 추출
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        # 크런치 동작을 위해 어깨-골반-무릎 각도 계산
        crunch_angle = calculate_angle(shoulder, hip, knee)
        knee_angle = calculate_angle(hip, knee, ankle)
        
        # 크런치 동작 감지 (앉았다가 다시 내려가는 동작)
        if knee_angle <= 90:
            cv2.putText(image, "You Can Do it! More Higher!", 
                        (10, 60),  # 화면의 적절한 위치에 메시지 표시
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)    
            if crunch_angle > 110:  # 상체가 내려간 상태
                stage = "down"
            elif crunch_angle < 105 and stage == "down":  # 상체가 올라간 상태
                stage = "up"
                correct_counter += 1  # 올바른 횟수 증가
            
        # 각도와 크런치 횟수를 이미지에 표시
        # cv2.putText(image, f"Crunch Angle: {int(crunch_angle)}", 
        #             tuple(np.multiply(hip, [image.shape[1], image.shape[0]]).astype(int)),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(image, f"Knee Angle: {int(knee_angle)}", 
        #             tuple(np.multiply(knee, [image.shape[1], image.shape[0]]).astype(int)),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.putText(image, 'Correct Crunch Count: ' + str(correct_counter), 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # 허리 각도 그리기 (호로 표시)
        image = draw_arc_angle(image, shoulder, hip, knee, crunch_angle, color=(0, 255, 0))


    return av.VideoFrame.from_ndarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), format="rgb24")

# WebRTC 스트리머 초기화
ctx = webrtc_streamer(
    key="Crunch-pose-analysis",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": {"width": {'min': 720, 'ideal': 720}, "height": {'min': 480, 'ideal': 480}}, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=600)
)




st.subheader("")
tab1, tab2, tab3 = st.tabs([" **운동 소개** "," **올바른 자세** "," **주의사항** "])

with tab1: 
    st.write("""
    ### 📌 크런치란?
    크런치는 **복근**을 집중적으로 단련하는 운동으로,
    **코어 근력을 강화**하고 **복부 지방을 줄이는 것에** 효과적입니다.
    """)
    
with tab2:
    st.write("""
    ### 📌 올바른 자세
    1. **기본 자세**: 바닥에 등을 대고 누워 무릎을 구부리고, 발은 바닥에 댑니📌다.
    2. **복근 수축**: 복근에 힘을 주며 상체를 들어올립니다. 턱을 가슴 쪽으로 당기지 않고, 시선은 천장을 향하게 합니다.
    3. **내리기 동작**: 상체를 천천히 바닥에 내려놓으며 복근의 긴장을 유지합니다.
    4. **호흡**: 상체를 들어올릴 때 숨을 내쉬고, 내릴 때 들이마십니다.
    """)

with tab3:    
    st.write("""
    ### 📌 주의사항
    - **목 긴장 피하기**: 상체를 들어올릴 때 목에 힘이 들어가지 않도록 합니다. 손으로 머리를 당기지 말고, 복근의 힘으로만 상체를 들어올리세요.
    - **너무 높은 범위로 들어올리지 않기**: 상체를 지나치게 높이 들어 올리지 말고, 복근의 수축을 유지할 수 있는 높이까지만 들어올립니다.
    - **등의 아치 피하기**: 허리가 바닥에서 떨어지지 않도록 주의합니다. 특히 허리 아치가 과도하게 생기지 않도록 하세요.
    """)
    
