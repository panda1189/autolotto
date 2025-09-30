import tkinter as tk
from tkinter import ttk
import queue

# ✅ 출력 리디렉션 클래스
class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass


class LottoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("로또 자동화 프로그램")
        self.root.geometry("950x700")

        style = ttk.Style()
        style.configure("TLabel", font=("맑은 고딕", 18))
        style.configure("TButton", font=("맑은 고딕", 18))
        style.configure("TEntry", font=("맑은 고딕", 18))

        self.text_area = None

    # =============================
    # 로그인 화면
    # =============================
    def show_login_screen(self, login_callback):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        entry_font = ("맑은 고딕", 18)

        ttk.Label(frame, text="아이디:").grid(row=0, column=0, sticky="w", pady=10, padx=10)
        self.id_entry = tk.Entry(frame, width=35, font=entry_font)
        self.id_entry.grid(row=0, column=1, pady=15, padx=10, ipady=8)

        ttk.Label(frame, text="비밀번호:").grid(row=1, column=0, sticky="w", pady=10, padx=10)
        self.pw_entry = tk.Entry(frame, show="*", width=35, font=entry_font)
        self.pw_entry.grid(row=1, column=1, pady=15, padx=10, ipady=8)

        login_btn = ttk.Button(
            frame,
            text="로그인",
            command=lambda: login_callback(self.id_entry.get().strip(), self.pw_entry.get().strip()),
            width=20
        )
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)

    # =============================
    # 메인 메뉴 화면
    # =============================
    def show_main_menu(self, menu_callback):
        self.clear_window()

        button_frame = ttk.Frame(self.root, padding=20)
        button_frame.pack(anchor="center", pady=20)

        menu_names = [
            "잔액조회", "수동번호구매", "자동번호구매",
            "당첨결과조회", "당첨내역상세조회", "종료"
        ]

        for i, name in enumerate(menu_names):
            btn = ttk.Button(button_frame, text=name, command=lambda n=name: menu_callback(n), width=25)
            btn.grid(row=i//2, column=i%2, padx=20, pady=15, sticky="ew")

        self.text_area = tk.Text(self.root, wrap="word", height=20, font=("Consolas", 14))
        self.text_area.pack(fill="both", expand=True, padx=15, pady=15)

    # =============================
    # 유틸: 화면 초기화
    # =============================
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()