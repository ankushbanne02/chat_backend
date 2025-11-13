import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # ✅ Allow requests from any domain
# You can restrict it later like: CORS(app, origins=["https://yourfrontend.com"])

API_KEY = "AIzaSyAsndoGdHcrFdlQsoA-i1pghUT7gAzsrKU"
MODEL = "gemini-2.0-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

@app.route("/ask", methods=["POST"])
def ask_gemini():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    payload = {"contents": [{"parts": [{"text": question}]}]}

    try:
        response = requests.post(
            URL,
            params={"key": API_KEY},
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        res_json = response.json()

        if "candidates" in res_json and res_json["candidates"]:
            answer = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            return jsonify({"answer": answer})
        else:
            return jsonify({"error": "No response from model", "raw": res_json}), 500

    except requests.exceptions.HTTPError as e:
        return jsonify({
            "error": "HTTP Error",
            "status_code": e.response.status_code,
            "details": e.response.text
        }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
