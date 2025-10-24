from collections import deque
import copy

def find_start(maze_map: list[list[int]]) -> tuple[int, int] | None:
    for i, row in enumerate(maze_map):
        for j, val in enumerate(row):
            if val == 2:
                return (i, j)
            
    return None

def is_valid(maze_map: list[list[int]], x: int, y: int, visited: list[list[int]]) -> bool:
    return (0 <= x < len(maze_map) and 0 <= y < len(maze_map[0]) and maze_map[x][y] != -1 and not visited[x][y])

def bfs_steps(global_directions: list[tuple[int, int]], maze_map: list[list[int]], goal: list[tuple[int, int]]) -> any:
    start = find_start(maze_map)

    if not start:
        return

    q = deque([(start, [start])])
    visited = [[False for _ in row] for row in maze_map]
    visited[start[0]][start[1]] = True
    directions = global_directions

    while q:
        (x, y), path = q.popleft()

        temp_maze_map = copy.deepcopy(maze_map)

        for i, row in enumerate(temp_maze_map):
            for j, val in enumerate(row):
                if val in (1, 2):
                    temp_maze_map[i][j] = -2

        for px, py in path:
            if temp_maze_map[px][py] in (0, -2):
                temp_maze_map[px][py] = 1

        temp_maze_map[x][y] = 2

        yield temp_maze_map

        if (x, y) in goal:
            return
        else:
            maze_map = copy.deepcopy(temp_maze_map)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if is_valid(maze_map, nx, ny, visited):
                visited[nx][ny] = True
                q.append(((nx, ny), path + [(nx, ny)]))

def dfs_steps(global_directions: list[tuple[int, int]], maze_map: list[list[int]], goal: list[tuple[int, int]]) -> any:
    start = find_start(maze_map)

    if not start:
        return

    stack = [(start, [start])]
    visited = [[False for _ in row] for row in maze_map]
    directions = global_directions

    while stack:
        (x, y), path = stack.pop()

        temp_maze_map = copy.deepcopy(maze_map)

        for i, row in enumerate(temp_maze_map):
            for j, val in enumerate(row):
                if val in (1, 2):
                    temp_maze_map[i][j] = -2

        for px, py in path:
            if temp_maze_map[px][py] in (0, -2):
                temp_maze_map[px][py] = 1

        temp_maze_map[x][y] = 2

        yield temp_maze_map

        if (x, y) in goal:
            return
        else:
            maze_map = copy.deepcopy(temp_maze_map)

        if not visited[x][y]:
            visited[x][y] = True

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if is_valid(maze_map, nx, ny, visited):
                    stack.append(((nx, ny), path + [(nx, ny)]))

def set_start_end(maze_map: list[list[int]], start_pos: tuple[int, int]) -> list[tuple[int, int]]:
    rows = len(maze_map)
    cols = len(maze_map[0]) if rows > 0 else 0
    goal = []

    for i in range(rows):
        for j in range(cols):
            if maze_map[i][j] in (1, 2):
                maze_map[i][j] = 0

            if (i, j) == (start_pos[0] - 1, start_pos[1] - 1):
                maze_map[i][j] = 2

            elif (i == 0 or i == rows - 1 or j == 0 or j == cols - 1) and maze_map[i][j] == 0:
                goal.append((i, j))

    return goal