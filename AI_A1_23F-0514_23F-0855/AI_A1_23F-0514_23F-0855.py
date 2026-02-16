import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque
import heapq

GRID_SIZE = 20

START = (1, 1)
TARGET = (11, 12)

DELAY = 0.05

EMPTY = 0
WALL = 1
START_NODE = 2
TARGET_NODE = 3
FRONTIER = 4
EXPLORED = 5
PATH = 6

MOVES = [
    (-1, 0), (0, 1), (1, 0),
    (1, 1), (1, -1),
    (0, -1),
    (-1, -1), (-1, 1)
]

# STRUCTURED GRID

def create_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE))

    # Border wall
    grid[0, :] = WALL
    grid[:, 0] = WALL
    grid[GRID_SIZE-1, :] = WALL
    grid[:, GRID_SIZE-1] = WALL

    # Horizontal segments
    for col in range(3, 8):
        grid[5, col] = WALL
    for col in range(10, 15):
        grid[10, col] = WALL
    for col in range(4, 9):
        grid[14, col] = WALL

    # Vertical segments
    for row in range(6, 11):
        grid[row, 7] = WALL
    for row in range(3, 8):
        grid[row, 13] = WALL
    for row in range(11, 16):
        grid[row, 4] = WALL

    grid[START] = START_NODE
    grid[TARGET] = TARGET_NODE

    return grid

# VISUALIZATION

def setup_visual(grid, algo_name):
    plt.ion()
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_title(f"Algorithm Name — {algo_name}")
    ax.set_xticks([])
    ax.set_yticks([])

    cmap = plt.cm.colors.ListedColormap([
        "white",   # empty
        "black",   # wall
        "lime",    # start
        "red",     # goal
        "cyan",    # frontier
        "blue",    # explored
        "yellow"   # path
    ])

    img = ax.imshow(grid, cmap=cmap, vmin=0, vmax=6)
    plt.show()
    return fig, img

def draw(fig, img, grid):
    grid[START] = START_NODE
    grid[TARGET] = TARGET_NODE

    img.set_data(grid)
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(DELAY)

# UTILITIES

def in_bounds(node):
    x, y = node
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE

def neighbors(node):
    result = []
    for dx, dy in MOVES:
        nxt = (node[0] + dx, node[1] + dy)
        if in_bounds(nxt):
            result.append(nxt)
    return result

def reconstruct(parent, end):
    path = []
    while end in parent:
        path.append(end)
        end = parent[end]
    return path[::-1]

# ALGORITHMS

def bfs(grid, fig, img):
    queue = deque([START])
    parent = {}
    visited = {START}

    while queue:
        current = queue.popleft()
        if current == TARGET:
            return reconstruct(parent, current)

        for n in neighbors(current):
            if grid[n] != WALL and n not in visited:
                visited.add(n)
                parent[n] = current
                queue.append(n)
                if grid[n] == EMPTY:
                    grid[n] = FRONTIER

        if grid[current] not in [START_NODE, TARGET_NODE]:
            grid[current] = EXPLORED

        draw(fig, img, grid)

    return None

def dfs(grid, fig, img):
    stack = [START]
    parent = {}
    visited = set()

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == TARGET:
            return reconstruct(parent, current)

        for n in reversed(neighbors(current)):
            if grid[n] != WALL and n not in visited:
                parent[n] = current
                stack.append(n)
                if grid[n] == EMPTY:
                    grid[n] = FRONTIER

        if grid[current] not in [START_NODE, TARGET_NODE]:
            grid[current] = EXPLORED

        draw(fig, img, grid)

    return None

