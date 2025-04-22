from flask import Flask, jsonify, request, session
from flask_cors import CORS
from database import db, Plant, Weather
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

db.init_app(app)  # Inicjalizacja bazy danych

# Użytkownicy testowi
users = {
    "admin": "password123",
    "user": "testpass"
}

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
            "id": plant.id,
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

# Endpointy pogody
@app.route('/weather', methods=['GET'])
def get_weather():
    weather = Weather.query.order_by(Weather.id.desc()).first()
    if weather:
        return jsonify(weather.to_dict())
    else:
        # Domyślne wartości, jeśli brak danych
        return jsonify({
            "sky_condition": "clear",
            "temperature": 20,
            "humidity": 50,
            "precipitation": False
        })

@app.route('/weather', methods=['POST'])
def set_weather():
    data = request.json
    # Walidacja: opad nie może wystąpić przy bezchmurnym niebie
    if data.get('precipitation') and data.get('sky_condition') == 'clear':
        return jsonify({"error": "Opad atmosferyczny nie może wystąpić przy bezchmurnym niebie!"}), 400

    new_weather = Weather(
        sky_condition=data.get('sky_condition', 'clear'),
        temperature=data.get('temperature', 20),
        humidity=data.get('humidity', 50),
        precipitation=data.get('precipitation', False)
    )
    db.session.add(new_weather)
    db.session.commit()
    return jsonify({"message": "Pogoda została zaktualizowana!"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
