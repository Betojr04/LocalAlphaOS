from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import NoAuthorizationError
import datetime

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists."}), 409

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id),  # ✅ convert to string
        expires_delta=datetime.timedelta(days=1),
    )

    return (
        jsonify(
            {"access_token": access_token, "message": f"Welcome back, {user.email}!"}
        ),
        200,
    )


# getting your user info:
@auth.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"id": user.id, "email": user.email}), 200


@auth.route("/update-password", methods=["PUT"])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not user or not user.check_password(current_password):
        return jsonify({"error": "Current password incorrect"}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200


@auth.route("/delete-account", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Account deleted successfully"}), 200


@auth.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()
    if not user:
        # Always respond the same way to prevent email discovery
        return (
            jsonify({"message": "If your email is registered, check your inbox."}),
            200,
        )

    reset_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=15),  # short-lived token
        additional_claims={"reset": True},
    )

    return (
        jsonify(
            {
                "message": "If your email is registered, check your inbox.",
                "reset_token": reset_token,  # For testing / frontend display
            }
        ),
        200,
    )


@auth.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("reset_token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    try:
        # Manually verify token
        verify_jwt_in_request(locations=["json"], token=token)
        user_id = get_jwt_identity()
    except NoAuthorizationError:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200
