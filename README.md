## 설치 및 실행 방법
1. 필요한 라이브러리는 모두 requirements.txt에 작성해 두었습니다. 아래 명령으로 빠르게 설치할 수 있습니다.
   ```bash
   pip install -r requirements.txt
   ```
2. 해당 어플리케이션을 실행하기 위해서 터미널에서 아래 명령을 입력합니다.
    ```bash
    create_database.py
    streamlit run 🏠_home.py
    ```

## 프로젝트 설명
실시간 스트리밍을 통해 운동 횟수를 세어주고 자세에 대한 간단한 피드백을 제공하는 웹 애플리케이션입니다.
Streamlit을 프레임워크를 사용하였고, 브라우저 상에서 실시간 스트리밍을 구현하기 위해 WebRTC를 활용했습니다.
WebRTC를 통해 전달받은 frame을 OpenCV가 처리하여 Mediaipipe를 사용하였습니다.

| 파일 및 모듈명                    | 내용                         | 상태       |
|----------------------------------|------------------------------|------------|
| create_database.p                | 데이터베이스 생성 스크립트     | ✅ 완료     |
| utils.py                         | 새로운 계정을 생성 가능        | ✅ 완료     |
| pages/1_✏️_Record.py            | 사용자 운동 기록 입력 페이지    | ✅ 완료     |
| pages/2_🧑🏼‍🦰_MyPage.py            | 개인 운동 기록 조회 페이지      | ✅ 완료     |
| pages/3_🔹_Squats.py            | 스쿼트 카운팅 및 피드백 페이지  | ✅ 완료     |
|pages/4_🔹_Side_Leteral_Raise.py |사이드레터럴레이즈 카운팅 페이지  | ✅ 완료     |
|pages/5_🔹_Crunch.py             | 크런치 카운팅 페이지           | ✅ 완료     |


## 블로그
제 블로그에 [시연동영상과 관련 자료](https://chocolatebuff.tistory.com/15)가 있습니다. 참고하세요!
