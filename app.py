import os
from flask import Flask, request, jsonify, Response
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY       = os.getenv("CAPTIONS_API_KEY")
CAPTIONS_BASE = "https://api.captions.ai/api"

app = Flask(__name__)

def forward(path: str) -> Response:
    """
    Forward the incoming JSON POST to Captions.ai API,
    inject x-api-key header, and relay back the response.
    """
    url = f"{CAPTIONS_BASE}/{path}"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    # Grab JSON body if present, else empty dict
    payload = request.get_json(silent=True) or {}
    resp = requests.post(url, json=payload, headers=headers)

    # Filter out hop-by-hop headers
    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    headers_out = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded]

    return Response(resp.content, status=resp.status_code, headers=headers_out)

# ----- AI Creator Endpoints -----
@app.route("/creator/list", methods=["POST"])
def list_creators():
    return forward("creator/list")

@app.route("/creator/submit", methods=["POST"])
def submit_video():
    return forward("creator/submit")

@app.route("/creator/poll", methods=["POST"])
def poll_video():
    return forward("creator/poll")

# ----- AI Edit Endpoints -----
@app.route("/edit/styles", methods=["POST"])
def list_edit_styles():
    return forward("edit/styles")

@app.route("/edit/submit", methods=["POST"])
def submit_edit():
    return forward("edit/submit")

@app.route("/edit/poll", methods=["POST"])
def poll_edit():
    return forward("edit/poll")

# ----- AI Twin Endpoints -----
@app.route("/twin/supported-languages", methods=["POST"])
def twin_supported_languages():
    return forward("twin/supported-languages")

@app.route("/twin/list", methods=["POST"])
def twin_list():
    return forward("twin/list")

@app.route("/twin/create", methods=["POST"])
def twin_create():
    return forward("twin/create")

@app.route("/twin/script", methods=["POST"])
def twin_script():
    return forward("twin/script")

@app.route("/twin/status", methods=["POST"])
def twin_status():
    return forward("twin/status")

@app.route("/twin/delete", methods=["POST"])
def twin_delete():
    return forward("twin/delete")

if __name__ == "__main__":
    # Start the Flask development server
    app.run(host="0.0.0.0", port=5000)

