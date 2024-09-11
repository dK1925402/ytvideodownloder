from flask import Flask, render_template, request, send_file, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

# Default path where videos will be temporarily saved
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")  # Default Chrome download location

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    try:
        # Set download options, including the file path to Chrome's Downloads folder
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Save video to Downloads folder
        }
        
        # Download video with yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  # Extract video info
            video_title = info_dict.get('title', None)  # Get video title
            video_ext = info_dict.get('ext', None)  # Get video file extension
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.{video_ext}")
        
        # Return file to the browser as a download
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {e}")
        return "Error downloading video", 500

if __name__ == '__main__':
    app.run(debug=True)
