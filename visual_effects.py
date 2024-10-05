import random
import colorsys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft


def generate_smooth_color(h):
    s = random.uniform(0.5, 0.8)  # Reduced saturation range
    v = random.uniform(0.6, 0.9)  # Increased brightness range
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


class ColorTransition:
    def __init__(self, start_color, end_color, duration_frames):
        self.start_color = np.array(start_color)
        self.end_color = np.array(end_color)
        self.duration_frames = duration_frames
        self.current_frame = 0
        self.smoothed_audio = 0

    def get_current_color(self):
        progress = self.current_frame / self.duration_frames
        current_color = self.start_color + (self.end_color - self.start_color) * progress
        return tuple(int(c) for c in current_color)

    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.duration_frames:
            self.start_color = self.end_color
            self.end_color = np.array(generate_smooth_color(random.random()))
            self.current_frame = 0


def apply_audio_effect(color_transition, audio_value):
    # Smooth the audio input
    color_transition.smoothed_audio = color_transition.smoothed_audio * 0.9 + audio_value * 0.1

    base_color = color_transition.get_current_color()
    intensity = 1.0 + color_transition.smoothed_audio * 0.5  # Reduced intensity range

    h, s, v = colorsys.rgb_to_hsv(*(c/255 for c in base_color))
    v = min(1.0, v * intensity)  # Adjust brightness based on smoothed audio
    color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))

    return color, intensity


def initialize_color_transitions(num_tiles):
    return [ColorTransition(
        generate_smooth_color(random.random()),
        generate_smooth_color(random.random()),
        random.randint(180, 360)  # Longer transition duration (3-6 seconds at 60 FPS)
    ) for _ in range(num_tiles)]


def mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    x, y = np.linspace(xmin, xmax, width), np.linspace(ymin, ymax, height)
    C = np.array(np.meshgrid(x, y)).T.reshape(-1, 2)
    Z = np.zeros(C.shape[0], dtype=complex)
    M = np.full(C.shape[0], True, dtype=bool)
    N = np.zeros(C.shape[0], dtype=int)

    for i in range(max_iter):
        Z[M] = Z[M] ** 2 + C[M][:, 0] + 1j * C[M][:, 1]
        M[np.abs(Z) > 2] = False
        N[M] = i

    return N.reshape(width, height)


def load_audio(filename):
    samplerate, data = wavfile.read(filename)
    audio_fft = fft(data)
    audio_freqs = np.abs(audio_fft)
    return audio_freqs


def plot_3d_fractal_with_audio(audio_freqs, fractal, width, height):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.linspace(0, width, width)
    y = np.linspace(0, height, height)
    X, Y = np.meshgrid(x, y)

    # Normalize audio frequencies to fit fractal dimensions
    audio_scaled = np.interp(audio_freqs[:width], (audio_freqs.min(), audio_freqs.max()), (-1, 1))

    # Plot the fractal, modulated by audio frequencies
    Z = fractal * audio_scaled[:, np.newaxis]

    ax.plot_surface(X, Y, Z, cmap='inferno')
    plt.show()


def visualize_waveform_with_fractal(audio_file):
    # Define parameters
    width, height = 500, 500
    fractal = mandelbrot(-2.0, 0.5, -1.25, 1.25, width, height, 100)

    # Load your audio file
    audio_freqs = load_audio(audio_file)

    # Plot 3D fractal with audio modulation
    plot_3d_fractal_with_audio(audio_freqs, fractal, width, height)
