# 可調整大小的棋盤五子棋遊戲，支援 'larger' 指令，自動外圍擴張與三子連線勝利條件

def get_labels(size):
    row_labels = [chr(i) for i in range(ord('A'), ord('A') + size)]
    col_labels = [str(i + 1) for i in range(size)]
    return row_labels, col_labels

def create_board(size):
    return [['-' for _ in range(size)] for _ in range(size)]

def expand_board_with_border(board, border=1):
    old_size = len(board)
    new_size = old_size + border * 2
    new_board = create_board(new_size)
    for i in range(old_size):
        for j in range(old_size):
            new_board[i + border][j + border] = board[i][j]
    return new_board

def check_needs_expansion(board, margin=2):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if board[row][col] != '-':
                if row < margin or col < margin or row >= size - margin or col >= size - margin:
                    return True
    return False

def print_board(board, row_labels, col_labels):
    col_header = "  | " + ' '.join(f"{col:2}" for col in col_labels)
    print(col_header)
    for i in range(len(board)):
        row_label = f"{row_labels[i]:<2}"
        row_cells = ' '.join(f"{cell:2}" for cell in board[i])
        print(f"{row_label}| {row_cells}")
    print("-" * (4 + 3 * len(board)))

def get_input(player, row_labels, col_labels):
    while True:
        move = input(f"Following is {player}'s: ").strip().upper()
        if move == "LARGER":
            return move, move
        if len(move) >= 2 and move[0] in row_labels and move[1:] in col_labels:
            row = row_labels.index(move[0])
            col = col_labels.index(move[1:])
            return row, col
        else:
            print("Invalid input. Please enter a move like F6, or type 'larger'.")

def check_win(board, row, col, player, win_count=5):
    size = len(board)
    directions = [
        (0, 1),   # →
        (1, 0),   # ↓
        (1, 1),   # ↘
        (1, -1)   # ↙
    ]

    for dr, dc in directions:
        count = 1

        # 往正方向延伸
        for i in range(1, win_count):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < size and 0 <= c < size and board[r][c] == player:
                count += 1
            else:
                break

        # 往反方向延伸
        for i in range(1, win_count):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < size and 0 <= c < size and board[r][c] == player:
                count += 1
            else:
                break

        if count >= win_count:
            return True

    return False

def shift_board(board, row, col, margin=2):
    """
    將 board 整體平移，使 (row,col) 至少距離邊界 margin。
    回傳新的 board，以及更新後的 row, col。
    """
    size = len(board)
    # 計算需要往哪個方向、多少格平移
    shift_r = 0
    shift_c = 0
    if row < margin:
        shift_r = margin - row
    elif row >= size - margin:
        shift_r = (size - margin - 1) - row

    if col < margin:
        shift_c = margin - col
    elif col >= size - margin:
        shift_c = (size - margin - 1) - col

    # 如果不需要平移，直接回傳原值
    if shift_r == 0 and shift_c == 0:
        return board, row, col

    # 建立同尺寸的新棋盤，默認全空
    new_board = create_board(size)
    for i in range(size):
        for j in range(size):
            ni = i + shift_r
            nj = j + shift_c
            if 0 <= ni < size and 0 <= nj < size:
                new_board[ni][nj] = board[i][j]

    # 更新落子座標
    new_row = row + shift_r
    new_col = col + shift_c
    return new_board, new_row, new_col


def play_game():
    board = create_board(7)
    current_player = 'O'

    while True:
        row_labels, col_labels = get_labels(len(board))
        print_board(board, row_labels, col_labels)

        move = get_input(current_player, row_labels, col_labels)
        if move == ("LARGER", "LARGER"):
            board = expand_board_with_border(board, border=1)
            print(f"Board size increased to {len(board)}x{len(board)}.")
            continue

        row, col = move
        if board[row][col] != '-':
            print("Cell already taken. Try again.")
            continue

        board[row][col] = current_player
        temp_board = board

        # 先平移
        if check_needs_expansion(board, margin=2):
            board, row, col = shift_board(board, row, col, margin=2)

        # 平移後若依然碰邊，再真正擴張
        if check_needs_expansion(board, margin=2):
            board = expand_board_with_border(temp_board, border=1)
            # shift_board 之後 board 大小不變，但 expand 後要重新計算 labels
            print(f"Board size increased to {len(board)}x{len(board)}.")

        # 判斷勝利
        if check_win(board, row, col, current_player, win_count=5):
            row_labels, col_labels = get_labels(len(board))
            print_board(board, row_labels, col_labels)
            print(f"Player {current_player} wins!")
            return

        # 換手
        current_player = 'X' if current_player == 'O' else 'O'

# 開始遊戲
play_game()
