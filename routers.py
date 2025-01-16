from flask import render_template, request, jsonify
from handlers import handle_recipe_search
from models import Recipe  # Import the Recipe model to interact with MySQL
from sqlalchemy.orm import aliased

current_index = 0
chunk_size = 5

# Define your routes here
def setup_routes(app):
    
    # Index route to render the home page and handle POST requests
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            data = request.get_json()
            user_input = data.get("prompt", "").lower().strip()
            response = handle_recipe_search(user_input)
            return jsonify(response)
        return render_template("index.html")
    
    # Route to get recipes in chunks from the database
    @app.route('/get-recipes', methods=['GET'])
    def get_recipes():
        global current_index
        
        # Query the next chunk of 5 recipes from the database
        recipes_chunk = Recipe.query.offset(current_index).limit(chunk_size).all()
        
        # Prepare the list of recipes to return
        recipes_list = [{"name": recipe.name, "icon": "fas fa-lemon"} for recipe in recipes_chunk]
        
        # Update the index for the next request
        current_index += chunk_size
        
        # If we've reached the end of the recipes list, reset the index (optional)
        if current_index >= Recipe.query.count():
            current_index = 0
        
        return jsonify(recipes_list)
