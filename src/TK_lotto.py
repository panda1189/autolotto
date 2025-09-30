import tkinter as tk
import sys, os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# UI 불러오기
from TK_UI import LottoUI, RedirectText

# 기존 기능 모듈
from login import login_function
from balance import check_balance
from passivity import passivity_lotto
from automatic import automatic_lotto
from winning_result import check_winning_result
from winning_history import winning_history_menu


class LottoController:
    def __init__(self, root):
        self.ui = LottoUI(root)
        self.driver = None
        self.wait = None
        self.env_path = ".env"

        # 처음엔 로그인 화면 표시
        self.ui.show_login_screen(self.login)

    # =============================
    # 드라이버 초기화
    # =============================
    def init_driver(self):
        if self.driver is None:
            self.driver = webdriver.Chrome()
            self.wait = WebDriverWait(self.driver, 10)

    # =============================
    # 로그인 처리
    # =============================
    def login(self, user_id, user_pw):
        if not user_id or not user_pw:
            from tkinter import messagebox
            messagebox.showerror("에러", "아이디와 비밀번호를 입력하세요.")
            return

        with open(self.env_path, "w", encoding="utf-8") as f:
            f.write(f"LOTTO_USER={user_id}\n")
            f.write(f"LOTTO_PASS={user_pw}\n")

        self.init_driver()
        if login_function(self.driver, self.wait):
            from tkinter import messagebox
            messagebox.showinfo("성공", "로그인 성공!")

            # 메인 메뉴 표시
            self.ui.show_main_menu(self.run_menu)

            # 출력 리디렉션
            sys.stdout = RedirectText(self.ui.text_area)
        else:
            from tkinter import messagebox
            messagebox.showerror("실패", "로그인 실패. 아이디/비밀번호를 확인하세요.")

    # =============================
    # 메뉴 실행
    # =============================
    def run_menu(self, menu_name):
        if menu_name == "종료":
            if self.driver:
                self.driver.quit()
            self.ui.root.quit()

        elif menu_name == "잔액조회":
            check_balance(self.driver, self.wait)

        elif menu_name == "수동번호구매":
            passivity_lotto(self.driver, self.wait)

        elif menu_name == "자동번호구매":
            automatic_lotto(self.driver, self.wait)

        elif menu_name == "당첨결과조회":
            check_winning_result(self.driver, self.wait, go_to_mypage=True)

        elif menu_name == "당첨내역상세조회":
            winning_history_menu()


if __name__ == "__main__":
    root = tk.Tk()
    app = LottoController(root)
    root.mainloop()