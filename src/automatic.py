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

    if result == "success" and purchased_tickets:
        print(f"\n자동 로또 {len(purchased_tickets)}매 구매 완료!\n")
        # 수동구매와 동일하게 티켓별 출력
        for idx, ticket in enumerate(purchased_tickets, start=1):
            print(f"{idx}번째 로또 : {ticket}")
    else:
        print("자동 로또 구매 실패")