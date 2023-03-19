import random
import sys
import math
import pygame
import time

pygame.init()

FOUND = False
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SCREEN = pygame.display.set_mode((400, 400))
pygame.quit()
sys.setrecursionlimit(100_000)


def load_map(name):
    with open(f"{name}") as f:
        y = 0
        lines = f.readlines()
        width = len(lines[0]) - 1
        height = len(lines) - 2
        nodes = [[0 for j in range(width)] for i in range(height)]
        for line in lines:
            for x, val in enumerate(line):
                if val == "X":
                    nodes[y][x] = 1
            y += 1
        return nodes


def load_positions(name):
    s, e = None, None
    with open(f"{name}") as f:
        lines = f.readlines()
        s = lines[-2]
        e = lines[-1]
        s = s.replace(",", "")
        e = e.replace(",", "")
    s = s.split()[1:]
    e = e.split()[1:]
    s = [int(s[1]), int(s[0])]
    e = [int(e[1]), int(e[0])]
    return s, e


def wanna_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            exit()


def draw_start_graph(start, end, graph):
    global SCREEN
    width = len(graph[0])
    height = len(graph)
    SCREEN = pygame.display.set_mode((width * 10, height * 10))
    pygame.display.set_caption("Search algorithms")
    SCREEN.fill(WHITE)
    pygame.display.update()
    for y in range(height):
        for x in range(width):
            if graph[y][x] == 1:
                display_rect([y, x], BLACK)
    display_rect(start, BLUE)
    display_rect(end, RED)
    pygame.display.update()
    time.sleep(0.5)


def display_rect(pos, color):
    rect = pygame.Rect(pos[1] * 10, pos[0] * 10, 10, 10)
    pygame.draw.rect(SCREEN, color, rect)


def draw_path(path):
    for node in path:
        display_rect(node, GREEN)
    pygame.display.update()


def backtracking(predecessors, end):
    p = []
    keys = predecessors.keys()
    pos = f"{end[0]} {end[1]}"
    while pos in keys:
        p.append(predecessors[pos])
        a = predecessors[pos]
        pos = f"{a[0]} {a[1]}"
    p.reverse()
    return p


def random_search(position, end, graph):
    print("Running random search")
    open = [position]
    preds = {}
    draw_start_graph(position, end, graph)
    while open:
        position = random.choice(open)
        display_rect(position, BLUE)
        pygame.display.update()
        wanna_quit()
        time.sleep(0.01)
        if position == end:
            break
        adjacent_nodes = []
        for i in ([-1, 0], [0, -1], [1, 0], [0, 1]):
            adjacent_nodes.append([position[0] + i[0], position[1] + i[1]])
        for node in adjacent_nodes:
            if graph[node[0]][node[1]] == 0 and node not in open:
                open.append(node)
                preds[f"{node[0]} {node[1]}"] = position

        open.remove(position)
        graph[position[0]][position[1]] = 1
    path = backtracking(preds, end)
    path.append(end)
    draw_path(path)
    print("Expanded nodes:", len(preds))
    print("Path length:", len(path) - 1)
    return path


def bfs(position, end, graph):
    print("Running BFS")
    draw_start_graph(position, end, graph)
    open = []
    preds = {}
    open.append(position)
    while open:
        position = open.pop(0)
        display_rect(position, BLUE)
        pygame.display.update()
        time.sleep(0.01)
        wanna_quit()
        if position == end:
            break
        adjacent_nodes = []
        for i in ([-1, 0], [0, -1], [1, 0], [0, 1]):
            adjacent_nodes.append([position[0] + i[0], position[1] + i[1]])
        for node in adjacent_nodes:
            if graph[node[0]][node[1]] == 0 and node not in open:
                open.append(node)
                preds[f"{node[0]} {node[1]}"] = position
        graph[position[0]][position[1]] = 1
    path = backtracking(preds, end)
    path.append(end)
    draw_path(path)
    print("Expanded nodes:", len(preds))
    print("Path length:", len(path) - 1)
    return path


def dfs(position, end, graph, preds):
    display_rect(position, BLUE)
    pygame.display.update()
    wanna_quit()
    time.sleep(0.01)
    global FOUND
    p = []
    graph[position[0]][position[1]] = 1
    if position == end:
        FOUND = True
        p = backtracking(preds, end)
        p.append(end)
        draw_path(p)
        print("Expanded nodes:", len(preds))
        print("Path length:", len(p) - 1)
        return p
    adjacent_nodes = []
    for i in ([-1, 0], [0, 1], [1, 0], [0, -1]):
        adjacent_nodes.append([position[0] + i[0], position[1] + i[1]])
    graph[position[0]][position[1]] = 1
    for new_pos in adjacent_nodes:
        if graph[new_pos[0]][new_pos[1]] == 0 and not FOUND:  # or smaller number of steps
            preds[f"{new_pos[0]} {new_pos[1]}"] = position
            p = dfs(new_pos, end, graph, preds)
    return p


def dfs_iterative(position, end, graph):
    open = [position]
    preds = {}
    print("Running DFS iterative")
    draw_start_graph(position, end, graph)
    while open:
        position = open.pop()
        display_rect(position, BLUE)
        pygame.display.update()
        wanna_quit()
        time.sleep(0.01)
        if position == end:
            break
        if graph[position[0]][position[1]] == 0:
            graph[position[0]][position[1]] = 1
            adjacent_nodes = []
            for i in ([-1, 0], [0, 1], [1, 0], [0, -1]):
                adjacent_nodes.append([position[0] + i[0], position[1] + i[1]])
            for new_pos in adjacent_nodes:
                if graph[new_pos[0]][new_pos[1]] == 0:  # or smaller number of steps
                    preds[f"{new_pos[0]} {new_pos[1]}"] = position
                    open.append(new_pos)
    path = backtracking(preds, end)
    path.append(end)
    draw_path(path)
    print("Expanded nodes:", len(preds))
    print("Path length:", len(path) - 1)
    return path


