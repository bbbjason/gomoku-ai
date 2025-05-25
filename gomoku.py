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
    for i in range(size):
        for j in range(size):
            if board[i][j] != '-':
                if i < margin or j < margin or i >= size - margin or j >= size - margin:
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

def check_win(board, player, win_count=5):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if board[row][col] != player:
                continue
            if col + win_count <= size and all(board[row][col + i] == player for i in range(win_count)):
                return True
            if row + win_count <= size and all(board[row + i][col] == player for i in range(win_count)):
                return True
            if row + win_count <= size and col + win_count <= size and all(board[row + i][col + i] == player for i in range(win_count)):
                return True
            if row + win_count <= size and col - win_count + 1 >= 0 and all(board[row + i][col - i] == player for i in range(win_count)):
                return True
    return False

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
        if board[row][col] == '-':
            board[row][col] = current_player

            # 移動後檢查是否接近邊界，如有則擴張
            if check_needs_expansion(board, margin=2):
                board = expand_board_with_border(board, border=1)

            if check_win(board, current_player):
                row_labels, col_labels = get_labels(len(board))
                print_board(board, row_labels, col_labels)
                print(f"Player {current_player} wins!")
                return

            current_player = 'X' if current_player == 'O' else 'O'
        else:
            print("Cell already taken. Try again.")

# 開始遊戲
play_game()
