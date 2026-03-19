from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import uuid, os, tempfile

app = Flask(__name__)

AUDIO_DIR = tempfile.gettempdir()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "gTTS service running"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# POST /speak — returns JSON with audio_url
@app.route("/speak", methods=["POST"])
def speak_post():
    data = request.get_json()
    text = data.get("text", "") if data else ""
    if not text:
        return jsonify({"error": "No text provided"}), 400
    filename = _generate_audio(text)
    base_url = request.host_url.rstrip("/")
    return jsonify({"audio_url": f"{base_url}/audio/{filename}"})

# GET /speak?text=... — returns JSON with audio_url (for Recall.ai)
@app.route("/speak", methods=["GET"])
def speak_get():
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    filename = _generate_audio(text)
    base_url = request.host_url.rstrip("/")
    return jsonify({"audio_url": f"{base_url}/audio/{filename}"})

# GET /audio/<filename> — serves the actual MP3 file
@app.route("/audio/<filename>", methods=["GET"])
def serve_audio(filename):
    filepath = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath, mimetype="audio/mpeg", as_attachment=False)

# GET /tts?text=... — returns the MP3 directly (what Recall.ai needs)
@app.route("/tts", methods=["GET"])
def tts_direct():
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    filename = _generate_audio(text)
    filepath = os.path.join(AUDIO_DIR, filename)
    return send_file(filepath, mimetype="audio/mpeg", as_attachment=False)

def _generate_audio(text):
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(filepath)
    return filename

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)