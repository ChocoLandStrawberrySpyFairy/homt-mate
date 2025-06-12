
import numpy as np
import cv2

def calculate_angle(a, b, c):
    """
    세 점 (a, b, c) 사이의 각도를 계산하는 함수입니다.
    """
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

def calculate_horizontal_angle(point1, point2):
    """
    두 점 (point1, point2) 사이의 선과 수평선 간의 각도를 계산하는 함수입니다.
    """
    point1, point2 = np.array(point1), np.array(point2)
    radians = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])
    return np.abs(radians * 180.0 / np.pi)



def draw_arc_angle(frame, start, mid, end, angle, radius=20, color=(255, 255, 255), thickness=2):
    """
    각도를 시각적으로 원호로 표시하고, 각도 값을 표시합니다.
    
    Parameters:
    - frame: 이미지를 그릴 프레임
    - start: 시작 점 (ex: 엉덩이)
    - mid: 각도의 중심이 되는 점 (ex: 무릎)
    - end: 끝 점 (ex: 발목)
    - angle: 표시할 각도
    - radius: 원호의 반지름
    - color: 원호와 텍스트의 색상
    - thickness: 원호의 두께
    """
    # 각도의 중심 점을 이미지 좌표로 변환
    mid_point = tuple(np.multiply(mid, [frame.shape[1], frame.shape[0]]).astype(int))
    
    # 시작 점과 끝 점을 이용해 원호의 시작 각도와 끝 각도를 계산
    start_vector = np.array(start) - np.array(mid)
    end_vector = np.array(end) - np.array(mid)
    
    # arctan2를 이용하여 각도를 구하고, radian을 degree로 변환
    start_angle = int(np.degrees(np.arctan2(start_vector[1], start_vector[0])))
    end_angle = int(np.degrees(np.arctan2(end_vector[1], end_vector[0])))
    
    # OpenCV의 원호 함수는 시계방향으로 작동하므로 시작 각도와 끝 각도를 조정
    if start_angle < end_angle:
        start_angle, end_angle = end_angle, start_angle
    
    # 원호 그리기
    cv2.ellipse(frame, mid_point, (radius, radius), 0, end_angle, start_angle, color, thickness)
    
    # 각도 표시
    angle_text_position = (mid_point[0] - 20, mid_point[1] - 20)
    cv2.putText(frame, f"{int(angle)}", angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

    return frame


def draw_horizontal_arc(frame, start, end, angle, radius=16, color=(255, 0, 0), thickness=2, line_color=(200, 200, 200), line_length=50):
    """
    수평선과 어깨-엉덩이 선 사이의 각도를 원호로 표시하고 각도 값을 표시합니다.
    원호는 수평선의 반대 방향인 2사분면에서 시작해 고정된 위치에서 각도에 따라 크기만 변경됩니다.

    파라미터 설명:
    - frame: 이미지를 그릴 프레임
    - start: 선분의 시작 점 (ex: 어깨)
    - end: 선분의 끝 점 (ex: 엉덩이)
    - angle: 표시할 각도 (수평선과의 각도)
    - radius: 원호의 반지름
    - color: 원호와 텍스트의 색상
    - thickness: 원호의 두께
    - line_color: 점선의 색상
    - line_length: 수평선 점선의 길이
    """
    # 엉덩이 점을 중심으로 원호를 그림
    end_point = tuple(np.multiply(end, [frame.shape[1], frame.shape[0]]).astype(int))
    
    # 시작 각도를 180도로 설정해 2사분면에서 원호 시작
    start_angle = 180
    end_angle = start_angle + angle  # 각도에 따라 원호의 끝 위치 조정

    # 원호 그리기
    cv2.ellipse(frame, end_point, (radius, radius), 0, start_angle, end_angle, color, thickness)
    
    # 엉덩이 위치에서 양쪽으로 뻗는 수평선 점선 그리기
    for i in range(-line_length, line_length, 8):  # 엉덩이 기준으로 좌우로 수평선
        cv2.circle(frame, (end_point[0] + i, end_point[1]), 2, line_color, -1, lineType=cv2.LINE_AA)
    
    # 각도 표시
    angle_text_position = (end_point[0] - 40, end_point[1] - 10)
    cv2.putText(frame, f"{int(angle)}", angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

    return frame
