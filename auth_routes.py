from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, mysql
from user_model import User

def register_auth_routes(app):

    # Enable session for login tracking
    app.secret_key = "supersecretkey"

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not (username and email and password):
            return jsonify({"error": "All fields required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400

        # 🔒 Hash the password
        hashed_pw = generate_password_hash(password)

        # 1️⃣ Add to Flask user site database
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        # 2️⃣ Also insert into app_user (Admin Panel DB)
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO app_user (username, email, password, role) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_pw, 'USER')
            )
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print("⚠️ Error syncing to admin DB:", e)

        return jsonify({"message": "User registered successfully"}), 201


    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        # ✅ Store username & id in session
        session['username'] = user.username
        session['user_id'] = user.id

        return jsonify({
            "message": "Login successful",
            "username": user.username,
            "user_id": user.id
        }), 200


    @app.route('/forgot-password', methods=['POST'])
    def forgot_password():
        data = request.get_json()
        email = data.get('email')
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check required fields
        if not (email and current_password and new_password and confirm_password):
            return jsonify({"error": "All fields are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Email not found"}), 404

        # Check current password
        if not check_password_hash(user.password_hash, current_password):
            return jsonify({"error": "Current password is incorrect"}), 401

        # Check new password match
        if new_password != confirm_password:
            return jsonify({"error": "New password and confirmation do not match"}), 400

        # Update password
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({"message": "Password updated successfully"}), 200


    # ✅ Updated route: return both username and user_id
    @app.route('/current-user', methods=['GET'])
    def get_current_user():
        username = session.get('username')
        user_id = session.get('user_id')
        if username and user_id:
            return jsonify({
                "username": username,
                "id": user_id
            }), 200
        return jsonify({"username": None}), 401
