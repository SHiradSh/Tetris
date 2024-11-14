def convert_shape_format(shape):
    positions = []
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shape_format):
        for j, column in enumerate(line):
            if column == 1:
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # Offset adjustment
    return positions

# Check if the shape is in a valid position
def valid_space(shape, grid):
    accepted_positions = [[(x, y) for x in range(len(grid[0])) if grid[y][x] == (0, 0, 0)] for y in range(len(grid))]
    accepted_positions = [pos for row in accepted_positions for pos in row]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# Check if the player has lost the game
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
