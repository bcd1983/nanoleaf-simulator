import pygame
import random
import logging
import numpy as np
from config import WIDTH, HEIGHT, WAVEFORM_RECT, WHITE, BLACK, NUM_TILES, NUM_SHAPES
from shape_generator import generate_shape, recognize_shape
from audio_capture import start_audio_stream, get_audio_data
from visual_effects import initialize_color_transitions, apply_audio_effect
from renderer import draw_hexagon, draw_power_cord, draw_waveform
from utils import normalize_safely, save_transparent_png

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for slider
SLIDER_MIN = 7
SLIDER_MAX = 21
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 20
SLIDER_X = 25  # Updated X position
SLIDER_Y = 25  # Updated Y position


def smooth_audio_data(audio_data, smoothing_factor=0.2):
    return np.convolve(audio_data, np.ones(int(len(audio_data) * smoothing_factor)) / int(len(audio_data) * smoothing_factor), mode='same')


def draw_slider(screen, value, font):
    # Draw the slider track
    pygame.draw.rect(screen, BLACK, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT), 2)
    
    # Calculate the position of the indicator
    indicator_x = SLIDER_X + ((value - SLIDER_MIN) / (SLIDER_MAX - SLIDER_MIN)) * SLIDER_WIDTH
    
    # Draw the indicator as a small circle
    pygame.draw.circle(screen, BLACK, (int(indicator_x), SLIDER_Y + SLIDER_HEIGHT // 2), 10)
    
    # Draw label
    label = font.render("Number of Tiles", True, BLACK)
    screen.blit(label, (SLIDER_X, SLIDER_Y - 25))
    
    # Draw current value
    value_text = font.render(str(value), True, BLACK)
    screen.blit(value_text, (SLIDER_X + SLIDER_WIDTH + 10, SLIDER_Y))


def get_slider_value(mouse_x):
    if SLIDER_X <= mouse_x <= SLIDER_X + SLIDER_WIDTH:
        return SLIDER_MIN + (mouse_x - SLIDER_X) / SLIDER_WIDTH * (SLIDER_MAX - SLIDER_MIN)
    return None


def draw_loading_animation(screen, center, radius, angle):
    # Draw a rotating circle as a loading animation
    end_angle = angle + 30
    pygame.draw.arc(screen, BLACK, (center[0] - radius, center[1] - radius, radius * 2, radius * 2), np.radians(angle), np.radians(end_angle), 5)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Nanoleaf Hexagon Shape Generator with Smooth Audio Reactivity")

    clock = pygame.time.Clock()
    num_tiles = NUM_TILES
    shapes = [generate_shape(num_tiles) for _ in range(NUM_SHAPES)]
    shape_names = [recognize_shape(shape) for shape in shapes]
    outlet_sides = [random.choice(['left', 'right']) for _ in range(NUM_SHAPES)]
    current_shape_index = 0
    
    font = pygame.font.Font(None, 36)
    color_transitions = initialize_color_transitions(num_tiles)
    
    # Start audio stream
    audio_stream = start_audio_stream()
    
    running = True
    dragging_slider = False  # Flag to track if the slider is being dragged
    loading = False  # Flag to indicate loading state
    loading_angle = 0  # Angle for loading animation
    fade_alpha = 255  # Alpha value for fade effect
    audio_buffer = np.zeros(1024)
    smoothed_audio_buffer = np.zeros(1024)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_shape_index = (current_shape_index - 1) % len(shapes)
                elif event.key == pygame.K_RIGHT:
                    current_shape_index = (current_shape_index + 1) % len(shapes)
                elif event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_META:
                    filename = f"nanoleaf_{shape_names[current_shape_index].lower()}_{current_shape_index + 1}.png"
                    saved_path = save_transparent_png(screen, filename)
                    print(f"Shape saved as: {saved_path}")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SLIDER_Y <= event.pos[1] <= SLIDER_Y + SLIDER_HEIGHT:
                    dragging_slider = True
            if event.type == pygame.MOUSEBUTTONUP:
                dragging_slider = False

        # Update slider value if dragging
        if dragging_slider:
            mouse_x, _ = pygame.mouse.get_pos()
            new_value = get_slider_value(mouse_x)
            if new_value is not None:
                num_tiles = int(new_value)
                shapes = [generate_shape(num_tiles) for _ in range(NUM_SHAPES)]
                shape_names = [recognize_shape(shape) for shape in shapes]
                color_transitions = initialize_color_transitions(num_tiles)
                loading = True  # Start loading animation

        screen.fill(WHITE)

        # Draw slider with label and current value
        draw_slider(screen, num_tiles, font)

        # Draw loading animation if loading
        if loading:
            draw_loading_animation(screen, (WIDTH // 2, HEIGHT // 2), 50, loading_angle)
            loading_angle = (loading_angle + 5) % 360
            fade_alpha = max(0, fade_alpha - 5)  # Fade out effect
            if fade_alpha == 0:
                loading = False  # Stop loading when fade out is complete
                fade_alpha = 255  # Reset alpha for next load

        shape = shapes[current_shape_index]
        outlet_side = outlet_sides[current_shape_index]

        min_x = min(tile[0] for tile in shape)
        max_x = max(tile[0] for tile in shape)
        min_y = min(tile[1] for tile in shape)
        max_y = max(tile[1] for tile in shape)
        offset_x = (WIDTH - (max_x - min_x)) / 2 - min_x
        offset_y = (HEIGHT - (max_y - min_y)) / 2 - min_y

        # Get latest audio data
        new_audio_data = get_audio_data()
        audio_buffer = np.roll(audio_buffer, -len(new_audio_data))
        audio_buffer[-len(new_audio_data):] = new_audio_data
        
        # Apply smoothing to the audio data
        smoothed_audio = smooth_audio_data(audio_buffer)
        smoothed_audio_buffer = np.roll(smoothed_audio_buffer, -len(smoothed_audio))
        smoothed_audio_buffer[-len(smoothed_audio):] = smoothed_audio
        
        normalized_audio = normalize_safely(smoothed_audio_buffer)
        
        for i, tile in enumerate(shape):
            center = (tile[0] + offset_x, tile[1] + offset_y)
            audio_index = int((i / len(shape)) * len(normalized_audio))
            color, intensity = apply_audio_effect(color_transitions[i], normalized_audio[audio_index])
            color = pygame.Color(*color)  # Convert to pygame.Color
            color.a = fade_alpha  # Apply fade effect
            draw_hexagon(screen, color, center, intensity)
            color_transitions[i].update()
            
            if i == 0:  # Log details for the first hexagon in each frame
                logging.debug(f"Hexagon 1 - Color: {color}, Intensity: {intensity:.2f}")

        draw_power_cord(screen, shape, offset_x, offset_y, outlet_side)

        shape_name = shape_names[current_shape_index]
        text = font.render(shape_name, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH/2, 30))
        screen.blit(text, text_rect)

        draw_waveform(screen, smoothed_audio_buffer, WAVEFORM_RECT)

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

        logging.debug("Frame completed.")

    audio_stream.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
