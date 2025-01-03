
# Flask Video Processing Application

This Flask application enables users to upload video files, process them by trimming into chunks, and download the processed video chunks. It supports uploading large video files (up to 500 MB), handles errors gracefully, and provides endpoints for managing uploaded and processed files.

## Features
- **Upload Video Files**: Accepts video files for processing.
- **Trim Videos into Chunks**: Processes uploaded videos into smaller chunks.
- **Manage Files**: Delete uploaded files when no longer needed.
- **Download Processed Chunks**: Download individual processed video chunks.
- **API and Web Interface**: Includes both API endpoints and web-based file management.

---

## Requirements
### Dependencies
Install the required dependencies using `pip`:
```bash
pip install flask werkzeug
```

### Folder Structure
The application relies on the following folder structure:
- `uploads/`: Stores uploaded video files.
- `processed/`: Stores processed video chunks.

Both folders are automatically created when the application runs.

---

## Getting Started

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone <repository-url>
```

### 2. Navigate to the Project Directory
```bash
cd <project-directory>
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
The application will start in debug mode and run at `http://127.0.0.1:5000/`.

---

## API Endpoints

### 1. **Homepage**
- **URL**: `/`
- **Method**: `GET`
- **Description**: Renders the upload page.

### 2. **Upload File**
- **URL**: `/upload`
- - **Method**: `POST`
- **Payload**: A video file in the `file` field of a `multipart/form-data` request.
- **Response**:
  - `200`: Success, returns the uploaded file name.
  - `400`: Error, invalid or missing file.

### 3. **Delete File**
- **URL**: `/upload/<filename>`
- **Method**: `DELETE`
- **Description**: Deletes an uploaded file by filename.
- **Response**:
  - `200`: Success, file deleted.
  - `404`: Error, file not found.

### 4. **Process File**
- **URL**: `/process/<filename>`
- **Method**: `POST`
- **Description**: Trims the specified video into smaller chunks and stores them in the `processed` folder.
- **Response**:
  - `200`: Success, returns URLs of processed chunks.
  - `404`: Error, file not found.

### 5. **Get Processed Chunks**
- **URL**: `/get_processed_chunks`
- **Method**: `GET`
- **Query Parameter**: `folder` - Name of the folder containing processed chunks.
- **Response**:
  - `200`: Success, returns a list of chunks.
  - `400`: Error, folder not specified.
  - `404`: Error, folder not found.

### 6. **Download File**
- **URL**: `/download/<path:filename>`
- **Method**: `GET`
- **Description**: Downloads a specific processed video chunk.
- **Response**:
  - `200`: Success, downloads the file.
  - `404`: Error, file not found.

### 7. **Results Page**
- **URL**: `/results`
- **Method**: `GET`
- **Query Parameter**: `folder` - Name of the folder containing results.
- **Description**: Renders the results page for a given folder.

### 8. **Error Handling**
- **413**: File too large (above 500 MB).

---

## Processing Logic
The `trim_video_to_chunks` function, imported from `video_processing`, handles splitting video files into smaller chunks and saves them in the `processed` directory. Ensure this module is implemented correctly for processing.

---

## File Upload Limit
The maximum upload size is set to **500 MB**. This can be adjusted by modifying:
```python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Adjust value as needed
```

---

## Templates
- **`upload.html`**: A web interface for uploading videos.
- **`results.html`**: Displays the processed chunks for a given folder.

Ensure these templates exist in a `templates` directory in the project root.

---

## Contributing
1. Fork the repository.
2. Create a new feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push the branch: `git push origin feature-name`
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
 