from app import db
from datetime import datetime


class SponsorshipEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    impressions = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
