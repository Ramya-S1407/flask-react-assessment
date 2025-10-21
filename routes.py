# routes.py
from flask import Blueprint, request, jsonify, current_app
from db import db
from models import Comment

bp = Blueprint("api", __name__)

# Get comments for a task
@bp.route("/tasks/<int:task_id>/comments", methods=["GET"])
def get_comments(task_id):
    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify([c.to_dict() for c in comments]), 200

# Add a comment for a task
@bp.route("/tasks/<int:task_id>/comments", methods=["POST"])
def add_comment(task_id):
    data = request.get_json() or {}
    text = data.get("text")
    author = data.get("author")
    if not text:
        return jsonify({"error": "Missing 'text' in body"}), 400

    comment = Comment(task_id=task_id, text=text, author=author)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

# Update a comment by id
@bp.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    data = request.get_json() or {}
    text = data.get("text")
    author = data.get("author")

    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if text is not None:
        comment.text = text
    if author is not None:
        comment.author = author

    db.session.commit()
    return jsonify(comment.to_dict()), 200

# Delete a comment by id
@bp.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"}), 200
