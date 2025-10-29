from flask import jsonify, request
from models import Category, Recipe  # Import models
from extensions import db  # Import db from extensions.py

def setup_route(app):
    print("Setting up routes...")

    # Helper function to convert a Recipe object to a dictionary
    def recipe_to_dict(recipe):
        return {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps or "",
            "url": recipe.url or "",
            "category_id": recipe.category_id
        }

    # Create a new recipe
    @app.route('/recipes', methods=['POST'])
    def add_recipe():
        data = request.get_json()
        required_fields = ['name', 'description', 'ingredients']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

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
            return jsonify({"error": "An error occurred while creating the recipe.", "details": str(e)}), 500

    # Get a single recipe by ID
    @app.route('/recipes/<int:recipe_id>', methods=['GET'])
    def view_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404
        return jsonify(recipe_to_dict(recipe))

    # Get all recipes with optional filtering by category_id and name
    @app.route('/recipes', methods=['GET'])
    def list_recipes():
        category_id = request.args.get('category_id')
        name = request.args.get('name')

        query = Recipe.query

        if category_id:
            query = query.filter_by(category_id=category_id)
        if name:
            query = query.filter(Recipe.name.ilike(f"%{name}%"))  # Case-insensitive search

        recipes = query.all()

        if not recipes:
            return jsonify({"message": "No recipes found"}), 200

        return jsonify([recipe_to_dict(recipe) for recipe in recipes])

    # Update a recipe by ID
    @app.route('/recipes/<int:recipe_id>', methods=['PUT'])
    def modify_recipe(recipe_id):
        print(f"Received PUT request for recipe_id: {recipe_id}")

        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404

        data = request.get_json()
        try:
            # Update fields only if provided
            recipe.name = data.get('name', recipe.name)
            recipe.description = data.get('description', recipe.description)
            recipe.ingredients = data.get('ingredients', recipe.ingredients)
            recipe.steps = data.get('steps', recipe.steps)
            recipe.url = data.get('url', recipe.url)
            recipe.category_id = data.get('category_id', recipe.category_id)
            if 'index' in data:  # Ensure 'index' exists in your model if you're using this
                recipe.index = data['index']
                
            db.session.commit()
            return jsonify({"message": "Recipe updated successfully!", "recipe": recipe_to_dict(recipe)}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while updating the recipe.", "details": str(e)}), 500

    # Delete a recipe by ID
    @app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
    def remove_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404

        try:
            db.session.delete(recipe)
            db.session.commit()
            return jsonify({"message": "Recipe deleted successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while deleting the recipe.", "details": str(e)}), 500