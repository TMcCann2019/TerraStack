from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Backend URL from ConfigMap / environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://api-svc:8081")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/check-backend", methods=["GET"])
def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-yard-quote", methods=["POST"])
def get_yard_quote():
    # Parse form data robustly
    sqft = request.form.get("sqft")
    try:
        sqft = float(sqft)
        if sqft <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "Please provide a valid 'sqft' value."}), 400

    try:
        # Call backend directly
        response = requests.get(f"{BACKEND_URL}/quote?sqft={sqft}", timeout=5)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Must bind to 0.0.0.0 inside container so external traffic works
    app.run(host="0.0.0.0", port=5000, debug=True)