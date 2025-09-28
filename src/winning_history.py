import pandas as pd
import keyboard
import time
from utils import clear_input_buffer

# CSV 불러오기
def load_data():
    return pd.read_csv("data/winning_all.csv")

# 회차별 당첨번호 조회
def search_by_round(df, round_no):
    row = df[df["회차"] == round_no]
    if row.empty:
        print(f"{round_no}회차 데이터가 없습니다.")
        return
    draw_date = row.iloc[0]["추첨일"]
    numbers = [row.iloc[0][f"번호{i}"] for i in range(1, 7)]
    bonus = row.iloc[0]["보너스"]

    print(f"\n   ({draw_date})   [{round_no}회차]")
    print(f"당첨번호: {', '.join(map(str, numbers))}")
    print(f"보너스번호: {bonus}")
    print("\nesc를 누르면 메뉴로 돌아갑니다.")
    while True:
        if keyboard.is_pressed("esc"):
            while keyboard.is_pressed("esc"):
                time.sleep(0.1)
            clear_input_buffer()
            return
        time.sleep(0.1)

# 범위내 번호분석
def analyze_range(df, start_round, end_round):
    # 실제 데이터 범위 확인 (추가됨)
    min_round = df["회차"].min()
    max_round = df["회차"].max()

    # 유효 범위 체크 (추가됨)
    if start_round < min_round or end_round > max_round:
        print(f"잘못된 범위입니다. (유효 범위: {min_round} ~ {max_round} 회차)")
        return
    if start_round > end_round:
        print("시작 회차는 끝 회차보다 클 수 없습니다.")
        return

    # 유효 범위일 때만 데이터 추출
    sub_df = df[(df["회차"] >= start_round) & (df["회차"] <= end_round)]
    
    start_date = sub_df.iloc[0]["추첨일"]
    end_date = sub_df.iloc[-1]["추첨일"]

    print(f"\n[{start_round}회차 ~ {end_round}회차] ({start_date} ~ {end_date})")

    # 모든 당첨번호 모으기
    all_numbers = []
    for i in range(1, 7):
        all_numbers.extend(sub_df[f"번호{i}"].tolist())
    all_numbers.extend(sub_df["보너스"].tolist()) 

    # 1~45 전체 번호에 대해 출현 빈도 계산
    freq = pd.Series(all_numbers).value_counts()
    # 1~45 전체 포함 + 내림차순 정렬
    freq = freq.reindex(range(1, 46), fill_value=0)     # 없는 번호는 0으로 채움
    freq = freq.sort_values(ascending=False, kind="mergesort")

    print("\n번호 출현 빈도 (많이 나온 → 적게 나온 순):")
    line = []
    for idx, (num, cnt) in enumerate(freq.items(), start=1):
        line.append(f"[{num} → {cnt}회]")
        if idx % 5 == 0:
            print("  ".join(line))
            line = []
    # 마지막 남은 데이터 출력
    if line:
        print("  ".join(line))
    
    print("\nesc를 누르면 메뉴로 돌아갑니다.")
    while True:
        if keyboard.is_pressed("esc"):
            while keyboard.is_pressed("esc"):
                time.sleep(0.1)
            clear_input_buffer()
            return
        time.sleep(0.1) 

# 메뉴 실행
def winning_history_menu():
    df = load_data()
    while True:
        print("\n===== 당첨내역 상세조회 =====")
        print("1. 회차별 당첨번호 조회")
        print("2. 범위내 번호분석")
        print("ESC. 상위 메뉴로 돌아가기")
        print("\n메뉴 키를 눌러 선택하세요 (예: 1~2, ESC: 상위 메뉴)")
        print(" ")

        key_pressed = False

        while not key_pressed:
            # 회차별 조회
            if keyboard.is_pressed("1"):
                print("회차별 당첨번호 조회 선택")
                while keyboard.is_pressed("1"):
                    time.sleep(0.1)
                    clear_input_buffer()

                # 입력 반복 루프
                while True:
                    min_round = df["회차"].min()
                    max_round = df["회차"].max()
                    try:
                        print(f"조회 가능범위: {min_round} ~ {max_round}")
                        round_no = int(input("조회할 회차 입력: "))
                        print(" ")

                        if round_no < min_round or round_no > max_round:
                            print("조회가능한 범위를 벗어났습니다.")
                            print(" ")
                            continue  # 다시 입력받기

                        # 정상 입력 시 조회 실행
                        search_by_round(df, round_no)
                        break

                    except ValueError:
                        print("숫자를 입력해주세요.")
                        print(" ")
                        continue

                key_pressed = True

            # 범위내 분석
            elif keyboard.is_pressed("2"):
                print("범위내 번호분석 선택")
                while keyboard.is_pressed("2"):
                    time.sleep(0.1)
                    clear_input_buffer()
                while True:  # 올바른 범위가 들어올 때까지 반복
                    try:
                        start = int(input("시작 회차 입력: "))
                        end = int(input("끝 회차 입력: "))

                        # 실제 데이터 범위 확인
                        min_round = df["회차"].min()
                        max_round = df["회차"].max()

                        if start < min_round or end > max_round:
                            print(f"잘못된 범위입니다. (유효 범위: {min_round} ~ {max_round} 회차)")
                            continue
                        if start > end:
                            print("시작 회차는 끝 회차보다 클 수 없습니다.")
                            continue

                        # 통과했으면 분석 실행
                        analyze_range(df, start, end)
                        break

                    except ValueError:
                        print("숫자를 입력하세요.")
                key_pressed = True

            # esc → 상위 메뉴
            elif keyboard.is_pressed("esc"): 
                print("상위 메뉴로 돌아갑니다.")
                while keyboard.is_pressed("esc"):   # 손 뗄 때까지 대기
                    time.sleep(0.1)
                clear_input_buffer()
                return "menu"
                
            time.sleep(0.1)