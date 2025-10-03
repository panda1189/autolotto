import pygetwindow as gw
import time
from auto_lotto import buy_lotto_automatic   # ← 함수 이름 그대로 사용

def automatic_lotto(driver, wait, ui):
    while True:
        try:
            tickets = int(ui.ui_input("(최대 5매) 자동구매 매수를 입력해주세요: "))
            if tickets <= 0 or tickets > 5:
                print("1 ~ 5 매수 범위내로 입력해주세요.")
                continue
            break
        except ValueError:
            print("숫자만 입력 가능합니다.")

    try:
        chrome_window = gw.getWindowsWithTitle("Chrome")[0]
        chrome_window.activate()
        time.sleep(0.5)
    except Exception:
        pass

    result, purchased_numbers = buy_lotto_automatic(driver, wait, tickets)

    if result == "success" and purchased_numbers:
        print(f"\n✅ 자동 로또 {tickets}매 구매 완료!\n")

        # 6개씩 끊어서 출력
        for idx in range(tickets):
            start = idx * 6
            end = start + 6
            ticket_nums = purchased_numbers[start:end]
            print(f"{idx+1}번째 로또 : {ticket_nums}")
    else:
        print("자동 로또 구매 실패")