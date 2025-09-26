import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from utils import clear_input_buffer


def buy_lotto_automatic(driver, wait, tickets):
    try:
        existing_windows = driver.window_handles  

        # 새 창 열기
        driver.execute_script("window.open('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40');")
        
        # 새 창 포커싱
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        # iframe 진입
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrm_tab")))
        time.sleep(1)

        # 자동번호발급 버튼 클릭
        auto_btn = wait.until(EC.element_to_be_clickable((By.ID, "num2")))
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", auto_btn)

        # 매수 선택 (tickets 변수 사용)
        select_elem = wait.until(EC.presence_of_element_located((By.ID, "amoundApply")))
        select = Select(select_elem)
        select.select_by_value(str(tickets))   # 입력받은 매수 값으로 선택
        
        # 확인 버튼 클릭
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='확인' and not(@id='btnBuy')]")))
            driver.execute_script("arguments[0].click();", confirm_btn)  # JS 클릭 보강
            time.sleep(2)
        except Exception as e:
            print("자동번호구매 확인 버튼 클릭 실패:", e)

        # 구매하기 버튼 클릭
        buy_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnBuy")))
        driver.execute_script("arguments[0].click();", buy_btn)
        time.sleep(2)

        # 결제 확인 레이어 대기 & 확인 클릭
        wait.until(EC.visibility_of_element_located((By.ID, "popupLayerConfirm")))
        popup_ok = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@id='popupLayerConfirm' and not(contains(@style,'display:none'))]""//input[@type='button' and normalize-space(@value)='확인']")))
        driver.execute_script("arguments[0].click();", popup_ok)

        # 레이어 사라질 때까지 대기
        wait.until(EC.invisibility_of_element_located((By.ID, "popupLayerConfirm")))

        # 잔액 부족 / 제한 알림 처리
        try:
            alert_ok = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='popupLayerAlert' and not(contains(@style,'display:none'))]""//input[@value='확인']")))
            driver.execute_script("arguments[0].click();", alert_ok)
            print("잔액이 부족합니다.")
            return "fail"
        except TimeoutException:
            pass

        # 로딩바(#execBuy) 사라질 때까지 대기
        try:
            WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, "execBuy")))
        except TimeoutException:
            pass

        # 구매내역 확인 레이어 닫기
        try:
            receipt_ok = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "closeLayer")))
            driver.execute_script("arguments[0].click();", receipt_ok)
        except TimeoutException:
            pass

        # # 구매창 닫기
        # driver.close()

        # # 메인 홈페이지 창으로 포커스 전환
        # for handle in driver.window_handles:
        #     driver.switch_to.window(handle)
        #     if "method=main" in driver.current_url:
        #         break
        
        # driver.refresh()
        # return "success"

    except TimeoutException as e:
        print("오류 발생! 자동구매 루틴 중 문제:", e)
    
    finally:
        # 성공이든 실패든 구매창 닫기 + 메인 포커싱 시도
        try:
            driver.close()
        except:
            pass
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "method=main" in driver.current_url:
                driver.refresh()
                break
        