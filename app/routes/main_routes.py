from flask import Blueprint, jsonify, render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.transaction import Transaction
from sqlalchemy import func

main = Blueprint("main", __name__)


@main.route("/api/dashboard-data", methods=["GET"])
@jwt_required()
def dashboard_data():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404

    income = (
        db.session.query(func.sum(Transaction.amount))
        .filter_by(user_id=user_id, type="income")
        .scalar()
    ) or 0

    expense = (
        db.session.query(func.sum(Transaction.amount))
        .filter_by(user_id=user_id, type="expense")
        .scalar()
    ) or 0

    return jsonify({"email": user.email, "income": income, "expense": expense}), 200


@main.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@main.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@main.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@main.route("/home", methods=["GET"])
def home():
    return render_template("index.html")
