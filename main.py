import os
import logging
from flask import Flask
from extensions import db  # Import db from extensions.py
from routers import setup_routes

# Setup Flask app
app = Flask(__name__, template_folder='templetss', static_folder='frontend')

# Setup MySQL connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Chetan%400903@localhost/recipedata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to avoid warnings

# Initialize SQLAlchemy (using db from extensions.py)
db.init_app(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup routes
setup_routes(app)

# Initialize database manually using app context
with app.app_context():
    try:
        # Make sure the database tables are created
        db.create_all()
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")

if __name__ == "__main__":
    print("Flask app initialized")
    app.run(debug=True)
