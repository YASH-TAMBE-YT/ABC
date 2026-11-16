N = 8
board = [-1] * N
nodes_explored = 0
solutions = []

def is_safe(board, row, col):
    for prev_col in range(col):
        prev_row = board[prev_col]
        if prev_row == row or abs(prev_row - row) == abs(prev_col - col):
            return False
    return True

def backtracking_search(col=0):
    global nodes_explored
    nodes_explored += 1
    if col == N:
        solutions.append(board.copy())
        return
    for row in range(N):
        if is_safe(board, row, col):
            board[col] = row
            backtracking_search(col + 1)
            board[col] = -1

backtracking_search(0)
print("Number of solutions found:", len(solutions))
print("Search nodes explored:", nodes_explored)

for row in range(N):
    print(" ".join(" Q " if solutions[0][col] == row else " . " for col in range(N)))