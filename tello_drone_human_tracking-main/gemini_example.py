import google.generativeai as genai

# ① Gemini API 키 설정 (자신이 발급받은 키로 교체)
genai.configure(api_key="AIzaSyCDinpHndIhYsRwBoKF0Rbc503M90nNq5g")

# ② 사용할 LLM 모델 지정
model = genai.GenerativeModel("gemini-1.5-flash")

# ③ 변환 대상 명령어 목록
VALID_COMMANDS = [
    "takeoff", "land",
    "forward", "back",
    "left", "right",
    "up", "down",
    "rotate_left", "rotate_right",
    "stop", "follow_me"
]

def translate_to_control_keyword(user_text: str) -> str:
    """
    한글(또는 자유 텍스트) 명령을 주면,
    VALID_COMMANDS 중 하나로 변환해 반환한다.
    """
    # ④ 프롬프트 문자열 구성
    prompt = f"""
너는 Tello 드론을 조종하는 어시스턴트야. 
아래 명령어 목록 중 하나만 정확히 출력해줘:

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

지금 입력: "{user_text}"
"""
    # ⑤ LLM 호출
    response = model.generate_content(prompt)
    result = response.text.strip()

    # ⑥ 반환값 검증
    if result in VALID_COMMANDS:
        return result
    else:
        return "invalid_command"

if __name__ == "__main__":
    # 테스트용 예제
    test_inputs = [
        "이륙시켜 줘",
        "뒤로 가",
        "높이 올라",
        "나를 따라와",
        "착륙해",
        "왼쪽으로 살짝"
    ]

    for txt in test_inputs:
        keyword = translate_to_control_keyword(txt)
        print(f"입력: {txt!r}  →  변환 결과: {keyword!r}")
