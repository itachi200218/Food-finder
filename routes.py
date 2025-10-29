from flask import jsonify, request, render_template
from sqlalchemy import or_
import logging

from models import Recipe, Category
from extensions import db
from handlers import handle_recipe_search

CHUNK_SIZE = 5  

def setup_routes(app):
  
    def recipe_to_dict(recipe):
        return {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps or "",
            "url": recipe.url or "",
            "category_id": recipe.category_id,
            "category_name": recipe.category.name if recipe.category else None
        }

    @app.route("/", methods=["GET"])
    def index():
        """Render the main page."""
        return render_template("index.html")

    @app.route("/api/search", methods=["POST"])
    def search_recipes_handler():
        """Handle search requests from the frontend."""
        try:
            data = request.get_json()
            user_input = data.get("prompt", "").lower().strip()
            category = data.get("category", None)
            response = handle_recipe_search(user_input, category)
            return jsonify(response)
        except Exception as e:
            logging.error(f"Error in search route: {e}")
            return jsonify({'error': 'An error occurred while processing your request'}), 500

    # --- Full CRUD API for Recipes ---

    @app.route('/api/recipes', methods=['POST'])
    def add_recipe():
        data = request.get_json()
        required_fields = ['name', 'description', 'ingredients']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields: name, description, ingredients"}), 400

        try:
            recipe = Recipe(
                name=data['name'],
                description=data['description'],
                ingredients=data['ingredients'],
                steps=data.get('steps', ''),
                url=data.get('url', ''),
                category_id=data.get('category_id')
            )
            db.session.add(recipe)
            db.session.commit()
            return jsonify({"message": "Recipe created successfully!", "recipe": recipe_to_dict(recipe)}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating recipe: {e}")
            return jsonify({"error": "An error occurred while creating the recipe."}), 500

    @app.route('/api/recipes', methods=['GET'])
    def list_recipes():
        category_id = request.args.get('category_id')
        name = request.args.get('name')
        page = max(int(request.args.get('page', 1)), 1)

        query = Recipe.query

        if category_id:
            query = query.filter_by(category_id=category_id)
        if name:
            query = query.filter(Recipe.name.ilike(f"%{name}%"))

        paginated_recipes = query.paginate(page=page, per_page=CHUNK_SIZE, error_out=False)
        recipes = paginated_recipes.items

        return jsonify({
            "recipes": [recipe_to_dict(recipe) for recipe in recipes],
            "total": paginated_recipes.total,
            "pages": paginated_recipes.pages,
            "current_page": page
        })

    @app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
    def get_recipe_detail(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        return jsonify(recipe_to_dict(recipe))

    @app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
    def modify_recipe(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        try:
            recipe.name = data.get('name', recipe.name)
            recipe.description = data.get('description', recipe.description)
            recipe.ingredients = data.get('ingredients', recipe.ingredients)
            recipe.steps = data.get('steps', recipe.steps)
            recipe.url = data.get('url', recipe.url)
            recipe.category_id = data.get('category_id', recipe.category_id)
            
            db.session.commit()
            return jsonify({"message": "Recipe updated successfully!", "recipe": recipe_to_dict(recipe)})
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating recipe {recipe_id}: {e}")
            return jsonify({"error": "An error occurred while updating the recipe."}), 500

    @app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
    def remove_recipe(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        try:
            db.session.delete(recipe)
            db.session.commit()
            return jsonify({"message": "Recipe deleted successfully!"})
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting recipe {recipe_id}: {e}")
            return jsonify({"error": "An error occurred while deleting the recipe."}), 500

    @app.route('/api/suggestions', methods=['GET'])
    def get_suggestions():
        """Fetch suggestions for recipe names based on user input."""
        query_param = request.args.get('query', '').strip()
        if not query_param:
            return jsonify([])

        try:
            suggestions = db.session.query(Recipe.name).filter(Recipe.name.ilike(f"%{query_param}%")).limit(10).all()
            suggestion_list = [s[0] for s in suggestions]
            return jsonify(suggestion_list)
        except Exception as e:
            logging.error(f"Error fetching suggestions: {e}")
            return jsonify({'error': 'Error fetching suggestions'}), 500
