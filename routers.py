# routers.py
from flask import render_template, request, jsonify
from handlers import handle_recipe_search
from data import mock_recipes

current_index = 0
chunk_size = 5

# Define your routes here
def setup_routes(app):
    
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            data = request.get_json()
            user_input = data.get("prompt", "").lower().strip()
            response = handle_recipe_search(user_input)
            return jsonify(response)
        return render_template("index.html")
    
    @app.route('/get-recipes', methods=['GET'])
    def get_recipes():
        global current_index
        
        # Get the next chunk of 5 recipes
        next_chunk = list(mock_recipes.items())[current_index:current_index + chunk_size]
        
        # Update the index for the next request
        current_index += chunk_size
        
        # If we've reached the end of the recipes list, reset the index (optional)
        if current_index >= len(mock_recipes):
            current_index = 0
        
        recipes_list = [{"name": recipe[0], "icon": "fas fa-lemon"} for recipe in next_chunk]
        
        return jsonify(recipes_list)
