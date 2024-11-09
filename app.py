from flask import Flask, jsonify, send_from_directory, render_template, send_file, redirect, url_for
import os
from xnxx_api import Client, Quality, threaded
from hashlib import sha256
import threading

app = Flask(__name__)

DOWNLOAD_FOLDER = "/tmp/videos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
client = Client()

download_status = {}
status_lock = threading.Lock()

def download_video_async(video_object, video_filename):
    with status_lock:
        download_status[video_filename] = "in-progress"

    video_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

    try:
        video_object.download(downloader=threaded, quality=Quality.BEST, path=video_path)
        with status_lock:
            download_status[video_filename] = "completed"
    except Exception as e:
        with status_lock:
            download_status[video_filename] = f"error: {str(e)}" 

@app.route('/<video_id>/<path:slug>', methods=['GET'])
def start_download(video_id, slug):
    full_url = f"https://xnxx.com/{video_id}/{slug}"

    try:
        video_object = client.get_video(full_url)
    except Exception as e:
        return render_template('error.html', error_message="There was an error retrieving the video details. Are you sure the URL is correct?")

    sha256_name = sha256(video_object.title.encode('utf-8')).hexdigest()
    video_filename = f"{sha256_name}.mp4"
    video_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

    if os.path.exists(video_path):
        return redirect(url_for('serve_video', filename=video_filename))

    with status_lock:
        if video_filename not in download_status:
            thread = threading.Thread(target=download_video_async, args=(video_object, video_filename))
            thread.start()

    return render_template('downloading.html', video_filename=video_filename, original_name=video_object.title)

@app.route('/check_download/<filename>', methods=['GET'])
def check_download(filename):
    with status_lock:
        status = download_status.get(filename, "not_started")
        downloaded = status == "completed"
    response = jsonify({"downloaded": downloaded, "status": status})
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/video/<filename>', methods=['GET'])
def serve_video(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return render_template('error.html', error_message="Video not found"), 404

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message="The page you requested could not be found."), 404

@app.errorhandler(502)
def bad_gateway(error):
    return render_template('error.html', error_message="There was a problem with the server. Please try again later."), 502

if __name__ == '__main__':
    app.run(debug=True)
