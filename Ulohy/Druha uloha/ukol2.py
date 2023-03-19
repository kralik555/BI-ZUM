import pygame
import random
import math
import time
# most of the code was taken from https://youtu.be/A80YzvNwqXA
# rewrite this for hill climbing algorithm

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.init()
SCREEN = pygame.display.set_mode((400, 400))
pygame.display.set_caption("N-Queens")
pygame.display.quit()


def pressed_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            exit()


def wait_for_key():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            return False
    return True


def visualize_solution(solution):
    n = len(solution)
    SCREEN.fill(WHITE)
    for row in range(n):
        for col in range(n):
            if (col + row) % 2:
                pygame.draw.rect(SCREEN, GRAY, (row * 50, col * 50, 50, 50))
    for col, row in enumerate(solution):
        pygame.draw.rect(SCREEN, RED, (row * 50, col * 50, 50, 50))
    display = True
    while display:
        pygame.display.update()
        display = wait_for_key()


def visualize_state(state):
    n = len(state)
    SCREEN.fill(WHITE)
    for row in range(n):
        for col in range(n):
            if (col + row) % 2:
                pygame.draw.rect(SCREEN, GRAY, (row * 50, col * 50, 50, 50))
    for col, row in enumerate(state):
        pygame.draw.rect(SCREEN, GREEN, (row * 50, col * 50, 50, 50))
    pressed_quit()
    pygame.display.update()
    if n <= 5:
        time.sleep(0.2)
    elif 5 < n < 11:
        time.sleep(0.1)
    else:
        time.sleep(0.05)


def solve_queens_clibing(n):
    global SCREEN
    SCREEN = pygame.display.set_mode((50 * n, 50 * n))
    evaluation = math.inf
    solution = None
    # restart method - is used when algo reaches local maximum (or minimum in my implementation)
    while evaluation != 0:
        board = [random.randint(0, n-1) for _ in range(n)]
        visualize_state(board)
        solution = hill_climbing(board)
        evaluation = get_eval(solution)
    return solution


def get_eval(state):
    attacks = 0
    for i in range(len(state)):
        for j in range(len(state)):
            if i == j:
                continue
            if state[i] == state[j]:
                attacks += 1
            elif abs(i - j) == abs(state[i] - state[j]):
                attacks += 1
    return attacks


def move_queen(state, row):
    states = []
    for i in range(len(state)):
        new_state = state.copy()
        if i != state[row]:
            new_state[row] = i
            states.append(new_state)
    return states


def get_neighbors(state):
    neighbors = []
    for i in range(len(state)):
        neighbors.extend(move_queen(state, i))
    return neighbors


def hill_climbing(state):
    while True:
        print("Doing something")
        visualize_state(state)
        neighbors = get_neighbors(state)
        next_eval = math.inf
        next_node = state
        for node in neighbors:
            if get_eval(node) < next_eval:
                next_node = node
                next_eval = get_eval(node)
        if next_eval >= get_eval(state):
            return state
        state = next_node


if __name__ == "__main__":
    while True:
        try:
            board_size = int(input("Input board size "))
            solution = solve_queens_clibing(board_size)
            visualize_solution(solution)
            pygame.quit()
        except ValueError:
            break
    pygame.quit()


