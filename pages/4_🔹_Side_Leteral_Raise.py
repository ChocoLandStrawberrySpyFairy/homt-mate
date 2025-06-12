import av
import streamlit as st
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
import cv2
import mediapipe as mp
import numpy as np
from utils import *  # utils 모듈에서 함수 가져오기

# Mediapipe Pose 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

st.title("Side Leteral Raise Assist")
st.subheader("제니의 직각어깨, 갖고 싶지 않니? 😎 ")

# 푸쉬업 카운트와 동작 상태 초기화
correct_counter = 0
wrong_counter = 0
stage = None  # 'down' 또는 'up' 상태 저장
evaluation = None  # 'correct' 또는 'wrong'로 평가

# 비디오 프레임을 처리하고 카운팅하는 콜백 함수
def video_frame_callback(frame: av.VideoFrame):
    global correct_counter, wrong_counter, stage, evaluation
    
    frame = frame.to_ndarray(format="rgb24")  # 비디오 프레임을 RGB로 변환
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # 포즈 추출
    results = pose.process(image)
    
    # 랜드마크가 감지된 경우
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # 왼쪽 어깨, 팔꿈치, 골반 좌표 추출
        landmarks = results.pose_landmarks.landmark
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, 
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, 
               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        
        shoulder_angle = calculate_angle(elbow, shoulder, hip)
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        
        
        if shoulder_angle > 85:  # 팔이 올라간 상태
            stage = "up"
            if 130<= elbow_angle <= 180:
                evaluation = "correct"
            else:
                evaluation = "wrong"
                cv2.putText(image, "Strighten Your Elblow 'Moderately'" , 
                        (10, 100),  # 화면의 적절한 위치에 메시지 표시
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                
        elif shoulder_angle < 50 and stage == 'up':  # 팔을 내려간 상태
            stage = "down"
            if evaluation == "correct":
                correct_counter += 1
            else:
                wrong_counter += 1
            evaluation = None  # 평가 초기화
        
            
        # 각도와 횟수를 이미지에 표시
        # cv2.putText(image, f"Shoulder Angle: {int(shoulder_angle)}", 
        #             tuple(np.multiply(shoulder, [image.shape[1], image.shape[0]]).astype(int)),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        
        # cv2.putText(image, f"Elbow Angle: {int(elbow_angle)}", 
        #             tuple(np.multiply(elbow, [image.shape[1], image.shape[0]]).astype(int)),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        
        cv2.putText(image, 'Correct SLR Count: ' + str(correct_counter), 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
        cv2.putText(image, 'Wrong SLR Count: ' + str(wrong_counter), 
                    (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
        # 어깨 각도 그리기 (호로 표시)
        image = draw_arc_angle(image, hip, shoulder, elbow, shoulder_angle, color=(0, 255, 0))

        # 팔꿈치 각도 그리기 (호로 표시)
        image = draw_arc_angle(image, shoulder, elbow, wrist, elbow_angle, color=(0, 255, 0))

    
    return av.VideoFrame.from_ndarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), format="rgb24")

# WebRTC 스트리머 초기화
ctx = webrtc_streamer(
    key="LateralRaise-pose-analysis",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": {"width": {'min': 720, 'ideal': 720}, "height": {'min': 480, 'ideal': 480}}, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=600)
)

st.subheader("")

tab1, tab2, tab3 = st.tabs([" **운동 소개** "," **올바른 자세** "," **주의사항** "])

with tab1: 
    st.write("""
    ### 📌 사이드 레터럴 레이즈란?
    사이드 레터럴 레이즈는 **어깨 근육을 강화**하는 운동으로, 특히 **측면 삼각근**에 효과적입니다.
    이 운동은 팔을 들어올리며 **어깨의 안정성과 모양을 개선**하는 데 도움을 줍니다.
    """)
    
with tab2:
    st.write("""
    ### 📌 올바른 자세
    1. **기본 자세**: 발을 엉덩이 너비로 벌리고 서서, 팔은 양옆으로 늘어뜨립니다.
    2. **올리기 동작**: 팔을 옆으로 들어올리며 어깨 높이까지 올립니다. 이때 팔꿈치를 약간 구부려 편안하게 유지합니다.
    3. **내리기 동작**: 어깨에 긴장을 유지하며 천천히 팔을 내립니다. 무리하지 않도록 조절하세요.
    4. **호흡**: 팔을 들어올릴 때 숨을 내쉬고, 내릴 때 들이마십니다.
    """)

with tab3:    
    st.write("""
    ### 📌 주의사항
    - **어깨 긴장 유지**: 어깨에 과도한 힘이 들어가지 않도록 부드럽게 올립니다. 어깨나 목의 긴장이 느껴지면 자세를 다시 점검합니다.
    - **팔꿈치 각도 유지**: 팔꿈치를 과도하게 굽히거나 펴지 않도록 주의합니다. 팔꿈치를 약간 구부린 상태로 유지하는 것이 좋습니다.
    - **과도한 무게 피하기**: 무리한 무게는 어깨 부상의 원인이 될 수 있습니다. 무게를 점진적으로 증가시키며 올바른 자세를 유지하세요.
    """)
    

