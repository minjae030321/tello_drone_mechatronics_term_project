import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import pygame
import threading
from main import FrontEnd  # main.py에 있는 FrontEnd 클래스 import
import pygame.locals as pl
import time

# ============ 드론 인스턴스 생성 및 쓰레드로 실행 ============
class DroneThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.drone = None

    def run(self):
        args = type('Args', (object,), {
            'vsize': None,
            'th': False,
            'tv': True,
            'td': True,
            'tr': True
        })()
        self.drone = FrontEnd(args)
        self.drone.run()

# 드론 조종 키 매핑
command_key_map = {
    'forward': pl.K_UP,
    'back': pl.K_DOWN,
    'left': pl.K_LEFT,
    'right': pl.K_RIGHT,
    'up': pl.K_w,
    'down': pl.K_s,
    'rotate_left': pl.K_a,
    'rotate_right': pl.K_d,
    'follow_me': pl.K_m
}

# 키 누르고 1초 후 떼기
pressed_keys = set()
def simulate_key_press(key, duration=1.0):
    if key is None or key in pressed_keys:
        return
    pressed_keys.add(key)
    drone_instance.keydown(key)
    def release_key():
        drone_instance.keyup(key)
        pressed_keys.remove(key)
    threading.Timer(duration, release_key).start()

# 명령어 실행 함수
def execute_command(cmd):
    if cmd == "takeoff":
        drone_instance.tello.takeoff()
        drone_instance.send_rc_control = True
        drone_instance.fobj.flying = True
    elif cmd == "land":
        drone_instance.tello.land()
        drone_instance.send_rc_control = False
        drone_instance.fobj.flying = False
    elif cmd in command_key_map:
        key = command_key_map[cmd]
        simulate_key_press(key, duration=1.0)

# Gemini API 설정
genai.configure(api_key="Your Gemini API Key")  # 여기에 본인 API 키 입력
model = genai.GenerativeModel("gemini-1.5-flash")

# 명령 전송 함수
def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return
    chat_area.insert(tk.END, f"\U0001F9D1 사용자: {user_input}\n")
    entry.delete(0, tk.END)
    try:
        full_prompt = f"""
너는 Tello 드론을 조종하는 음성 어시스턴트야. 사용자가 입력한 문장을 분석해서
드론 명령어 중 하나로 변환해줘. 가능한 명령어는 다음과 같아:

- takeoff
- land
- forward
- back
- left
- right
- up
- down
- rotate_left
- rotate_right
- stop
- follow_me

예시 입력과 출력:
- "이륙해줘" → takeoff
- "이제 착륙하자" → land
- "앞으로 가" → forward
- "나 따라와" → follow_me

지금 입력: "{user_input}"

너의 출력은 반드시 명령어 한 단어로만 해줘.
"""
        response = model.generate_content(full_prompt)
        result = response.text.strip()
        chat_area.insert(tk.END, f"🤖 Gemini: {result}\n\n")
        execute_command(result)
    except Exception as e:
        chat_area.insert(tk.END, f"⚠️ 오류: {e}\n\n")

# GUI 생성
root = tk.Tk()
root.title("📡 드론 명령어 입력기")
root.geometry("600x600")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=10, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(entry_frame, text="전송", command=send_message)
send_button.pack(side=tk.RIGHT)

# 드론 실행 쓰레드 시작
drone_thread = DroneThread()
drone_thread.start()

# 드론 인스턴스가 준비될 때까지 대기
while drone_thread.drone is None:
    time.sleep(0.1)

drone_instance = drone_thread.drone

# GUI 루프 시작
root.mainloop()
