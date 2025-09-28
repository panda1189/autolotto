import os, time
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

def handle_alert(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"로그인 실패: {alert.text}")
        alert.accept()  # 확인 버튼 누르기

        # alert이 완전히 사라질 때까지 대기
        WebDriverWait(driver, timeout).until_not(EC.alert_is_present())
        return True
    except:
        return False
    
def login_function(driver, wait):
    while True:  # 성공할 때까지 반복
        # 1. .env 로드
        load_dotenv(override=True)
        user_id = os.getenv("LOTTO_USER")
        user_pw = os.getenv("LOTTO_PASS")

        # 2. 로그인 페이지 열기
        driver.get("https://www.dhlottery.co.kr/user.do?method=login&returnUrl=")
        time.sleep(1)

        # 3. 아이디 / 비밀번호 입력
        id_box = wait.until(EC.presence_of_element_located((By.ID, "userId")))
        id_box.clear()
        id_box.send_keys(user_id + Keys.TAB)

        pw_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
        pw_box.clear()
        pw_box.send_keys(user_pw)

        # 4. 로그인 버튼 클릭
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_common.lrg.blu"))).click()

        # 5. 버튼 클릭 직후 alert 처리
        if handle_alert(driver):
            # alert이 있었다 → 실패 → 새 입력 받기
            user_id = input("아이디: ").strip()
            user_pw = input("비밀번호: ").strip()
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f"LOTTO_USER={user_id}\n")
                f.write(f"LOTTO_PASS={user_pw}\n")
            continue  # 다시 시도

        # 6. 성공 확인 (로그아웃 버튼 존재 여부)
        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn_common.sml[href*='logout']"))
            )
            print("로그인 성공")

            # 성공한 정보로 .env 갱신
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f"LOTTO_USER={user_id}\n")
                f.write(f"LOTTO_PASS={user_pw}\n")

            return True

        except TimeoutException:
            print("로그인 여부 확인 실패 (로그아웃 버튼 미탐색)")
            return False