import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import pygame
import threading
import speech_recognition as sr
import pygame.locals as pl
import time
from main import FrontEnd

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
    'takeoff': pl.K_t,
    'land': pl.K_l,
    'forward': pl.K_UP,
    'back': pl.K_DOWN,
    'left': pl.K_LEFT,
    'right': pl.K_RIGHT,
    'up': pl.K_w,
    'down': pl.K_s,
    'rotate_left': pl.K_a,
    'rotate_right': pl.K_d,
    'stop': None,
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

# Gemini 설정
genai.configure(api_key="Your Gemini API Key")
model = genai.GenerativeModel("gemini-1.5-flash")

# 명령 처리
def process_command(text):
    chat_area.insert(tk.END, f"\U0001F9D1 사용자: {text}\n")
    try:
        full_prompt = f"""
너는 Tello 드론을 조종하는 어시스턴트야. 입력을 아래 명령어 중 하나로 변환해줘:

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

지금 입력: "{text}"

출력은 명령어 하나만!
"""
        response = model.generate_content(full_prompt)
        result = response.text.strip()
        chat_area.insert(tk.END, f"🤖 Gemini: {result}\n\n")

        if result in command_key_map:
            key = command_key_map[result]
            simulate_key_press(key, duration=1.0)
        else:
            chat_area.insert(tk.END, "⚠️ 유효하지 않은 명령입니다.\n\n")
    except Exception as e:
        chat_area.insert(tk.END, f"⚠️ 오류: {e}\n\n")

# STT 실행
def start_stt():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_area.insert(tk.END, "🎤 말하세요...\n")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="ko-KR")
            process_command(text)
        except Exception as e:
            chat_area.insert(tk.END, f"⚠️ STT 실패: {e}\n\n")

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
entry.bind("<Return>", lambda event: process_command(entry.get()) or entry.delete(0, tk.END))

send_button = tk.Button(entry_frame, text="전송", command=lambda: process_command(entry.get()) or entry.delete(0, tk.END))
send_button.pack(side=tk.RIGHT)

stt_button = tk.Button(root, text="🎙️ STT 명령어 말하기", command=start_stt)
stt_button.pack(pady=10)

# 드론 실행 쓰레드 시작
drone_thread = DroneThread()
drone_thread.start()

# 드론 준비 대기
while drone_thread.drone is None:
    time.sleep(0.1)
drone_instance = drone_thread.drone

# 루프
root.mainloop()
