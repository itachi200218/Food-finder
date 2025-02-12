from flask import render_template, request, jsonify
from handlers import handle_recipe_search
from models import db, Recipe, Category
from sqlalchemy import or_
import logging

# Set up logging for error handling
logging.basicConfig(level=logging.ERROR)

CHUNK_SIZE = 5  # Constant for recipes per page

def setup_routes(app):

    @app.route("/", methods=["GET", "POST"])
    def index():
        """Render the main page or handle search requests."""
        if request.method == "POST":
            try:
                data = request.get_json()
                user_input = data.get("prompt", "recipeName").lower().strip()
                response = handle_recipe_search(user_input)
                return jsonify(response)
            except Exception as e:
                logging.error(f"Error in index route: {e}")
                return jsonify({'error': 'An error occurred while processing your request'}), 500
        return render_template("index.html")

    @app.route('/get-recipes', methods=['GET'])
    def get_recipes():
        """Fetch a list of recipes with optional filtering by category or keyword."""
        try:
            category = request.args.get('category')  # Example: 'chicken'
            page = max(int(request.args.get('page', 1)), 1)
            
            # Base query to fetch recipes with optional keyword filtering
            query = db.session.query(Recipe).join(Category, Recipe.category_id == Category.id).distinct(Recipe.name)

            if category:
                query = query.filter(
                    or_(
                        Recipe.name.ilike(f"%{category}%"),
                        Category.name.ilike(f"%{category}%")
                    )
                )

            recipes = query.offset((page - 1) * CHUNK_SIZE).limit(CHUNK_SIZE).all()

            recipe_data = [
                {
                    'id': recipe.id,
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

        except Exception as e:
            logging.error(f"Error fetching recipes: {e}")
            return jsonify({'error': 'Error fetching recipes'}), 500

    @app.route('/get-recipe-detail', methods=['GET'])
    def get_recipe_detail():
        """Fetch detailed information about a specific recipe by ID or name."""
        try:
            recipe_id = request.args.get('id')
            if not recipe_id:
                return jsonify({'error': 'No recipe ID provided'}), 400

            # Check if the provided ID is a digit (search by ID) or a string (search by name)
            recipe = None
            if recipe_id.isdigit():
                recipe = db.session.query(Recipe).filter_by(id=int(recipe_id)).first()
            else:
                recipe = db.session.query(Recipe).filter(Recipe.name.ilike(f"%{recipe_id}%")).first()

            if recipe:
                recipe_data = {
                    'id': recipe.id,
                    'name': recipe.name,
                    'description': recipe.description,
                    'ingredients': [i.strip() for i in recipe.ingredients.split(',') if i.strip()],
                    'steps': [s.strip().capitalize() for s in recipe.steps.split('.') if s.strip()],
                    'url': recipe.url
                }
                return jsonify(recipe_data)
            else:
                return jsonify({'error': 'Recipe not found'}), 404

        except Exception as e:
            logging.error(f"Error fetching recipe details: {e}")
            return jsonify({'error': 'Error fetching recipe details'}), 500

    @app.route('/get-suggestions', methods=['GET'])
    def get_suggestions():
        """Fetch suggestions for recipe names based on user input."""
        try:
            query = request.args.get('query', '').strip()
            if not query:
                return jsonify([])

            suggestions = db.session.query(Recipe.name).filter(Recipe.name.ilike(f"%{query}%")).limit(10).all()
            suggestion_list = [s[0] for s in suggestions]
            return jsonify(suggestion_list)

        except Exception as e:
            logging.error(f"Error fetching suggestions: {e}")
            return jsonify({'error': 'Error fetching suggestions'}), 500
