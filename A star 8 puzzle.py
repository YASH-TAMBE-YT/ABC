import heapq

goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
start = (1, 2, 3, 4, 0, 6, 7, 5, 8)

def heuristic(state):
    distance = 0
    for value in range(1, 9):
        r1, c1 = divmod(state.index(value), 3)
        r2, c2 = divmod(goal.index(value), 3)
        distance += abs(r1 - r2) + abs(c1 - c2)
    return distance

def neighbours(state):
    result = []
    blank = state.index(0)
    row, col = divmod(blank, 3)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_blank = nr * 3 + nc
            new_state = list(state)
            new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]
            result.append(tuple(new_state))
    return result

open_list = []
heapq.heappush(open_list, (heuristic(start), 0, start, [start]))
visited = set()

while open_list:
    f, g, current, path = heapq.heappop(open_list)
    print(f"g = {g}, h = {heuristic(current)}, f = {f}")

    if current == goal:
        print(f"\nGoal Found! Total Moves = {g}")
        for step in path:
            print(step[0:3], "\n", step[3:6], "\n", step[6:9], "\n")
        break

    if current in visited:
        continue
    visited.add(current)

    for nxt in neighbours(current):
        if nxt not in visited:
            new_g = g + 1
            new_f = new_g + heuristic(nxt)
            heapq.heappush(open_list, (new_f, new_g, nxt, path + [nxt]))