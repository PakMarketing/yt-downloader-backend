from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Test Route to Check if Flask is Running
@app.route("/")
def home():
    return "Flask server is running!"

# YouTube Video Download Route
@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    DOWNLOAD_FOLDER = "downloads"
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return jsonify({"status": "success", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)})

# Flask Run Configuration
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's default port
    app.run(host="0.0.0.0", port=port, debug=True)
