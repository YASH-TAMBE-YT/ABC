from collections import deque

grid = [
    ['S', 0, 0, 'X'],
    [0, 'X', 0, 0],
    [0, 0, 0, 'X'],
    ['X', 0, 0, 'G']
]
rows, cols = len(grid), len(grid[0])
start, goal = (0, 0), (3, 3)

queue = deque([(start, [start])])
visited = {start}
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
final_path = None

while queue:
    current, path = queue.popleft()
    print("Current Position:", current, "| Visited:", visited)

    if current == goal:
        final_path = path
        print("\nGoal Reached!")
        break

    for dr, dc in directions:
        nr, nc = current[0] + dr, current[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] != 'X' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

print("Path Found:", final_path if final_path else "No path exists.")