from flask import Flask, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from video_processing import trim_video_to_chunks

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Limit file size to 500 MB

# Ensure the upload and processed folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/results')
def results():
    # Access the query parameter
    folder_name = request.args.get('folder')
    
    # Check if folder_name is passed correctly
    if folder_name:
        return render_template('results.html', folder=folder_name)
    else:
        return "No folder name provided", 400  # Bad request if folder is missing

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file is a video
    if not file.content_type.startswith('video/'):
        return jsonify({'error': 'Invalid file type. Please upload a video file.'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return jsonify({'filename': filename}), 200

@app.route('/upload/<filename>', methods=['DELETE'])
def delete_file(filename):
    decoded_filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], decoded_filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "File deleted"}), 200
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/process/<filename>', methods=['POST'])
def process_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # Process the video
    output_dir = os.path.join(app.config['PROCESSED_FOLDER'], filename.rsplit('.', 1)[0])
    os.makedirs(output_dir, exist_ok=True)
    trim_video_to_chunks(file_path, output_dir)

    # List processed files in the output directory
    processed_files = os.listdir(output_dir)
    processed_files = [url_for('download_file', filename=os.path.join(filename.rsplit('.', 1)[0], f)) for f in processed_files]

    # Return the list of processed files
    return jsonify({'processed_files': processed_files}), 200


@app.route('/get_processed_chunks')
def get_processed_chunks():
    folder_name = request.args.get('folder')

    if not folder_name:
        return jsonify({'error': 'Folder not specified'}), 400

    folder_path = os.path.join(app.config['PROCESSED_FOLDER'], folder_name)

    if not os.path.exists(folder_path):
        return jsonify({'error': 'Folder not found'}), 404

    chunks = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
    
    return jsonify({'chunks': [{'fileName': chunk} for chunk in chunks]})


@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)

@app.errorhandler(413)
def request_entity_too_large(error):
    return "File too large. Please upload a smaller file.", 413

if __name__ == "__main__":
    app.run(debug=True)

