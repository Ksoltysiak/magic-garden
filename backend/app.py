from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

# KONFIGURACJA SESJI I CIASTECZEK
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',  # Zezwól na współdzielenie ciasteczek między domenami
    SESSION_COOKIE_SECURE=False     # Wyłącz HTTPS-only dla localhost
)

# INICJALIZACJA CORS
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"]
)

# Inicjalizacja SQLAlchemy
db = SQLAlchemy(app)


# Użytkownicy testowi
users = {
    "admin": "password123",
    "user": "testpass"
}

# Model rośliny
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Plant {self.name}>"

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
    plants = Plant.query.all()
    return jsonify([
        {
            "id": plant.id,  # Dodaj ID!
            "name": plant.name,
            "image": plant.image,
            "description": plant.description
        } for plant in plants
    ])

@app.route('/plants', methods=['POST'])
@login_required
def add_plant():
    data = request.json
    if not data.get("name") or not data.get("image") or not data.get("description"):
        return jsonify({"error": "Brakuje wymaganych danych (nazwa, obraz, opis)"}), 400

    new_plant = Plant(
        name=data["name"],
        image=data["image"],
        description=data["description"]
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify({"message": "Dodano roślinę!"}), 201

@app.route('/plants/<int:plant_id>', methods=['PUT'])
@login_required
def update_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({"error": "Roślina nie istnieje"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Brak danych"}), 400

    plant.name = data.get("name", plant.name)
    plant.image = data.get("image", plant.image)
    plant.description = data.get("description", plant.description)
    db.session.commit()
    return jsonify({"message": "Zaktualizowano roślinę!"}), 200

@app.route('/plants/<int:plant_id>', methods=['DELETE'])
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({"error": "Roślina nie istnieje"}), 404

    db.session.delete(plant)
    db.session.commit()
    return jsonify({"message": "Usunięto roślinę!"}), 200

if __name__ == '__main__':
    with app.app_context():  # Używamy kontekstu aplikacji
        db.create_all()  # Tworzy wszystkie tabele, jeśli nie istnieją
    app.run(debug=True)
