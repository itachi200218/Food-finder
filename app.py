# from flask import Flask
# from extensions import db
# from dotenv import load_dotenv
# import os
# from router import setup_route  # Import setup_route from router.py
# from flask_cors import CORS  # Import CORS

# # Initialize the Flask app
# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# # Load environment variables from .env file
# load_dotenv()

# # Setup MySQL connection URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Chetan%400903@localhost/recipedata'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to avoid warnings

# # Initialize SQLAlchemy (using db from extensions.py)
# db.init_app(app)

# # Simple root route to check if the app is running
# @app.route('/')
# def home():
#     return "Welcome to the Recipe API!"

# # Setup routes from router.py
# setup_route(app)

# if __name__ == '__main__':
#     app.run(debug=True)