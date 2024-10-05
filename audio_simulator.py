import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def simulate_audio_data(num_samples, t):
    frequencies = [2, 3, 5, 7, 11, 13]
    amplitudes = [0.5, 0.3, 0.2, 0.1, 0.05, 0.025]
    audio_data = np.zeros(num_samples)
    for freq, amp in zip(frequencies, amplitudes):
        audio_data += amp * np.sin(2 * np.pi * freq * t / num_samples)
    
    # Log a sample of the audio data
    logging.info(f"Audio data sample (first 5 values): {audio_data[:5]}")
    logging.info(f"Audio data stats - Min: {audio_data.min():.2f}, Max: {audio_data.max():.2f}, Mean: {audio_data.mean():.2f}")
    
    return audio_data