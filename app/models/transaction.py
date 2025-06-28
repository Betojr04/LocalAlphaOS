from app import db
from datetime import datetime


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Foreign key if needed later
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    note = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
