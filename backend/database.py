from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Plant {self.name}>"

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sky_condition = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    precipitation = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "sky_condition": self.sky_condition,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "precipitation": self.precipitation
        }
