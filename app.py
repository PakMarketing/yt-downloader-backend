from flask import Flask, request, jsonify, send_file
import os
import subprocess

app = Flask(__name__)

# Ensure Correct Cookies Path
COOKIES_FILE = r"C:\Users\PAK MARKETING\Desktop\Python\youtube_cookies.txt"
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "YouTube Downloader API is Running!"

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"error": "No URL provided!"}), 400

    try:
        command = [
            "yt-dlp", 
            "--cookies", COOKIES_FILE,
            "-f", "best",
            "-o", os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            video_url
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500
        
        # Find downloaded file
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.endswith(('.mp4', '.webm', '.mkv')):
                return send_file(os.path.join(DOWNLOAD_FOLDER, file), as_attachment=True)
        
        return jsonify({"error": "Download failed!"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
