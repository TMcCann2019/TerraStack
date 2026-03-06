from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_URL = "http://backend-svc:8000"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check-backend")
def check_backend():
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)