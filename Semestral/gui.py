import pygame

pygame.init()

TILE_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0, 50)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((5 * TILE_SIZE, 5 * TILE_SIZE))
pygame.display.set_caption("5x5 chess")


def display_board():
    for i in range(5):
        for j in range(5):
            x = i * TILE_SIZE
            y = j * TILE_SIZE
            color = WHITE if (i + j) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, [x, y, TILE_SIZE, TILE_SIZE])


def display_piece(player_color, sprite, x, y):
    """
    Displays a piece sprite
    Tile says where it should be displayed
    And player color if it should be mirrored
    """
    ts = TILE_SIZE
    sprite = pygame.transform.scale(sprite, (ts, ts))
    if player_color == "black":
        screen.blit(sprite, (x * ts, y * ts))
    else:
        screen.blit(sprite, (x * ts, (4 - y) * ts))
