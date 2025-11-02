import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from tone_generator import gen_copy_paste
import traceback
from AudioSeparate import AudioSeparation

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

TRACKS_FOLDER = 'tracks'
os.makedirs(TRACKS_FOLDER, exist_ok=True)

@app.route('/desmosify', methods=['POST'])
def desmosify_audio():
    if 'audio_file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['audio_file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 1. Separate the audio file into tracks
            AudioSeparation(filepath, TRACKS_FOLDER)

            track_names = ['vocals', 'drums', 'bass', 'other']
            all_tracks_latex = {}

            # 2. Process each track individually
            for name in track_names:
                print(f"Processing track: {name}...")
                track_filepath = os.path.join(TRACKS_FOLDER, f"{os.path.splitext(filename)[0]}_{name}.mp3")
                if os.path.exists(track_filepath):
                    latex_strings = gen_copy_paste(track_filepath, interval_length=0.05, num_tones=250, name=name)
                    all_tracks_latex[name] = latex_strings

            return jsonify({"tracks": all_tracks_latex})
        except Exception as e:
            print(f"An error occurred during audio processing: {e}")
            traceback.print_exc()
            return jsonify({"error": f"Failed to process audio: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)