import sounddevice as sd
import numpy as np
import queue

audio_queue = queue.Queue()
CHUNK_SIZE = 1024  # Number of samples per chunk
SAMPLE_RATE = 44100  # Sample rate in Hz

def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_chunk = np.mean(indata, axis=1)
    audio_queue.put(audio_chunk)

def get_blackhole_device():
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if 'BlackHole' in device['name']:
            return i
    raise ValueError("BlackHole device not found. Make sure it's installed and recognized by your system.")

def start_audio_stream():
    device = get_blackhole_device()
    stream = sd.InputStream(device=device, channels=2, samplerate=SAMPLE_RATE, 
                            callback=audio_callback, blocksize=CHUNK_SIZE)
    stream.start()
    return stream

def get_audio_data():
    if not audio_queue.empty():
        return audio_queue.get()
    return np.zeros(CHUNK_SIZE)

if __name__ == "__main__":
    stream = start_audio_stream()
    try:
        while True:
            audio_data = get_audio_data()
            print(f"Audio data shape: {audio_data.shape}, Mean: {np.mean(audio_data):.4f}, Max: {np.max(audio_data):.4f}")
    except KeyboardInterrupt:
        stream.stop()
        print("Audio stream stopped.")