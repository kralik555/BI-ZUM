import pygame
import gui
from board import Board
from board import player_move
import time
import math

pygame.init()

# 5x5 chess

over = False
board = Board()
while not over:
    gui.display_board()
    board.display_pieces()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over = True
    if board.over:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('GAME OVER', True, gui.GREEN, gui.BLUE)
        textRect = text.get_rect()
        textRect.center = (5 * gui.TILE_SIZE // 2, 5 * gui.TILE_SIZE // 2)
        gui.screen.blit(text, textRect)
        pygame.display.update()
        time.sleep(2)
        board = Board()
        continue
    if board.to_move == "black":
        time0 = time.time()
        board.find_move_time = 0
        board.undo_time = 0
        board.move_time = 0
        board.eval_time = 0
        move = board.minimax(6, -math.inf, math.inf, max_depth=6)
        print(time.time() - time0, board.tried_moves)
        print("Undo time:", board.undo_time)
        print("Find move time:", board.find_move_time)
        print("Move time:", board.move_time)
        print("Eval time:", board.eval_time)
        board.tried_moves = 0
        board.move(move[0], move[1])
        gui.display_board()
    else:
        player_move(board)


pygame.quit()
