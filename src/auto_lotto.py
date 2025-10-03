import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select


def buy_lotto_automatic(driver, wait, tickets):
    """
    자동번호 구매 실행 함수
    -> 각 티켓별 번호를 2차원 배열로 반환
       예: [[1,2,3,4,5,6], [7,8,9,10,11,12], ...]
    """
    try:
        # 새 창 열기
        driver.execute_script("window.open('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        # iframe 진입
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrm_tab")))
        time.sleep(1)

        # 자동번호발급 버튼 클릭
        auto_btn = wait.until(EC.element_to_be_clickable((By.ID, "num2")))
        driver.execute_script("arguments[0].click();", auto_btn)
        time.sleep(0.5)

        # 매수 선택
        select_elem = wait.until(EC.presence_of_element_located((By.ID, "amoundApply")))
        select = Select(select_elem)
        select.select_by_value(str(tickets))

        # 확인 버튼 클릭
        confirm_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='button' and @value='확인' and not(@id='btnBuy')]")
            )
        )
        driver.execute_script("arguments[0].click();", confirm_btn)
        time.sleep(2)

        # 구매하기 버튼
        buy_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnBuy")))
        driver.execute_script("arguments[0].click();", buy_btn)
        time.sleep(2)

        # 결제 확인 레이어 확인 클릭
        wait.until(EC.visibility_of_element_located((By.ID, "popupLayerConfirm")))
        popup_ok = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[@id='popupLayerConfirm' and not(contains(@style,'display:none'))]"
            "//input[@type='button' and normalize-space(@value)='확인']"
        )))
        driver.execute_script("arguments[0].click();", popup_ok)
        wait.until(EC.invisibility_of_element_located((By.ID, "popupLayerConfirm")))

        # ❌ 예치금 부족 팝업 확인
        try:
            alert_ok = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//div[@id='popupLayerAlert' and not(contains(@style,'display:none'))]//input[@value='확인']"
                ))
            )
            driver.execute_script("arguments[0].click();", alert_ok)
            print("❌ 예치금이 부족합니다.")
            return "fail", []
        except TimeoutException:
            pass

        # ✅ 구매번호 추출 (티켓 단위)
        purchased_tickets = []
        try:
            ticket_divs = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#reportRow"))
            )
            for div in ticket_divs:
                spans = div.find_elements(By.CSS_SELECTOR, "div.nums span")
                nums = [int(el.text) for el in spans if el.text.strip().isdigit()]
                if nums:
                    purchased_tickets.append(nums)
        except Exception:
            purchased_tickets = []

        # 구매내역 확인 레이어 닫기
        try:
            receipt_ok = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "closeLayer"))
            )
            driver.execute_script("arguments[0].click();", receipt_ok)
        except TimeoutException:
            pass

        return "success", purchased_tickets

    except TimeoutException as e:
        print("오류 발생! 자동구매 루틴 중 문제:", e)
        return "fail", []

    finally:
        try:
            driver.close()
        except:
            pass
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "method=main" in driver.current_url:
                driver.refresh()
                break