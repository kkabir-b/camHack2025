import os
from audio_separator.separator import Separator



def AudioSeparation(inputFile, outputFolder):

    # --- Configuration ---
    INPUT_FILE = inputFile  # Replace with your audio file
    OUTPUT_DIR = outputFolder       # Folder to save the separated tracks
    # ---------------------
    print(f"Initializing separator...")

    # Initialize the Separator
    sp = Separator(output_dir = OUTPUT_DIR, output_format="mp3")
    sp.load_model(model_filename="htdemucs_ft.yaml")

    custom_names = {
        'vocals': 'vocals',
        'drums': 'drums',
        'bass': 'bass',
        'other': 'other'
    }

    print(f"Loading and processing file: {INPUT_FILE}")

    # Run the separation
    output_paths = sp.separate(INPUT_FILE, custom_output_names=custom_names)

    print(f"Separation complete!")
    print(f"Find your separated tracks in: {OUTPUT_DIR}")
    for path in output_paths:
        print(path)

if __name__ == "__main__":
    AudioSeparation("Monkeys-Spinning-Monkeys(chosic.com).mp3", "SeparatedTracks")