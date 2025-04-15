from flask import Flask, jsonify, request, session
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secret_key'
CORS(app, supports_credentials=True)

# Użytkownicy testowi
users = {
    "admin": "password123",
    "user": "testpass"
}

plants = []

# Dekorator sprawdzający, czy użytkownik jest zalogowany
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"error": "Brak autoryzacji"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        session['user'] = username
        return jsonify({"message": "Zalogowano jako " + username})
    return jsonify({"error": "Nieprawidłowe dane logowania"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Wylogowano"})

@app.route('/plants', methods=['GET'])
@login_required
def get_plants():
    return jsonify(plants)

@app.route('/plants', methods=['POST'])
@login_required
def add_plant():
    data = request.json
    if not data.get("name") or not data.get("image") or not data.get("description"):
        return jsonify({"error": "Brakuje wymaganych danych (nazwa, obraz, opis)"}), 400
    plants.append({
        "name": data["name"],
        "image": data["image"],
        "description": data["description"]
    })
    return jsonify({"message": "Dodano roślinę!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
