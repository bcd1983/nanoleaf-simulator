import os
import pygame
import numpy as np

def normalize_safely(data):
    min_val = np.min(data)
    max_val = np.max(data)
    if min_val == max_val:
        return np.zeros_like(data)
    return (data - min_val) / (max_val - min_val)

def save_transparent_png(surface, filename):
    shapes_dir = os.path.join(os.getcwd(), 'shapes')
    os.makedirs(shapes_dir, exist_ok=True)
    file_path = os.path.join(shapes_dir, filename)
    surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    surf.fill((255,255,255,0))
    surf.blit(surface, (0,0))
    pygame.image.save(surf, file_path)
    return file_path