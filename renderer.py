import pygame
import math
from pygame.math import Vector2
from config import BLACK, WHITE, HEX_RADIUS

def draw_hexagon(surface, color, center, intensity):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        x = center[0] + HEX_RADIUS * math.cos(angle_rad)
        y = center[1] + HEX_RADIUS * math.sin(angle_rad)
        points.append((x, y))
    
    adjusted_color = tuple(min(255, int(c * intensity)) for c in color)
    
    pygame.draw.polygon(surface, adjusted_color, points)
    pygame.draw.aalines(surface, BLACK, True, points, 1)

def draw_power_cord(surface, shape, offset_x, offset_y, outlet_side):
    bottom_tile = max(shape, key=lambda tile: tile[1])
    cord_start = Vector2(bottom_tile[0] + offset_x, bottom_tile[1] + offset_y + HEX_RADIUS)
    
    if outlet_side == 'left':
        cord_end = Vector2(0, surface.get_height())
    else:  # right side
        cord_end = Vector2(surface.get_width(), surface.get_height())
    
    control_point = Vector2((cord_start.x + cord_end.x) / 2, cord_start.y + (cord_end.y - cord_start.y) / 3)
    
    points = [(cord_start.x, cord_start.y)]
    for t in range(1, 101):
        t = t / 100
        x = (1-t)**2 * cord_start.x + 2*(1-t)*t * control_point.x + t**2 * cord_end.x
        y = (1-t)**2 * cord_start.y + 2*(1-t)*t * control_point.y + t**2 * cord_end.y
        points.append((x, y))
    
    pygame.draw.aalines(surface, BLACK, False, points, 2)

def draw_waveform(surface, audio_data, rect):
    pygame.draw.rect(surface, WHITE, rect)
    pygame.draw.rect(surface, BLACK, rect, 1)
    
    points = []
    for i, sample in enumerate(audio_data):
        x = rect.left + i * rect.width / len(audio_data)
        y = rect.centery + sample * rect.height / 2
        points.append((x, y))
    
    if len(points) > 1:
        pygame.draw.aalines(surface, BLACK, False, points, 1)