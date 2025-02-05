from flask import render_template, request, jsonify
from handlers import handle_recipe_search
from models import db, Recipe, Category  # Import the Recipe model to interact with MySQL
from sqlalchemy.orm import aliased

# Global variables for pagination
current_index = 0
chunk_size = 5

# Define your routes here
def setup_routes(app):

    # Index route to render the home page and handle POST requests
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            data = request.get_json()
            user_input = data.get("prompt", "recipeName").lower().strip()
            response = handle_recipe_search(user_input)
            return jsonify(response)
        return render_template("index.html")

    # Route to get recipes from the database with category filtering and pagination
    @app.route('/get-recipes', methods=['GET'])
    def get_recipes():
        try:
            # Get parameters from the request
            category = request.args.get('category')
            page = int(request.args.get('page', 1))  # Default to page 1 if not provided

            # Limit to 5 recipes per page
            recipes_per_page = 5

            # Build query based on category
            query = db.session.query(Recipe).join(Category, Recipe.category_id == Category.id)

            if category:
                query = query.filter(Category.name.ilike(f"%{category}%"))

            # Pagination logic
            recipes = query.offset((page - 1) * recipes_per_page).limit(recipes_per_page).all()

            if recipes:
                # Convert recipes to a list of dictionaries
                recipe_data = [
                    {
                        'name': recipe.name,
                        'description': recipe.description,
                        'ingredients': recipe.ingredients,
                        'steps': recipe.steps,
                        'url': recipe.url,
                        'category': recipe.category.name
                    }
                    for recipe in recipes
                ]

                return jsonify(recipe_data)
            else:
                return jsonify([])  # No more recipes

        except Exception as e:
            print(f"Error fetching recipes: {e}")
            return jsonify({'error': 'Error fetching recipes'}), 500
