import keyboard
import pygetwindow as gw
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from utils import clear_input_buffer
from login import login_function
from balance import check_balance
from passivity import passivity_lotto
from automatic import automatic_lotto
from winning_result import check_winning_result
from winning_history import winning_history_menu

# .env 로그인 정보 확인하기
def check_env_file():
    env_path = ".env"
    # 1. .env 파일이 존재하는지 확인
    if not os.path.exists(env_path):
        print(".env 파일이 없습니다. 새로 생성합니다.")
        user_id = input("아이디를 입력하세요: ").strip()
        user_pw = input("비밀번호를 입력하세요: ").strip()

        # 2. .env 파일 생성 및 저장
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"LOTTO_USER={user_id}\n")
            f.write(f"LOTTO_PASS={user_pw}\n")
        print(".env 파일이 생성되었습니다.")

    # 3. .env 불러오기
    load_dotenv(env_path)

def main_menu(driver, wait):
    while True:
        print("\n===== 로또 자동화 프로그램 =====")
        print("1. 잔액조회")
        print("2. 수동번호구매")
        print("3. 자동번호구매")
        print("4. 당첨결과조회")
        print("5. 당첨내역상세조회")
        print("esc. 종료")
        print("\n메뉴 키를 눌러 선택하세요 (예: 1~5, esc: 종료)")

        clear_input_buffer()

        result = None
        key_pressed = False

        # 키 입력 대기
        # 잔액조회 코드
        while not key_pressed:
            if keyboard.is_pressed('1'):
                print("잔액조회 선택")
                while keyboard.is_pressed('1'):  # 손을 뗄 때까지 대기
                    time.sleep(0.1)
                    clear_input_buffer()
                result = check_balance(driver, wait)
                key_pressed = True
                if result == 'exit':
                    return
                elif result == 'menu':
                    continue  
        
            # 수동번호구매 코드
            elif keyboard.is_pressed('2'):
                print("수동번호구매 선택")
                while keyboard.is_pressed('2'):  # 손을 뗄 때까지 대기
                    time.sleep(0.1)
                    clear_input_buffer()
                try:
                    chrome_window = gw.getWindowsWithTitle("Chrome")[0]  # 첫 번째 Chrome 창 선택
                    chrome_window.activate()  # 창을 앞으로 가져와서 포커스
                    time.sleep(0.5)  # 안정화를 위해 잠깐 대기
                except Exception:
                    pass
                result = passivity_lotto(driver, wait) # 수동번호구매 함수 호출
                key_pressed = True
                if result == 'exit':
                    return
                elif result == 'menu':
                    continue  
            
            # 자동번호구매 코드
            elif keyboard.is_pressed('3'):
                print("자동번호구매 선택")
                while keyboard.is_pressed('3'):
                    time.sleep(0.1)
                    clear_input_buffer()
                try:
                    chrome_window = gw.getWindowsWithTitle("Chrome")[0]
                    chrome_window.activate()
                    time.sleep(0.5)
                except Exception:
                    pass
                result = automatic_lotto(driver, wait)   # 자동번호구매 함수 호출
                key_pressed = True
                if result == 'exit':
                    return
                elif result == 'menu':
                    continue  
            
            # 당첨결과조회 코드
            elif keyboard.is_pressed('4'):
                print("당첨결과조회 선택")
                while keyboard.is_pressed('4'):  # 손을 뗄 때까지 대기
                    time.sleep(0.1)
                    clear_input_buffer()

                # 여기서 winning_result.py 함수 호출
                result = check_winning_result(driver, wait, my_tickets=[[1, 2, 3, 4, 5, 6]],go_to_mypage=True)  
                key_pressed = True
                if result == 'exit':
                    return
                elif result == 'menu':
                    continue
            
            # 당첨내역상세조회 코드
            elif keyboard.is_pressed('5'):
                print("당첨내역 상세조회 선택")
                while keyboard.is_pressed('5'):
                    time.sleep(0.1)
                    clear_input_buffer()
                result = winning_history_menu()  
                key_pressed = True

                if result == 'exit':
                    return
                elif result == 'menu':
                    continue


            elif keyboard.is_pressed('esc'):
                time.sleep(0.1)
                print("프로그램 종료")
                return  # 완전히 종료

            time.sleep(0.1)  # CPU 과부하 방지

        # check_balance 결과 처리
        if result == 'exit':
            return
        elif result == 'menu':
            continue

def main():
    # .env 확인 및 없으면 생성
    check_env_file()

    # 1. Selenium 드라이버 생성
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # 로그인 실행
    success = login_function(driver, wait)  # 함수 호출해서 로그인
    if not success:
        print('입력하신 로그인 정보가 잘못되었습니다.')
        time.sleep(3)
        driver.quit()
        return  # 로그인 실패 시 종료  

    # 3. 로그인 성공 후 메뉴 실행
    main_menu(driver, wait)

    # 4. 프로그램 종료 시 드라이버 닫기
    driver.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("오류 발생:", e)
        input("엔터를 누르면 프로그램 종료")