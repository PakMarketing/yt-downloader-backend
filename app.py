@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    print("Received request for URL:", url)  # Debugging log

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
            print("Downloaded file:", filename)  # Debugging log

        if not os.path.exists(filename):
            return jsonify({"error": "File not found"}), 500

        return send_file(filename, as_attachment=True)

    except Exception as e:
        print("Error:", str(e))  # Debugging log
        return jsonify({"error": str(e)}), 500
