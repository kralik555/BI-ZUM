import gui
import pygame
from itertools import product
import random
import time

pygame.init()


class Piece:

    def __init__(self, color, col, row):
        self.color = color
        self.col = col
        self.row = row


class Board:
    def __init__(self):
        self.board = [[0 for i in range(5)] for _ in range(5)]

        self.sprites = ["white_pawn", "white_knight", "white_bishop", "white_rook", "white_queen", "white_king",
                        "black_pawn", "black_knight", "black_bishop", "black_rook", "black_queen", "black_king"]

        self.board[0] = [4, 2, 3, 5, 6]
        self.board[1] = [1 for _ in range(5)]
        self.board[3] = [7 for _ in range(6)]
        self.board[4] = [10, 8, 9, 11, 12]
        self.to_move = "white"
        self.player_color = "white"
        self.ai_color = "black"
        self.values = [1, 3, 3, 5, 9, 100_000]
        self.over = False
        self.num_of_pieces = 20
        self.past_moves = []
        self.tried_moves = 0
        self.undo_time = 0
        self.find_move_time = 0
        self.move_time = 0
        self.eval_time = 0
        self.evaluations = {}
        self.minmax_evals = {}

    def display_pieces(self):
        """
        Calls display function for each piece on the board
        """
        for i in range(5):
            for j in range(5):
                if self.board[i][j] != 0:
                    sprite = pygame.image.load(f"Sprites/{self.sprites[self.board[i][j] - 1]}.png")
                    gui.display_piece(self.player_color, sprite, j, i)

    def moves(self, col, row):
        """
        Returns moves that can be done from a tile
        based on what piece type there is on the tile
        """
        if self.board[row][col] == 0:
            return []
        elif self.board[row][col] in [3, 4, 5, 9, 10, 11]:
            return self.sliding_moves(col, row)
        elif self.board[row][col] in [6, 12]:
            return self.simple_king_moves(col, row)
        elif self.board[row][col] in [2, 8]:
            return self.knight_moves(col, row)
        elif self.board[row][col] in [1, 7]:
            return self.pawn_moves(col, row)

    def pawn_moves(self, col, row):
        possible_moves = []
        if self.board[row][col] == 1:  # white
            if self.board[row + 1][col] == 0:
                possible_moves.append([col, row + 1])
            if col < 4:
                if self.board[row + 1][col + 1] > 6:
                    possible_moves.append([col + 1, row + 1])
            if col > 0:
                if self.board[row + 1][col - 1] > 6:
                    possible_moves.append([col - 1, row + 1])
        else:
            if self.board[row][col] == 7:  # black
                if self.board[row - 1][col] == 0:
                    possible_moves.append([col, row - 1])
                if col < 4:
                    if 0 < self.board[row - 1][col + 1] <= 6:
                        possible_moves.append([col + 1, row - 1])
                if col > 0:
                    if 0 < self.board[row - 1][col - 1] <= 6:
                        possible_moves.append([col - 1, row - 1])
        return possible_moves

    def sliding_moves(self, col, row):
        moves = []
        b_d = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        r_d = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        if self.board[row][col] in [3, 9, 5, 11]:
            for d in b_d:
                dist = 1
                while 0 <= row + dist * d[0] < 5 and 0 <= col + dist * d[1] < 5:
                    tile = self.board[row + dist * d[0]][col + dist * d[1]]
                    if tile == 0 or ((tile - 1) // 6) != ((self.board[row][col] - 1) // 6):
                        moves.append([col + dist * d[1], row + dist * d[0]])
                        dist += 1
                        if tile != 0:
                            break
                    else:
                        break
        if self.board[row][col] in [4, 10, 5, 11]:
            for d in r_d:
                dist = 1
                while 0 <= row + dist * d[0] < 5 and 0 <= col + dist * d[1] < 5:
                    tile = self.board[row + dist * d[0]][col + dist * d[1]]
                    if tile == 0 or ((tile - 1) // 6) != ((self.board[row][col] - 1) // 6):
                        moves.append([col + dist * d[1], row + dist * d[0]])
                        dist += 1
                        if tile != 0:
                            break
                    else:
                        break
        return moves

    def simple_king_moves(self, col, row):
        moves = []
        tiles = list(product((0, 1, -1), repeat=2))
        tiles.remove((0, 0))
        for tile in tiles:
            if 0 <= col + tile[0] < 5 and 0 <= row + tile[1] < 5:
                if self.board[row + tile[1]][col + tile[0]] == 0:
                    moves.append([col + tile[0], row + tile[1]])
                if self.board[row][col] == 6:
                    if self.board[row + tile[1]][col + tile[0]] > 6:
                        moves.append([col + tile[0], row + tile[1]])
                else:
                    if 0 < self.board[row + tile[1]][col + tile[0]] <= 6:
                        moves.append([col + tile[0], row + tile[1]])
        return moves

    def knight_moves(self, col, row):
        moves = []
        tiles = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
        for tile in tiles:
            if 0 <= col + tile[0] < 5 and 0 <= row + tile[1] < 5:
                if self.board[row + tile[1]][col + tile[0]] == 0:
                    moves.append([col + tile[0], row + tile[1]])
                if self.board[row][col] == 2:
                    if self.board[row + tile[1]][col + tile[0]] > 6:
                        moves.append([col + tile[0], row + tile[1]])
                else:
                    if 0 < self.board[row + tile[1]][col + tile[0]] < 7:
                        moves.append([col + tile[0], row + tile[1]])
        return moves

    def all_moves(self):
        moves = {}
        possible_moves = []
        for row in range(5):
            for col in range(5):
                if self.to_move == "white" and 0 < self.board[row][col] <= 6:
                    mvs = self.moves(col, row)
                    moves[(col, row)] = mvs
                elif self.to_move == "black" and 6 < self.board[row][col] < 13:
                    mvs = self.moves(col, row)
                    moves[(col, row)] = mvs
        for key, value in moves.items():
            for i in value:
                possible_moves.append([list(key), i])
        return possible_moves

    def evaluate(self):
        b = tuple(tuple(sub) for sub in self.board)
        if b in self.evaluations.keys():
            return self.evaluations[b]
        white_val = 0
        black_val = 0
        for row in range(5):
            for col in range(5):
                if self.board[row][col] != 0:
                    if self.board[row][col] > 6:
                        black_val += self.values[(self.board[row][col] - 1) % 6]
                    else:
                        white_val += self.values[(self.board[row][col] - 1) % 6]
        if self.to_move == "white":
            self.evaluations[b] = white_val - black_val
            return white_val - black_val
        else:
            self.evaluations[b] = black_val - white_val
            return black_val - white_val

    def make_random_move(self):
        move = random.choice(self.all_moves())
        start = move[0]
        end = move[1]
        self.move(start, end)

    def move(self, start, end):
        self.past_moves.append([start, end, self.board[start[1]][start[0]], self.board[end[1]][end[0]]])
        if self.board[end[1]][end[0]] != 0:
            self.num_of_pieces -= 1
            if self.board[end[1]][end[0]] in [6, 12]:
                self.over = True
            if self.num_of_pieces <= 2:
                self.over = True
        self.board[end[1]][end[0]] = self.board[start[1]][start[0]]
        self.board[start[1]][start[0]] = 0
        if self.to_move == "white":
            self.to_move = "black"
        else:
            self.to_move = "white"
        if self.board[end[1]][end[0]] == 1 and end[1] == 4:
            self.board[end[1]][end[0]] = 5
        elif self.board[end[1]][end[0]] == 1 and end[1] == 4:
            self.board[end[1]][end[0]] = 11

    def undo_move(self):
        move = self.past_moves.pop()
        self.over = False
        start = move[0]
        end = move[1]
        if self.board[end[1]][end[0]]:
            self.num_of_pieces += 1
        self.board[start[1]][start[0]] = move[2]
        self.board[end[1]][end[0]] = move[3]
        if self.to_move == "white":
            self.to_move = "black"
        else:
            self.to_move = "white"

    def minimax(self, depth, alpha, beta, max_depth=4):
        b = tuple(tuple(sub) for sub in self.board)
        if (b, depth) in self.minmax_evals:
            return self.minmax_evals[(b, depth)]
        if depth == 0:
            time0 = time.time()
            ev = self.evaluate()
            self.eval_time += time.time() - time0
            return ev
        time0 = time.time()
        moves = self.all_moves()
        self.find_move_time += time.time() - time0
        best_move = None
        if not moves:
            return 0
        for move in moves:
            time0 = time.time()
            self.move(move[0], move[1])
            self.move_time += time.time() - time0
            self.tried_moves += 1
            evaluate = -self.minimax(depth - 1, -beta, -alpha, max_depth)
            time0 = time.time()
            self.undo_move()
            self.undo_time += time.time() - time0
            self.minmax_evals[(b, depth)] = evaluate
            if evaluate > beta and depth != max_depth:
                return beta
            if evaluate > alpha:
                alpha = evaluate
                best_move = move
        if depth == max_depth:
            return best_move
        return alpha


def player_move(board):
    chosen = None
    ts = gui.TILE_SIZE
    moved = False
    while not moved:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // ts
                row = 4 - (y // ts)
                if not chosen:
                    if board.board[row][col] != 0:
                        if board.board[row][col] <= 6:
                            chosen = (row, col)
                else:
                    if [col, row] not in board.moves(chosen[1], chosen[0]):
                        chosen = None
                    else:
                        board.move([chosen[1], chosen[0]], [col, row])
                        moved = True
        gui.display_board()
        board.display_pieces()
        if chosen:
            for move in board.moves(chosen[1], chosen[0]):
                pygame.draw.circle(gui.screen, gui.RED, (ts * move[0] + ts/2, ts * (4 - move[1]) + ts/2), ts/8)
        pygame.display.update()


