from app import db
from datetime import datetime


class ClientCheckin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    client_name = db.Column(db.String(100))
    checkin_time = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(200))
