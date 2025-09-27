import sys
import keyboard
import pygetwindow as gw
import time
from auto_lotto import buy_lotto_automatic
from utils import clear_input_buffer

def automatic_lotto(driver, wait):

    clear_input_buffer()

    # 구매 매수 입력
    while True:
        try:
            tickets = int(input("(최대 5매) 자동으로 구매하실 로또의 매수를 입력해주세요. : "))
            if tickets <= 0 or tickets > 5:
                print("1 ~ 5 매수 범위내로 입력해주세요.")
                continue
            break
        except ValueError:
            print("숫자만 입력 가능합니다.")

    try:
        chrome_window = gw.getWindowsWithTitle("Chrome")[0]
        chrome_window.activate()   # 브라우저 앞으로 가져오기
        time.sleep(0.5)            # 안정화를 위해 잠시 대기
    except Exception:
        pass

    # 자동 구매 실행
    result = buy_lotto_automatic(driver, wait, tickets)
    if result == "success":
        print(f"{tickets}매 자동 로또 구매 완료")
    else:
        print("자동번호구매 실패")

    print("\n메뉴로 돌아가시려면 '1', 종료하시려면 'ESC' 키를 누르세요.")
    while True:
        if keyboard.is_pressed('1'):
            while keyboard.is_pressed('1'):
                time.sleep(0.1)
                clear_input_buffer()
            return "menu"   
        elif keyboard.is_pressed('esc'):
            while keyboard.is_pressed('esc'):
                time.sleep(0.1)
                clear_input_buffer()
            return "exit" 
        time.sleep(0.1) # CPU 과부하 방지