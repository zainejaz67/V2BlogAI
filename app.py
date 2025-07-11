from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import requests
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
import os

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

# --- Transcript Utilities ---
def get_video_id(youtube_url: str) -> str:
    q = urlparse(youtube_url)
    host = q.hostname
    if host == "youtu.be":
        return q.path.lstrip("/")
    if host in ("www.youtube.com", "youtube.com"):
        if q.path == "/watch":
            return parse_qs(q.query)["v"][0]
        if q.path.startswith(("/embed/", "/v/")):
            return q.path.split("/")[2]
    raise ValueError("Unrecognized YouTube URL format")

def fetch_transcript(video_id: str) -> str:
    try:
        segments = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(seg["text"] for seg in segments)
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "No transcript available (private video, region‑locked, or captions turned off)."

def generate_blog_with_ollama(transcript: str) -> str:
    prompt = (
        "Write a detailed, engaging blog post based on the following YouTube transcript. "
        "The blog MUST start with a single main title at the top (do not repeat this as a subheading). "
        "After the introduction, you MUST organize the content into at least 3 distinct sections, each with its own clear subheading. "
        "Subheadings are mandatory—do not submit a blog without at least 3 subheadings after the introduction. "
        "Make subheadings visually and semantically distinct from the main heading. "
        "Finish with a conclusion. Use subheadings to break up the content and make it easy to read.\n\nTranscript:\n" + transcript
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    if response.ok:
        data = response.json()
        return data.get("response", "(No response from model)")
    return "Failed to generate blog post."

# Remove blog_to_html and /download_blog endpoint

from flask import Response
import re

# --- API Endpoint ---
@app.route('/generate_blog', methods=['POST'])
def generate_blog():
    data = request.get_json()
    youtube_url = data.get('url')
    if not youtube_url:
        return jsonify({"error": "No YouTube URL provided."}), 400
    try:
        video_id = get_video_id(youtube_url)
        transcript = fetch_transcript(video_id)
        if transcript.startswith("Transcripts are disabled") or transcript.startswith("No transcript"):
            return jsonify({"error": transcript}), 400
        blog_post = generate_blog_with_ollama(transcript)
        return jsonify({"blog_post": blog_post})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Serve Frontend ---
@app.route('/')
def serve_index():
    return send_from_directory(STATIC_DIR, 'frontend.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(STATIC_DIR, path)

if __name__ == "__main__":
    app.run(debug=True) 