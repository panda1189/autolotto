import sys
import keyboard
import pygetwindow as gw
import time
from utils import clear_input_buffer

from buy_lotto import buy_lotto_manual

def passivity_lotto(driver, wait):
    clear_input_buffer()
    # 구매 매수 입력
    while True:
        try:
            tickets = int(input("(최대 5매) 수동으로 구매하실 로또의 매수를 입력해주세요. : "))
            if tickets <= 0 or tickets > 5:
                print("1 ~ 5 매수 범위내로 입력해주세요.")
                continue
            break
        except ValueError:
            print("숫자만 입력 가능합니다.")

    all_tickets = []

    for i in range(1, tickets + 1):
        print(f"\n*** {i}번째 로또 번호 입력 ***")
        print("*** 숫자범위 1~45, 숫자는 중복불가합니다. ***")
        ticket_nums = []
        while len(ticket_nums) < 6:
            try:
                num = int(input(f"{len(ticket_nums)+1}번째 숫자 : "))
                if num < 1 or num > 45:
                    print("1~45 범위의 숫자만 입력 가능합니다.")
                elif num in ticket_nums:
                    print("중복된 숫자는 입력할 수 없습니다.")
                else:
                    ticket_nums.append(num)
            except ValueError:
                print("숫자만 입력 가능합니다.")
        all_tickets.append(ticket_nums)

    try:
        chrome_window = gw.getWindowsWithTitle("Chrome")[0]
        chrome_window.activate()  # 브라우저 앞으로 가져오기
        time.sleep(0.5)          # 안정화를 위해 잠시 대기
    except Exception:
        pass

    result = buy_lotto_manual(driver, wait, all_tickets) # 입력한 번호를 구매 실행

    if result == "success":
        print(f"{len(all_tickets)}매 수동 로또 구매 완료")
    else:
        print("수동 로또 구매 실패")

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