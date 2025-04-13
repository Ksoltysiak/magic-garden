from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

plants = []

@app.route('/plants', methods=['GET'])
def get_plants():
    return jsonify(plants)

@app.route('/plants', methods=['POST'])
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
