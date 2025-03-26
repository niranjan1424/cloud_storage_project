from flask import Flask, request, jsonify, render_template, send_file
from mega import Mega
import os

app = Flask(__name__)

# Use environment variables for credentials
MEGA_EMAIL = os.getenv("MEGA_EMAIL", "your_email_here")
MEGA_PASSWORD = os.getenv("MEGA_PASSWORD", "your_password_here")

# Ensure credentials are provided
if MEGA_EMAIL == "your_email_here" or MEGA_PASSWORD == "your_password_here":
    raise ValueError("Set MEGA_EMAIL and MEGA_PASSWORD as environment variables.")

mega = Mega()
mega_instance = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

# Secure authentication credentials
USERNAME = os.getenv("APP_USERNAME", "niranjan")
PASSWORD = os.getenv("APP_PASSWORD", "naan dhan")

# Download folder setup
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

def check_auth(auth):
    """Verify username and password securely."""
    return auth and auth.username == USERNAME and auth.password == PASSWORD

@app.route("/")
def home():
    """Render the frontend without authentication."""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """Upload file to Mega.nz with authentication."""
    auth = request.authorization
    if not check_auth(auth):
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(DOWNLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        mega_instance.upload(file_path)
        os.remove(file_path)  # Cleanup after upload
        return jsonify({"message": f"File '{file.filename}' uploaded successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list_files", methods=["GET"])
def list_files():
    """List files stored in Mega.nz with authentication."""
    auth = request.authorization
    if not check_auth(auth):
        return jsonify({"error": "Unauthorized"}), 401

    files = mega_instance.get_files()
    file_list = [{"name": file["a"]["n"], "id": file["h"]} for file in files.values() if "a" in file and "n" in file["a"]]

    return jsonify({"files": file_list})

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """Download file from Mega.nz with authentication."""
    auth = request.authorization
    if not check_auth(auth):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        files = mega_instance.get_files()
        file_id = None

        for file_key, file_info in files.items():
            if isinstance(file_info, dict) and "a" in file_info and "n" in file_info["a"]:
                if file_info["a"]["n"] == filename:
                    file_id = file_key
                    break

        if not file_id:
            return jsonify({"error": f"File '{filename}' not found on Mega.nz"}), 404

        file_path = mega_instance.download(file_id, DOWNLOAD_FOLDER)
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": "Download failed, file not found."}), 500

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)