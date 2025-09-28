import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


def buy_lotto_manual(driver, wait, all_tickets):
    try:
        existing_windows = driver.window_handles  

        # 새 창 열기
        driver.execute_script("window.open('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40');")

        # 새 창 포커싱
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrm_tab")))

        # 수동 번호 선택
        for ticket in all_tickets:
            for num in ticket:  # 예: [29, 17, 7, 20, 33, 40]
                checkbox_id = f"check645num{num}"  # 그대로 숫자 붙이면 됨
                try:
                    label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"label[for='{checkbox_id}']")))
                    label.click()
                except Exception as e:
                    print(f"{num} 클릭 실패:", e)

        # 확인 버튼 클릭
            try:
                confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='확인' and not(@id='btnBuy')]")))
                driver.execute_script("arguments[0].click();", confirm_btn)  # ✅ JS 클릭만 사용
                time.sleep(2)
            except Exception as e:
                print("세트 확인 버튼 클릭 실패:", e)

        # 구매하기 버튼 클릭
        buy_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnBuy")))
        driver.execute_script("arguments[0].click();", buy_btn)  # JS 클릭 보강
        time.sleep(2)

        # 결제 확인 레이어 대기 & 확인 클릭
        wait.until(EC.visibility_of_element_located((By.ID, "popupLayerConfirm")))
        popup_ok = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@id='popupLayerConfirm' and not(contains(@style,'display:none'))]""//input[@type='button' and normalize-space(@value)='확인']")))
        driver.execute_script("arguments[0].click();", popup_ok)

        # 레이어 사라질 때까지 대기
        wait.until(EC.invisibility_of_element_located((By.ID, "popupLayerConfirm")))

        # 잔액 부족 / 제한 알림 처리
        try:
            alert_ok = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='popupLayerAlert' and not(contains(@style,'display:none'))]//input[@value='확인']")))
            driver.execute_script("arguments[0].click();", alert_ok)
            print("잔액이 부족합니다.")
            return "fail"
        except TimeoutException:
            pass

        # 성공시 로딩바(#execBuy) 사라질 때까지 대기
        try:
            WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, "execBuy")))
        except TimeoutException:
            pass

        # 6) 구매내역 확인 레이어 닫기
        try:
            receipt_ok = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "closeLayer")))
            driver.execute_script("arguments[0].click();", receipt_ok)
        except TimeoutException:
            print("구매내역 확인 레이어가 뜨지 않았습니다 (이미 닫혔을 수 있음)")
        
        print("구매한 번호:", all_tickets)
        return "success" 
        
    except TimeoutException as e:
        print("오류 발생! 구매 루틴 중 문제:", e)
        return "fail"

    finally:
        #성공/실패 상관없이 실행
        try:
            driver.close()
        except:
            pass

        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "method=main" in driver.current_url:
                driver.refresh()
                break