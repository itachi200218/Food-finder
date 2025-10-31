import logging
from flask import Flask, render_template
from extensions import db, mysql
from routers import setup_routes
from auth_routes import register_auth_routes   # ✅ Add this import
from like_routes import like_bp                # ✅ Added import for Like routes

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__, template_folder='templetss', static_folder='frontend')

# 🛠️ MySQL + SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Chetan%400903@localhost/recipedata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Setup API routes
setup_routes(app)

# Setup Auth routes
register_auth_routes(app)   # ✅ Added here

# Setup Like routes
app.register_blueprint(like_bp)  # ✅ Added this line

# Chatbot page
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# User Authentication Page
@app.route('/auth')
def auth_page():
    return render_template('auth.html')
@app.route('/liked')
def liked_page():
    return render_template('liked.html')

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

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
