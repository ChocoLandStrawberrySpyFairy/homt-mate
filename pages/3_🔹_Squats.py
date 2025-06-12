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

st.title("Squats Asist")
st.subheader("체력 기르기는 역시 스쿼트지!  💪")

# 카운터 초기화
correct_counter = 0  # 세션에 저장하지 않음
wrong_counter = 0
stage = None
evaluation = None

# 비디오 프레임을 처리하고 카운팅하는 콜백 함수
def video_frame_callback(frame: av.VideoFrame):
    global correct_counter, wrong_counter, stage, evaluation

    frame = frame.to_ndarray(format="rgb24")
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # 포즈 추출
    results = pose.process(image)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        landmarks = results.pose_landmarks.landmark
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        knee_angle = calculate_angle(hip, knee, ankle)
        waist_hangle = calculate_horizontal_angle(shoulder, hip)

        if knee_angle < 90:
            stage = "down"
            if 50 <= waist_hangle:
                evaluation = "correct"
            else:
                evaluation ="wrong"
                cv2.putText(image, "Bending Waist Too Much !!", 
                        (10, 100),  # 화면의 적절한 위치에 메시지 표시
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                    
        elif knee_angle > 160 and stage == "down":
            stage = "up"
            if evaluation == "correct":
                correct_counter += 1
            else:
                wrong_counter += 1
                evaluation = None


        # 프레임에 스쿼트 횟수와 각도 표시
        # cv2.putText(image, f"Waist Angle: {int(waist_hangle)}", 
        #             tuple(np.multiply(hip, [image.shape[1], image.shape[0]]).astype(int)),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        # cv2.putText(image, f"Knee Angle: {int(knee_angle)}", 
        #             tuple(np.multiply(knee, [image.shape[1], image.shape[0]]).astype(int)),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.putText(image, 'Correct Count: ' + str(correct_counter), 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(image, 'Wrong Count: ' + str(wrong_counter), 
                    (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # 무릎 각도 그리기 (호로 표시)
        image = draw_arc_angle(image, hip, knee, ankle, knee_angle, color=(0, 255, 0))

        # 허리 각도 그리기 (수평선과의 각도)
        image = draw_horizontal_arc(image, shoulder, hip, waist_hangle, radius=16, color=(0, 255, 0), line_color=(0, 255, 0), line_length=50)
    
    return av.VideoFrame.from_ndarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), format="rgb24")


# WebRTC 스트리머 초기화
webrtc_streamer(
    key="Squats-pose-analysis",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": {"width": {'min': 720, 'ideal': 720}, "height": {'min': 480, 'ideal': 480}}, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=600)
) 

st.subheader("")

tab1, tab2, tab3 = st.tabs([" **운동 소개** "," **올바른 자세** "," **주의사항** "])
    
with tab1: 
    
    st.write("""
    ### 📌 맨몸 스쿼트란?
    맨몸 스쿼트는 **하체 근력**을 키우고 **전신 근육**을 단련하는 운동으로,
    별도의 장비 없이 자신의 체중을 이용해 수행합니다.
    주로 **허벅지, 엉덩이, 코어 근육을 강화**하는 데 효과적이며, **균형감과 유연성**에도 도움을 줍니다.""")
    
with tab2:     
    st.write("""
    ### 📌 올바른 자세
    1. **기본 자세**: 발은 어깨너비로 벌리고, 발끝은 약간 바깥쪽을 향하게 합니다. 등을 곧게 펴고, 무릎이 발끝을 벗어나지 않도록 합니다.
    2. **하강 동작**: 허리를 굽히지 않고 엉덩이를 뒤로 밀면서 천천히 앉습니다. 무릎이 발끝을 넘지 않게 주의하면서, 허벅지가 바닥과 평행이 될 때까지 내려갑니다.
    3. **상승 동작**: 발뒤꿈치를 지탱하며, 엉덩이와 허벅지의 힘으로 일어섭니다. 이때 무릎이 흔들리지 않게 유지하는 것이 중요합니다.
    4. **호흡**: 내려갈 때 숨을 들이마시고, 올라올 때 내쉽니다.
    """)

with tab3:    
    st.write("""
    ### 📌 스쿼트 시 주의사항
    - **무릎 위치**: 무릎이 발끝을 넘지 않도록 하여 관절에 무리가 가지 않도록 합니다.
    - **허리 자세**: 등을 둥글게 말거나 허리를 과도하게 굽히지 않습니다. 허리를 중립 자세로 유지하는 것이 중요합니다.
    - **균형 유지**: 체중은 발뒤꿈치에 실어주어 균형을 유지합니다. 발가락 쪽으로 체중이 쏠리지 않게 주의하세요.
    - **과도한 깊이 조절**: 너무 깊게 앉지 않도록 자신의 유연성과 체력에 맞는 깊이로 조절하세요. 특히 무릎이나 허리에 불편함이 느껴질 경우, 무리하지 않는 것이 중요합니다.
    - **속도**: 너무 빠르게 내려가지 않도록 천천히 통제된 동작으로 수행합니다. 특히 초보자의 경우, 속도를 조절해 안정성을 높입니다.
    """)

