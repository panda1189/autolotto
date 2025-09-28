import keyboard
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import clear_input_buffer


def check_balance(driver, wait):
    try:
        # 마이페이지 또는 잔액이 표시되는 요소 대기 후 가져오기
        balance_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.information li.money a strong")))
        balance = balance_element.text
        print(f"현재 남은 잔액은 {balance} 입니다.")
    except:
        print("잔액 조회 중 오류가 발생했습니다")
        return

    print("메뉴로 돌아가시려면 '1', 종료하시려면 'ESC' 키를 누르세요.")

    while True:
        # '1' 키를 누르면 메뉴로 돌아감
        if keyboard.is_pressed('1'):
            print("메뉴로 돌아갑니다.")
            while keyboard.is_pressed('1'):   # 손 뗄 때까지 대기
                time.sleep(0.1)
                clear_input_buffer()
            return 'menu'
        # 'esc' 키를 누르면 프로그램 종료
        elif keyboard.is_pressed('esc'):
            print("프로그램 종료")
            while keyboard.is_pressed('esc'):  # 손 뗄 때까지 대기
                time.sleep(0.1)
                clear_input_buffer()
            return 'exit'