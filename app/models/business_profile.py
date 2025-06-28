from app import db


class BusinessProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    business_name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(80))
    location = db.Column(db.String(120))
    description = db.Column(db.String(300))
