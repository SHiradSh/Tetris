import pygame
import random
from piece import Piece, SHAPES, SHAPE_COLORS
from grid import create_grid, draw_grid, clear_rows
from helper import convert_shape_format, valid_space, check_lost

# Set up game window dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Main function
def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Piece(5, 0, random.choice(SHAPES))
    next_piece = Piece(5, 0, random.choice(SHAPES))
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    # Game loop
    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        clock.tick()

        # Handle piece falling
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        # Add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        # If the piece reaches the bottom, lock the position
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Piece(5, 0, random.choice(SHAPES))
            change_piece = False
            # Check for cleared rows
            score += clear_rows(grid, locked_positions) * 10

        draw_grid(surface, grid, score)

        # Check if the game is over
        if check_lost(locked_positions):
            run = False

    pygame.display.quit()

if __name__ == "__main__":
    main()
