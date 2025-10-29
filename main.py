import logging
from flask import Flask, render_template
from extensions import db
from routers import setup_routes

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__, template_folder='templetss', static_folder='frontend')

# MySQL config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Chetan%400903@localhost/recipedata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Setup API routes
setup_routes(app)

# Chatbot page
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Initialize DB tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error during DB init: {e}")

if __name__ == "__main__":
    print("Flask app running on http://127.0.0.1:5000")
    app.run(debug=True)