def ucs(grid, fig, img):
    pq = []
    heapq.heappush(pq, (0, START))
    parent = {}
    cost = {START: 0}

    while pq:
        c, current = heapq.heappop(pq)
        if current == TARGET:
            return reconstruct(parent, current)

        for n in neighbors(current):
            if grid[n] != WALL:
                new_cost = c + 1
                if n not in cost or new_cost < cost[n]:
                    cost[n] = new_cost
                    parent[n] = current
                    heapq.heappush(pq, (new_cost, n))
                    if grid[n] == EMPTY:
                        grid[n] = FRONTIER

        if grid[current] not in [START_NODE, TARGET_NODE]:
            grid[current] = EXPLORED

        draw(fig, img, grid)

    return None

def dls(grid, fig, img, limit):
    stack = [(START, 0)]
    parent = {}
    visited = set()

    while stack:
        current, depth = stack.pop()
        if current == TARGET:
            return reconstruct(parent, current)
        if depth > limit:
            continue

        visited.add(current)

        for n in reversed(neighbors(current)):
            if grid[n] != WALL and n not in visited:
                parent[n] = current
                stack.append((n, depth+1))
                if grid[n] == EMPTY:
                    grid[n] = FRONTIER

        if grid[current] not in [START_NODE, TARGET_NODE]:
            grid[current] = EXPLORED

        draw(fig, img, grid)

    return None

def iddfs(grid, fig, img):
    for depth in range(1, GRID_SIZE * 2):
        temp = grid.copy()
        result = dls(temp, fig, img, depth)
        if result:
            return result
    return None

def bidirectional(grid, fig, img):
    q_start = deque([START])
    q_goal = deque([TARGET])

    parent_start = {}
    parent_goal = {}
    visited_start = {START}
    visited_goal = {TARGET}

    while q_start and q_goal:

        current = q_start.popleft()
        for n in neighbors(current):
            if grid[n] != WALL and n not in visited_start:
                parent_start[n] = current
                visited_start.add(n)
                q_start.append(n)

                if n in visited_goal:
                    path1 = reconstruct(parent_start, n)
                    path2 = reconstruct(parent_goal, n)
                    return path1 + path2[::-1]

        current = q_goal.popleft()
        for n in neighbors(current):
            if grid[n] != WALL and n not in visited_goal:
                parent_goal[n] = current
                visited_goal.add(n)
                q_goal.append(n)

                if n in visited_start:
                    path1 = reconstruct(parent_start, n)
                    path2 = reconstruct(parent_goal, n)
                    return path1 + path2[::-1]

        draw(fig, img, grid)

    return None

# MAIN LOOP

def main_loop():
    algo_dict = {
        "1": "BFS",
        "2": "DFS",
        "3": "UCS",
        "4": "DLS",
        "5": "IDDFS",
        "6": "Bidirectional"
    }

    while True:
        print("\nSelect Algorithm:")
        print("1 - BFS")
        print("2 - DFS")
        print("3 - UCS")
        print("4 - DLS")
        print("5 - IDDFS")
        print("6 - Bidirectional")
        print("0 - Exit")

        choice = input("Enter choice: ")

        if choice == "0":
            print("Program Ended.")
            break

        if choice not in algo_dict:
            print("Invalid choice")
            continue

        grid = create_grid()
        algo_name = algo_dict[choice]
        fig, img = setup_visual(grid, algo_name)

        start_time = time.time()

        if choice == "1":
            path = bfs(grid, fig, img)
        elif choice == "2":
            path = dfs(grid, fig, img)
        elif choice == "3":
            path = ucs(grid, fig, img)
        elif choice == "4":
            path = dls(grid, fig, img, 25)
        elif choice == "5":
            path = iddfs(grid, fig, img)
        elif choice == "6":
            path = bidirectional(grid, fig, img)

        end_time = time.time()

        if path:
            for node in path:
                if grid[node] not in [START_NODE, TARGET_NODE]:
                    grid[node] = PATH
                draw(fig, img, grid)

        print("Execution Time:", round(end_time - start_time, 4), "seconds")

        input("Press ENTER to continue...")
        plt.close(fig)

if __name__ == "__main__":
    main_loop()