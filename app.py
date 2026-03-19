from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import uuid, os, tempfile

app = Flask(__name__)

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Generate a unique filename
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(tempfile.gettempdir(), filename)

    # Convert text to speech
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(filepath)

    # Return the audio file directly
    return send_file(filepath, mimetype="audio/mpeg", as_attachment=False)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

---

**File 2: `requirements.txt`**
```
flask==3.0.3
gTTS==2.5.1
gunicorn==22.0.0