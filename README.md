# 🛸 Tello Drone Mechatronics Term Project

이 프로젝트는 **음성 인식 → LLM(Gemini) → 드론 제어**까지 전체 파이프라인을 구현한 메카트로닉스 텀 프로젝트입니다.  
사용자는 자연어로 드론에게 명령을 내릴 수 있으며, 드론은 객체를 인식하고 추적하거나 다양한 명령에 응답합니다.

---

## 📌 주요 기능

- 🎯 **YOLOv8 기반 사람 인식 및 추적**
- 🎙️ **음성 명령을 Gemini LLM으로 처리하여 드론 제어 명령 생성**
- 🕹️ **명령을 pygame 키 시뮬레이션으로 변환하여 Tello 드론 제어**
- 🔁 **실시간 비디오 스트리밍, RC 명령 전송, 자동 모드/수동 모드 전환**

---

## 🧩 시스템 구성

[사용자 음성 입력]
↓
[STT (Speech-to-Text)]
↓
[Gemini LLM]
↓
["forward", "takeoff", ...]
↓
[command_key_map → simulate_key_press()]
↓
[FrontEnd 클래스 → 드론 제어]


---

## 🗂️ 주요 모듈 설명

### `DroneThread`
- `threading.Thread`를 상속한 드론 제어 전용 스레드
- GUI/LLM과 독립적으로 실행되며, `FrontEnd.run()`을 통해 루프 시작

### `FrontEnd`
- 메인 루프를 담당하며, 키 이벤트와 프레임 처리를 수행
- YOLO 모델 로딩 및 실시간 영상 분석 처리 포함

### `simulate_key_press(key, duration=1.0)`
- 특정 키를 누른 후 일정 시간(기본 1초) 뒤에 자동으로 떼는 기능
- `keydown()`과 `keyup()` 메서드를 통해 실제 조작처럼 동작

---

🧠 사용 예시
🔧 키 명령 시뮬레이션
python
복사
편집
command = "forward"
key = command_key_map[command]  # pl.K_UP
simulate_key_press(key)         # 1초간 전진 후 자동 정지
🛠️ 설치 및 실행
1. 환경 세팅
bash
복사
편집
pip install -r requirements.txt
2. 실행
bash
복사
편집
python final2.py
✅ 드론은 Tello Wi-Fi에 연결된 상태여야 합니다.