def greedy_algorithm(position, end, graph):
    print("Running greedy")
    draw_start_graph(position, end, graph)
    open = [position]
    preds = {}
    while open:
        if position == end:
            break
        adjacent_nodes = []
        for i in ([-1, 0], [0, -1], [1, 0], [0, 1]):
            adjacent_nodes.append([position[0] + i[0], position[1] + i[1]])
        for node in adjacent_nodes:
            if graph[node[0]][node[1]] == 0 and node not in open:
                open.append(node)
                preds[f"{node[0]} {node[1]}"] = position
        open.remove(position)
        graph[position[0]][position[1]] = 1
        min_dist = math.inf
        best_node = open[0]
        for node in open:
            # manhattan distance
            dist = abs(node[0] - end[0]) + abs(node[1] - end[1])
            if dist < min_dist:
                min_dist = dist
                best_node = node
        position = best_node
        display_rect(position, BLUE)
        pygame.display.update()
        time.sleep(0.01)
    path = backtracking(preds, end)
    path.append(end)
    draw_path(path)
    print("Expanded nodes:", len(preds))
    print("Path length:", len(path) - 1)
    return path


def a_star(position, end, graph):
    print("Running A*")
    draw_start_graph(position, end, graph)
    open = [position]
    preds = {}
    nodes_dist = {}
    nodes_possible_dist = {}
    for row in range(len(graph)):
        for col in range(len(graph[0])):
            nodes_possible_dist[f"{row} {col}"] = math.inf
            nodes_dist[f"{row} {col}"] = math.inf
    nodes_dist[f"{position[0]} {position[1]}"] = 0
    nodes_possible_dist[f"{position[0]} {position[1]}"] = abs(position[0] - end[0]) + abs(position[1] - end[1])

    while open:
        position = open[0]
        min_dist = nodes_possible_dist[f"{position[0]} {position[1]}"]
        wanna_quit()
        for node in open:
            if nodes_possible_dist[f"{node[0]} {node[1]}"] < min_dist:
                min_dist = nodes_possible_dist[f"{node[0]} {node[1]}"]
                position = node
        if position == end:
            break
        display_rect(position, BLUE)
        pygame.display.update()
        time.sleep(0.01)
        open.remove(position)
        adjacent_nodes = []
        for i in ([-1, 0], [0, -1], [1, 0], [0, 1]):
            adjacent_nodes.append([position[0] + i[0], position[1] + i[1]])
        for node in adjacent_nodes:
            if graph[node[0]][node[1]] == 0:
                dist = nodes_dist[f"{position[0]} {position[1]}"] + 1
                if dist < nodes_dist[f"{node[0]} {node[1]}"]:
                    preds[f"{node[0]} {node[1]}"] = position
                    nodes_dist[f"{node[0]} {node[1]}"] = dist
                    nodes_possible_dist[f"{node[0]} {node[1]}"] = dist + abs(node[0] - end[0]) + abs(node[1] - end[1])
                    if node not in open:
                        open.append(node)

    path = backtracking(preds, end)
    path.append(end)
    draw_path(path)
    print("Expanded nodes:", len(preds))
    print("Path length:", len(path) - 1)
    return path


def wait_for_enter():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return


def test():
    global SCREEN
    global FOUND
    names = ["00_11_11_1550177690.txt", "01_71_51_156.txt", "02_71_51_1552235384.txt"]
    for name in names:
        FOUND = False
        file = f"testy/{name}"
        width = len(load_map(file)[0])
        height = len(load_map(file))
        SCREEN = pygame.display.set_mode((width * 10, height * 10))
        pygame.display.set_caption("Search algorithms")
        pygame.display.update()

        start, end = load_positions(file)
        print(len(dfs_iterative(start, end, load_map(file))) - 1)
        wait_for_enter()
        print(len(random_search(start, end, load_map(file))) - 1)
        wait_for_enter()
        print(len(bfs(start, end, load_map(file))) - 1)
        wait_for_enter()
        print(len(greedy_algorithm(start, end, load_map(file))) - 1)
        wait_for_enter()
        print(len(a_star(start, end, load_map(file))) - 1)
        wait_for_enter()


def get_graph():
    global SCREEN
    name = input("Name of the file: ")
    try:
        load_map(name)
    except FileNotFoundError:
        print("Invalid file path")
        return None, -1, -1

    start, end = load_positions(name)
    return load_map(name), start, end


if __name__ == "__main__":
    while True:
        graph, start, end = get_graph()
        if not graph:
            continue
        algo = input("Give algorithm to use (possible are BFS, DFS, Random, Greedy, A*): ")
        if algo not in ["DFS", "BFS", "Greedy", "A*", "Random"]:
            print("Incorrect algorithm")
            continue
        if algo == "DFS":
            dfs_iterative(start, end, graph)
        elif algo == "BFS":
            bfs(start, end, graph)
        elif algo == "Greedy":
            greedy_algorithm(start, end, graph)
        elif algo == "Random":
            random_search(start, end, graph)
        else:
            a_star(start, end, graph)
        wait_for_enter()
        pygame.quit()
        if start == -1:
            break

    # test()
    pygame.quit()



