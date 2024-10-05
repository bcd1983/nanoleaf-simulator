# Nanoleaf Shape Generator

This project simulates a Nanoleaf-like display with dynamic, audio-reactive hexagon shapes. It uses Python with Pygame for graphics and NumPy for audio simulation.

## Project Structure

- `main.py`: Entry point for the application.
- `renderer.py`: Handles rendering of shapes and visual effects.
- `audio_capture.py`: Manages audio input and processing.
- `visual_effects.py`: Contains functions for applying visual effects based on audio input.
- `config.py`: Configuration settings for the application.
- `utils.py`: Utility functions used across the project.
- `assets/`: Contains image assets used for textures.
- `shapes/`: Stores shape data and images.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Homebrew (for macOS users)

## Installation

### Step 1: Install Homebrew (macOS only)

If you're using macOS and don't have Homebrew installed, follow these steps:

1. Open Terminal.
2. Run the following command:

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. Follow the prompts to complete the installation.

### Step 2: Set up the project

1. Clone or download this repository to your local machine.
2. Open a terminal and navigate to the project directory.

### Step 3: Create and activate a virtual environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS and Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 4: Install dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### Windows Installation

1. Ensure Python and pip are installed.
2. Follow steps 2 to 4 above.

### Linux Installation

1. Ensure Python and pip are installed.
2. Follow steps 2 to 4 above.

## Running the Application

To run the Nanoleaf Shape Generator:

1. Ensure your virtual environment is activated.
2. Run the following command:

   ```bash
   python main.py
   ```

## Controls

- Use the left and right arrow keys to cycle through different shapes.
- Press Cmd+Enter (Mac) or Ctrl+Enter (Windows/Linux) to save the current shape as a PNG. Outputs to the project directory in /output.

## Troubleshooting

If you encounter any issues with Pygame, try upgrading it:

```bash
pip install --upgrade pygame
```

For any other problems, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. You are free to fork, modify, and use it as you wish.

## Screenshots

[Consider adding screenshots or a demo video here.]