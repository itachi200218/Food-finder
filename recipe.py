from flask import Flask, render_template, request, jsonify
from handlers import handle_recipe_search, handle_advanced_recipe_search  # Import your handler functions
from models import db, Recipe, Category
from sqlalchemy import or_
import logging

@app.route('/get-recipe-detail', methods=['GET'])
def get_recipe_detail():
    """Fetch detailed information about a specific recipe by ID or name."""
    try:
        recipe_id = request.args.get('id', '').strip()
        if not recipe_id:
            return jsonify({'error': 'No recipe ID provided'}), 400

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

            # Render the recipe detail page using SSR
            return render_template('recipe_detail.html', recipe=recipe_data)

        else:
            return jsonify({'error': 'Recipe not found'}), 404

    except Exception as e:
        logging.error(f"Error fetching recipe details: {e}")
        return jsonify({'error': 'Error fetching recipe details'}), 500
