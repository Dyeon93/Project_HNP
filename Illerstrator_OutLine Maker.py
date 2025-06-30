import os
import time
import pyautogui
import subprocess
import pyperclip  # 클립보드를 사용하여 한글 입력 문제 해결

def open_illustrator():
    """ Illustrator 실행 """
    illustrator_path = "C:/Program Files/Adobe/Adobe Illustrator 2024/Support Files/Contents/Windows/Illustrator.exe"
    subprocess.Popen([illustrator_path])
    time.sleep(10)  # Illustrator 실행 대기

def open_file_with_illustrator(file_path):
    """ 파일을 Illustrator로 직접 열기 """
    subprocess.Popen([file_path], shell=True)
    time.sleep(3)  # 파일이 열릴 때까지 대기

def paste_text(text):
    """ 클립보드를 사용하여 한글 입력 문제 해결 """
    pyperclip.copy(text)
    time.sleep(1)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

def process_illustrator_files(folder_path):
    # 폴더 내 모든 .ai 파일 찾기
    ai_files = [f for f in os.listdir(folder_path) if f.endswith(".ai")]

    # Illustrator 활성화
    pyautogui.hotkey("alt", "tab")
    time.sleep(3)

    for file in ai_files:
        file_path = os.path.join(folder_path, file)
        file_name = os.path.splitext(file)[0]  # 확장자 제거한 파일명
        output_ai = f"{file_name}_OL.ai"
        output_pdf = f"{file_name}_OL.pdf"

        # Illustrator에서 직접 파일 열기
        open_file_with_illustrator(file_path)

        # 윈도우가 이전크기로 돌아가는 문제 해결
        pyautogui.hotkey('win', 'up')
        time.sleep(1)

        # 파일이 정상적으로 열릴 수 있도록 추가 대기
        time.sleep(3)

        # 모두 선택 (Ctrl + A)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(1)

        # 심볼 연결 해제 (메뉴 클릭 방식)
        pyautogui.click(x=1508, y=561)  # 좌표 조정 필요
        time.sleep(1)

        # 아웃라인 변환 (Shift + Ctrl + O)
        pyautogui.hotkey("shift", "ctrl", "o")
        time.sleep(1)

        # 다른 이름으로 저장 (AI 파일)
        pyautogui.hotkey("ctrl", "shift", "s")
        time.sleep(1)
        paste_text(output_ai)  # 한글 입력 문제 해결
        pyautogui.hotkey("alt", "s")
        time.sleep(1)
        pyautogui.click(x=1073, y=812)  # 좌표 조정 필요
        time.sleep(2)

        # 다른 이름으로 저장 (PDF 파일)
        pyautogui.hotkey("ctrl", "shift", "s")
        time.sleep(1)
        paste_text(output_pdf)  # 한글 입력 문제 해결
        pyautogui.hotkey("alt", "s")
        time.sleep(1)
        pyautogui.click(x=1073, y=812)  # 좌표 조정 필요
        time.sleep(2)

        # 닫기 (Ctrl + W)
        pyautogui.hotkey("ctrl", "w")
        time.sleep(2)

        # 타이머
        lt = time.localtime()

        print(f"✅ Processed: {file} : {lt.tm_year}.{lt.tm_mon}.{lt.tm_mday} {lt.tm_hour}:{lt.tm_min}:{lt.tm_sec}")

if __name__ == "__main__":
    folder_path = "C:/Users/PC-KDY/Desktop/아웃라인 따는 폴더"  # AI 파일이 있는 폴더 경로
    open_illustrator()
    process_illustrator_files(folder_path)
