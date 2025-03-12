from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

# Downloaded files ka folder
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url):
    """YouTube video ko download karne ka function"""
    try:
        ydl_opts = {
            'cookiefile': 'youtube_cookies.txt',  # ✅ Cookies file ka path
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',  # ✅ File save karne ka format
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',  # ✅ MP4 format me merge
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename  # ✅ Return file ka path

    except Exception as e:
        return str(e)

@app.route("/download", methods=["GET"])
def download():
    """API route jo YouTube video ko download karega"""
    url = request.args.get("url")
    
    if not url:
        return jsonify({"error": "URL parameter missing"}), 400
    
    filepath = download_video(url)
    
    if not os.path.exists(filepath):
        return jsonify({"error": "Download failed"}), 500
    
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
