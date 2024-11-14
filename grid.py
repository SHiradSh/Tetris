import pygame
from piece import BLACK, WHITE

# Set up game window dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Create a grid for the game board
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

# Draw the grid
def draw_grid(surface, grid, score=0):
    surface.fill(BLACK)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw grid lines
    for i in range(GRID_HEIGHT):
        pygame.draw.line(surface, WHITE, (0, i * BLOCK_SIZE), (SCREEN_WIDTH, i * BLOCK_SIZE))
    for j in range(GRID_WIDTH):
        pygame.draw.line(surface, WHITE, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, SCREEN_HEIGHT))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(label, (SCREEN_WIDTH - label.get_width() - 10, 10))

# Check if any rows are completely filled and clear them
def clear_rows(grid, locked):
    increment = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        row = grid[y]
        if BLACK not in row:
            increment += 1
            for x in range(GRID_WIDTH):
                del locked[(x, y)]
            for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
                x, y2 = key
                if y2 < y:
                    new_key = (x, y2 + 1)
                    locked[new_key] = locked.pop(key)
    return increment
