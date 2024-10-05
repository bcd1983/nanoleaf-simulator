import pygame

# Display settings
WIDTH, HEIGHT = 800, 600
WAVEFORM_RECT = pygame.Rect(WIDTH - 210, 10, 200, 100)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Hexagon properties
HEX_RADIUS = 30
HEX_HEIGHT = HEX_RADIUS * 2
HEX_WIDTH = (3 ** 0.5) * HEX_RADIUS

# Shape settings
NUM_TILES = 10
NUM_SHAPES = 10

# Directions for adjacent hexagons
DIRECTIONS = [
    (HEX_WIDTH, 0),
    (HEX_WIDTH/2, HEX_HEIGHT*3/4),
    (-HEX_WIDTH/2, HEX_HEIGHT*3/4),
    (-HEX_WIDTH, 0),
    (-HEX_WIDTH/2, -HEX_HEIGHT*3/4),
    (HEX_WIDTH/2, -HEX_HEIGHT*3/4)
]