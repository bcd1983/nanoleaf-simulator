import random
from config import DIRECTIONS, HEX_WIDTH

def generate_shape(num_tiles):
    shape = [(0, 0)]
    for _ in range(num_tiles - 1):
        added = False
        while not added:
            base_tile = random.choice(shape)
            direction = random.choice(DIRECTIONS)
            new_tile = (base_tile[0] + direction[0], base_tile[1] + direction[1])
            if new_tile not in shape:
                shape.append(new_tile)
                added = True
    return shape

def recognize_shape(shape):
    width = max(tile[0] for tile in shape) - min(tile[0] for tile in shape)
    height = max(tile[1] for tile in shape) - min(tile[1] for tile in shape)
    aspect_ratio = width / height if height != 0 else float('inf')
    
    num_tiles = len(shape)
    
    if aspect_ratio > 1.5:
        return "Snake" if num_tiles < 8 else "Dragon"
    elif aspect_ratio < 0.67:
        return "Tree" if num_tiles < 8 else "Tower"
    elif 0.9 < aspect_ratio < 1.1:
        return "Blob" if num_tiles < 8 else "Cloud"
    else:
        extremities = sum(1 for tile in shape if sum(1 for t in shape if abs(t[0]-tile[0])+abs(t[1]-tile[1]) == HEX_WIDTH) == 1)
        if extremities > 3:
            return "Starfish" if num_tiles < 8 else "Octopus"
        elif extremities == 3:
            return "Bird" if aspect_ratio > 1 else "Fish"
        elif extremities == 2:
            return "Fox" if aspect_ratio > 1 else "Rabbit"
        else:
            return "Turtle" if aspect_ratio > 1 else "Bear"