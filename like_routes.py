from flask import Blueprint, request, jsonify, session
from extensions import db
from user_model import User, Like

like_bp = Blueprint("like_bp", __name__)

# ❤️ Like a recipe
@like_bp.route("/like", methods=["POST"])
def like_recipe():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()
    recipe_name = data.get("recipe_name")
    user_id = session["user_id"]

    if not recipe_name:
        return jsonify({"error": "Recipe name required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    existing_like = Like.query.filter_by(user_id=user_id, recipe_name=recipe_name).first()
    if existing_like:
        return jsonify({"message": "Recipe already liked"}), 200

    like = Like(recipe_name=recipe_name, user_id=user_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({"message": f"Recipe '{recipe_name}' liked successfully!"}), 201


# 💔 Unlike a recipe
@like_bp.route("/unlike", methods=["POST"])
def unlike_recipe():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()
    recipe_name = data.get("recipe_name")
    user_id = session["user_id"]

    if not recipe_name:
        return jsonify({"error": "Recipe name required"}), 400

    like = Like.query.filter_by(user_id=user_id, recipe_name=recipe_name).first()
    if not like:
        return jsonify({"message": "Recipe not found in liked list"}), 404

    db.session.delete(like)
    db.session.commit()

    return jsonify({"message": f"Recipe '{recipe_name}' unliked successfully!"}), 200


# ⭐ Get all liked recipes (uses session)
@like_bp.route("/likes", methods=["GET"])
def get_likes():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    user_id = session["user_id"]
    user = User.query.get(user_id)

    liked_recipes = [like.recipe_name for like in user.likes]
    return jsonify(liked_recipes), 200
