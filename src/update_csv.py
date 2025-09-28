import pandas as pd
from datetime import datetime, timedelta

def update_winning_csv(round_no, win_numbers, bonus_number, csv_path="data/winning_all.csv"):
    # CSV 불러오기
    df = pd.read_csv(csv_path)

    # 마지막 회차, 마지막 추첨일 확인
    last_round = df.iloc[-1]["회차"]
    last_date_str = df.iloc[-1]["추첨일"]     
    last_date = datetime.strptime(last_date_str, "%Y.%m.%d")

    # 새로운 회차 = 마지막 회차 + 1 인 경우만 추가
    if int(round_no) == int(last_round) + 1:
        # 날짜 = 마지막 날짜 + 7일
        new_date = last_date + timedelta(days=7)
        draw_date = new_date.strftime("%Y.%m.%d")

        new_row = {
            "년도": new_date.year,
            "회차": int(round_no),
            "추첨일": draw_date,
            "번호1": win_numbers[0],
            "번호2": win_numbers[1],
            "번호3": win_numbers[2],
            "번호4": win_numbers[3],
            "번호5": win_numbers[4],
            "번호6": win_numbers[5],
            "보너스": bonus_number,
        }

        # 기존 df + 새로운 행을 합치기 ,  concat -> 이어붙힌다는 의미
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # 다시 CSV로 저장 (덮어쓰기)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        print(f"{round_no}회차 당첨결과가 데이터에 추가되었습니다.")
    else:
        print(f"데이터 업데이트 필요 없음 (마지막 회차={last_round}, 조회 회차={round_no})")