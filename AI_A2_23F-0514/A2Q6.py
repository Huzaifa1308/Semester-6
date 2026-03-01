import pygame
import random
import math
import heapq
import time

ROWS = 20
COLS = 20
CELL = 30
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

def heuristic(a, b, heuristic_type):
    if heuristic_type == "manhattan":
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    else:
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def neighbors(node, grid):
    r, c = node
    result = []
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if grid[nr][nc] != 1:
                result.append((nr,nc))
    return result

def search(grid, start, goal, algorithm, heuristic_type):
    visited_nodes = 0
    open_list = []
    count = 0
    g = {start: 0}
    parent = {}
    visited_set = set()
    frontier_set = set()

    start_time = time.time()

    heapq.heappush(open_list, (heuristic(start, goal, heuristic_type), count, start))
    count += 1

    while open_list:
        _, _, current = heapq.heappop(open_list)
        visited_nodes += 1
        visited_set.add(current)

        if current == goal:
            exec_time = (time.time()-start_time)*1000
            path = build_path(parent, goal)
            return path, visited_nodes, exec_time, visited_set, frontier_set

        for nb in neighbors(current, grid):
            new_g = g[current] + 1

            if nb not in g or new_g < g[nb]:
                g[nb] = new_g
                parent[nb] = current

                if algorithm == "astar":
                    f = new_g + heuristic(nb, goal, heuristic_type)
                else:
                    f = heuristic(nb, goal, heuristic_type)

                heapq.heappush(open_list, (f, count, nb))
                count += 1
                frontier_set.add(nb)

    exec_time = (time.time()-start_time)*1000
    return [], visited_nodes, exec_time, visited_set, frontier_set

def build_path(parent, goal):
    path = []
    node = goal
    while node in parent:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path

def run_visualization(algorithm, heuristic_type, dynamic_mode, density):

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pathfinding Visualization")

    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    start = (0,0)
    goal = (ROWS-1, COLS-1)

    for r in range(ROWS):
        for c in range(COLS):
            if (r,c) not in [start, goal]:
                if random.random() < density:
                    grid[r][c] = 1

    path = []
    visited_set = set()
    frontier_set = set()
    visited_nodes = 0
    exec_time = 0

    search_started = False

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)
        screen.fill((255,255,255))

        if dynamic_mode and search_started and path:
            if random.random() < 0.02:
                r = random.randint(0, ROWS-1)
                c = random.randint(0, COLS-1)
                if (r,c) not in [start, goal]:
                    grid[r][c] = 1
                    if (r,c) in path:
                        path, visited_nodes, exec_time, visited_set, frontier_set = search(
                            grid, start, goal, algorithm, heuristic_type)

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            r = y // CELL
            c = x // CELL
            if 0 <= r < ROWS and 0 <= c < COLS:
                if (r,c) not in [start, goal]:
                    grid[r][c] = 0 if grid[r][c] == 1 else 1

        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c*CELL, r*CELL, CELL, CELL)

                if grid[r][c] == 1:
                    pygame.draw.rect(screen, (0,0,0), rect)
                elif (r,c) in path:
                    pygame.draw.rect(screen, (0,255,0), rect)
                elif (r,c) in visited_set:
                    pygame.draw.rect(screen, (255,0,0), rect)
                elif (r,c) in frontier_set:
                    pygame.draw.rect(screen, (255,255,0), rect)
                else:
                    pygame.draw.rect(screen, (255,255,255), rect)

                pygame.draw.rect(screen, (200,200,200), rect, 1)

        pygame.draw.rect(screen, (0,0,255), (start[1]*CELL, start[0]*CELL, CELL, CELL))
        pygame.draw.rect(screen, (128,0,128), (goal[1]*CELL, goal[0]*CELL, CELL, CELL))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    path, visited_nodes, exec_time, visited_set, frontier_set = search(
                        grid, start, goal, algorithm, heuristic_type)
                    search_started = True

    pygame.quit()

    print("\n--- METRICS ---")
    print("Algorithm:", algorithm)
    print("Heuristic:", heuristic_type)
    print("Visited Nodes:", visited_nodes)
    print("Path Cost:", len(path))
    print("Execution Time (ms):", round(exec_time,2))
    print("----------------\n")

while True:
    print("==== PATHFINDING MENU ====")
    print("1. A*")
    print("2. Greedy Best First")
    alg_choice = input("Select Algorithm: ")
    algorithm = "astar" if alg_choice == "1" else "gbfs"

    print("\n1. Manhattan")
    print("2. Euclidean")
    heu_choice = input("Select Heuristic: ")
    heuristic_type = "manhattan" if heu_choice == "1" else "euclidean"

    dyn = input("\nEnable Dynamic Mode? (y/n): ")
    dynamic_mode = True if dyn.lower() == "y" else False

    density = float(input("\nObstacle Density (0.0 - 0.5 recommended): "))

    print("\nInstructions:")
    print("- Left Click to add/remove obstacles")
    print("- Press ENTER to start search")
    print("- Close window to return to menu\n")

    run_visualization(algorithm, heuristic_type, dynamic_mode, density)

    again = input("Run again? (y/n): ")
    if again.lower() != "y":
        break