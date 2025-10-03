import sys, time, re
import keyboard
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from update_csv import update_winning_csv

BYWIN_URL = "https://dhlottery.co.kr/gameResult.do?method=byWin&wiselog=C_A_1_1"

def check_winning_result(driver, wait, my_tickets=None, go_to_mypage=True):
    """
    4번 메뉴: 새 탭으로 byWin 페이지를 열어 회차/번호만 추출 후 출력.
    go_to_mypage=True 이면 같은 탭에서 우측 상단 '마이페이지'까지 눌러줌.
    """
    orig_window = driver.current_window_handle
    new_window = None

    try:
        # 새탭 열기
        existing = set(driver.window_handles)
        driver.execute_script(f"window.open('{BYWIN_URL}');")
        wait.until(lambda d: len(d.window_handles) > len(existing))
        new_window = (set(driver.window_handles) - existing).pop()
        driver.switch_to.window(new_window)
        time.sleep(0.8)

        # 회차
        round_text = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.win_result h4 strong"))
        ).text.strip()                          # 예: "1190회"
        round_no = re.search(r"\d+", round_text).group()

        # 당첨번호 6개 + 보너스 1개
        win_spans = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.win_result .num.win p span"))
        )
        if len(win_spans) < 6:
            raise TimeoutException(f"당첨번호 span 6개를 찾지 못했습니다. (찾은 개수={len(win_spans)})")

        win_numbers = []
        for s in win_spans[:6]: # win_spans에서 앞의 6개 요소만 반복 (당첨번호 6개)
            txt = s.text.strip() # 각 요소의 텍스트를 가져와 공백 제거
            if not txt.isdigit(): # 만약 숫자가 아니면
                # 숫자가 늦게 채워지는 경우 잠깐 재시도
                for _ in range(15):
                    time.sleep(0.1)
                    txt = s.text.strip()
                    if txt.isdigit(): # 숫자가 채워졌으면 중단
                        break
            win_numbers.append(int(txt)) # 최종적으로 정수로 변환해서 리스트에 추가

        bonus_txt = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.win_result .num.bonus p span"))
        ).text.strip()
        if not bonus_txt.isdigit():
            for _ in range(15):
                time.sleep(0.1)
                bonus_txt = driver.find_element(
                    By.CSS_SELECTOR, "div.win_result .num.bonus p span"
                ).text.strip()
                if bonus_txt.isdigit():
                    break
        bonus_number = int(bonus_txt)

        # 4.출력 (요청 포맷)
        print(f"\n== 제 {round_no}회차 당첨 결과 조회 ==")
        print(f"당첨번호 : {win_numbers}")
        print(f"보너스번호 : [{bonus_number}]")

        # CSV 자동 업데이트
        update_winning_csv(round_no, win_numbers, bonus_number, csv_path="data/winning_all.csv")

        # 마이페이지 이동
        if go_to_mypage:
            driver.get("https://dhlottery.co.kr/userSsl.do?method=myPage")
            wait.until(EC.url_contains("userSsl.do?method=myPage"))
        
        # 당첨결과
        rows = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.tbl_data_col tbody tr"))
            )
        found = False
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) >= 6:
                row_round = tds[1].text.strip()   # 두 번째 열 = 회차
                result_text = tds[5].text.strip() # 여섯 번째 열 = 당첨결과
                if row_round == round_no:
                    print(f"마이페이지 당첨결과: {result_text}")
                    found = True
        if not found:
            print("마이페이지에서 해당 회차의 당첨결과를 찾지 못했습니다.")

        # 현재 탭 닫기
        driver.close()

        # 메인 홈페이지 창으로 포커스 전환
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "method=main" in driver.current_url:
                break

    except Exception as e:
        print("오류 발생:", e)