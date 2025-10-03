import pandas as pd

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


# 범위내 번호분석
def analyze_range(df, start_round, end_round):
    min_round = df["회차"].min()
    max_round = df["회차"].max()

    if start_round < min_round or end_round > max_round:
        print(f"잘못된 범위입니다. (유효 범위: {min_round} ~ {max_round} 회차)")
        return
    if start_round > end_round:
        print("시작 회차는 끝 회차보다 클 수 없습니다.")
        return

    sub_df = df[(df["회차"] >= start_round) & (df["회차"] <= end_round)]
    
    start_date = sub_df.iloc[0]["추첨일"]
    end_date = sub_df.iloc[-1]["추첨일"]

    print(f"\n[{start_round}회차 ~ {end_round}회차] ({start_date} ~ {end_date})")

    # 출현 빈도 계산
    all_numbers = []
    for i in range(1, 6+1):
        all_numbers.extend(sub_df[f"번호{i}"].tolist())
    all_numbers.extend(sub_df["보너스"].tolist())

    freq = pd.Series(all_numbers).value_counts()
    freq = freq.reindex(range(1, 46), fill_value=0)
    freq = freq.sort_values(ascending=False, kind="mergesort")

    print("\n번호 출현 빈도 (많이 나온 → 적게 나온 순):")
    line = []
    for idx, (num, cnt) in enumerate(freq.items(), start=1):
        line.append(f"[{num} → {cnt}회]")
        if idx % 5 == 0:
            print("  ".join(line))
            line = []
    if line:
        print("  ".join(line))


# 메뉴 실행 (UI 기반)
def winning_history_menu(ui):
    df = load_data()

    print("\n===== 당첨내역 상세조회 =====")
    print("1. 회차별 당첨번호 조회")
    print("2. 범위내 번호분석")

    choice = ui.ui_input("선택하세요 (1/2): ")

    if choice == "1":
        min_round = df["회차"].min()
        max_round = df["회차"].max()
        while True:
            try:
                print(f"조회 가능범위: {min_round} ~ {max_round}")
                round_no = int(ui.ui_input("조회할 회차 입력: "))
                if round_no < min_round or round_no > max_round:
                    print("⚠ 조회가능한 범위를 벗어났습니다.")
                    continue
                search_by_round(df, round_no)
                break
            except ValueError:
                print("⚠ 숫자를 입력해주세요.")

    elif choice == "2":
        min_round = df["회차"].min()
        max_round = df["회차"].max()
        while True:
            try:
                start = int(ui.ui_input("시작 회차 입력: "))
                end = int(ui.ui_input("끝 회차 입력: "))
                if start < min_round or end > max_round:
                    print(f"잘못된 범위입니다. (유효 범위: {min_round} ~ {max_round} 회차)")
                    continue
                if start > end:
                    print("⚠ 시작 회차는 끝 회차보다 클 수 없습니다.")
                    continue
                analyze_range(df, start, end)
                break
            except ValueError:
                print("⚠ 숫자를 입력하세요.")