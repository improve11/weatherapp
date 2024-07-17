from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
