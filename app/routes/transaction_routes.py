# app/routes/transaction_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Transaction
from datetime import datetime

transactions = Blueprint("transactions", __name__)


# ADDING A TRANSACTION
@transactions.route("/transactions", methods=["POST"])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    txn = Transaction(
        user_id=user_id,
        type=data["type"],
        amount=data["amount"],
        category=data["category"],
        note=data.get("note", ""),
    )

    db.session.add(txn)
    db.session.commit()
    return jsonify({"message": "Transaction created"}), 201


# GETTING ALL TRANSACTIONS
@transactions.route("/transactions", methods=["GET"])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = (
        Transaction.query.filter_by(user_id=user_id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    result = [
        {
            "id": t.id,
            "type": t.type,
            "amount": t.amount,
            "category": t.category,
            "note": t.note,
            "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M"),
        }
        for t in transactions
    ]

    return jsonify(result), 200


# DELETING SPECIFIC TRANSACTION
@transactions.route("/transactions/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
def delete_transaction(transaction_id):
    user_id = get_jwt_identity()

    txn = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not txn:
        return jsonify({"error": "Transaction not found"}), 404

    db.session.delete(txn)
    db.session.commit()

    return jsonify({"message": "Transaction deleted"}), 200


# UPDATING A SPECIFIC TRANSACTION
@transactions.route("/transactions/<int:transaction_id>", methods=["PUT"])
@jwt_required()
def update_transaction(transaction_id):
    user_id = get_jwt_identity()
    txn = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()

    if not txn:
        return jsonify({"error": "Transaction not found"}), 404

    data = request.get_json()

    txn.type = data.get("type", txn.type)
    txn.amount = data.get("amount", txn.amount)
    txn.category = data.get("category", txn.category)
    txn.note = data.get("note", txn.note)

    if "timestamp" in data:
        try:
            txn.timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Invalid timestamp format"}), 400

    db.session.commit()

    return jsonify({"message": "Transaction updated"}), 200


# GET THE EXPENSES TRANSACTIONS
@transactions.route("/expenses", methods=["GET"])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expenses = (
        Transaction.query.filter_by(user_id=user_id, type="expense")
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    result = [
        {
            "id": e.id,
            "amount": e.amount,
            "category": e.category,
            "note": e.note,
            "timestamp": e.timestamp.strftime("%Y-%m-%d %H:%M"),
        }
        for e in expenses
    ]

    return jsonify(result), 200


# GET THE INCOME TRANSACTIONS
@transactions.route("/income", methods=["GET"])
@jwt_required()
def get_income():
    user_id = get_jwt_identity()
    income = (
        Transaction.query.filter_by(user_id=user_id, type="income")
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    result = [
        {
            "id": inc.id,
            "amount": inc.amount,
            "category": inc.category,
            "note": inc.note,
            "timestamp": inc.timestamp.strftime("%Y-%m-%d %H:%M"),
        }
        for inc in income
    ]

    return jsonify(result), 200
