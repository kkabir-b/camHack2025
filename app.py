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
            AudioSeparation(filepath, "/tracks")
            latex_strings = gen_copy_paste(filepath, interval_length=0.05, num_tones=250, name='vocals')
            return jsonify({"latex_expressions": latex_strings})
        except Exception as e:
            print(f"An error occurred during audio processing: {e}")
            traceback.print_exc()
            return jsonify({"error": f"Failed to process audio: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)