from flask import Flask, request, jsonify
from services.functions import login_user
app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    User_mail = data.get("User_mail")
    password = data.get("password")

    if not User_mail or not password:
        return jsonify({"error": "Email and password are required"}), 400

    result, status = login_user(User_mail, password)
    return jsonify(result), status

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
