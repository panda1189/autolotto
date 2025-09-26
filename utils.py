import msvcrt

# 입력 버퍼 비우기
def clear_input_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()