from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

COBALT_API = "http://localhost:9000"

@app.route("/")
def home():
    return {
        "status": "running",
        "service": "cobalt wrapper api"
    }

@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "success": False,
            "error": "Missing URL"
        }), 400

    try:
        payload = {
            "url": url,
            "vCodec": "h264",
            "vQuality": "720",
            "filenamePattern": "basic",
            "isAudioOnly": False
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(
            COBALT_API,
            json=payload,
            headers=headers,
            timeout=60
        )

        data = response.json()

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
