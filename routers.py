from flask import render_template, request, jsonify
from handlers import handle_recipe_search
from models import db, Recipe, Category  # Import the Recipe model to interact with MySQL
from sqlalchemy.orm import aliased

# Global variables for pagination
current_index = 0
chunk_size = 5

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

    # Route to get recipes with pagination and category filtering, avoiding duplicates
    @app.route('/get-recipes', methods=['GET'])
    def get_recipes():
        try:
            category = request.args.get('category')
            page = max(int(request.args.get('page', 1)), 1)  # Ensure page is at least 1
            recipes_per_page = chunk_size

            # Build query with distinct recipe names
            query = db.session.query(Recipe).join(Category, Recipe.category_id == Category.id).distinct(Recipe.name)

            if category:
                query = query.filter(Category.name.ilike(f"%{category}%"))

            # Pagination
            recipes = query.offset((page - 1) * recipes_per_page).limit(recipes_per_page).all()

            if recipes:
                recipe_data = [
                    {   'id': recipe.id,
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
                return jsonify([])  # No recipes found

        except Exception as e:
            print(f"Error fetching recipes: {e}")
            return jsonify({'error': 'Error fetching recipes'}), 500

    # Route to get recipe details by ID
    @app.route('/get-recipe-detail', methods=['GET'])
    def get_recipe_detail():
        try:
            recipe_id = request.args.get('id')
            if recipe_id:
                # Fetch the recipe by ID
                recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
                if recipe:
                    recipe_data = {
                        'name': recipe.name,
                        'description': recipe.description,
                        'ingredients': recipe.ingredients.split(', '),
                        'steps': recipe.steps.split('. '),
                        'url': recipe.url
                    }
                    return jsonify(recipe_data)
                else:
                    return jsonify({'error': 'Recipe not found'}), 404
            else:
                return jsonify({'error': 'No recipe ID provided'}), 400
        except Exception as e:
            print(f"Error fetching recipe details: {e}")
            return jsonify({'error': 'Error fetching recipe details'}), 500