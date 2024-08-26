from flask import Flask, request, jsonify, send_file
from googleapiclient.discovery import build
import os
import requests

app = Flask(__name__)

# Remplace ta clé API ici
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def search_youtube_videos(title, max_results=6):
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            part="snippet",
            q=title,
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        videos = []

        for item in response.get("items", []):
            video = {
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"],
                "thumb": item["snippet"]["thumbnails"]["high"]["url"]
            }
            videos.append(video)

        return videos
    except Exception as e:
        print(f"Error during YouTube search: {str(e)}")
        raise

@app.route('/yts', methods=['GET'])
def get_videos():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "Title parameter is required"}), 400
    
    try:
        videos = search_youtube_videos(title)
        return jsonify({"videos": videos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['GET'])
def download_audio():
    video_url = request.args.get('video_url')
    title = request.args.get('title')

    if not video_url or not title:
        return jsonify({"error": "video_url and title parameters are required"}), 400

    try:
        # Simuler le téléchargement de l'audio à partir de l'URL vidéo
        audio_file_path = f"{title}.mp3"

        if not os.path.exists(audio_file_path):
            return jsonify({"error": "Audio file not found"}), 404

        # Envoyer le fichier tel quel au client pour téléchargement
        return send_file(audio_file_path, as_attachment=True)
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {str(e)}")
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        print(f"Error during file handling: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
