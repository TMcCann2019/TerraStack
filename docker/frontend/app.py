from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://api-svc:8081")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-yard-quote", methods=["POST"])
def get_yard_quote():
    sqft = request.form.get("sqft")
    if not sqft or not sqft.isdigit():
        return jsonify({"error": "Invalid square footage"}), 400
    try:
        response = requests.get(f"{BACKEND_URL}/yard-quote", params={"sqft": sqft}, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to get quote", "details": str(e)}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)