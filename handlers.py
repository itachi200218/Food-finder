from rapidfuzz import process as rapid_process
from models import Recipe  # Import Recipe model
from extensions import db  # Import db from extensions.py
import logging

# Set up the logger
logger = logging.getLogger(__name__)

def handle_recipe_search(user_input):
    try:
        # Clean the user input
        user_input = user_input.lower().strip()

        # Log the user input for debugging
        logger.info(f"Received user input: {user_input}")

        response = {}

        # Search for exact match in the database first
        matched_recipe = db.session.query(Recipe).filter(Recipe.name.ilike(f"%{user_input}%")).first()

        if matched_recipe:
            response = {
                "name": matched_recipe.name,
                "ingredients": matched_recipe.ingredients.split(", "),
                "description": matched_recipe.description,
                "steps": matched_recipe.steps.split(" | "),
                "url": matched_recipe.url
            }
            logger.info(f"Exact match found: {matched_recipe.name}")
        else:
            recipes = db.session.query(Recipe).all()
            recipe_names = [recipe.name for recipe in recipes]
            logger.info(f"Recipe names: {recipe_names}")  # Log the recipe names

            matched_recipe = rapid_process.extractOne(user_input, recipe_names, score_cutoff=70)

            if matched_recipe:
                recipe_name = matched_recipe[0]
                recipe = db.session.query(Recipe).filter_by(name=recipe_name).first()
                response = {
                    "name": recipe.name,
                    "ingredients": recipe.ingredients.split(", "),
                    "description": recipe.description,
                    "steps": recipe.steps.split(" | "),
                    "url": recipe.url
                }
                logger.info(f"Fuzzy match found: {recipe_name}")
            else:
                response = {"error": "No matching recipe found."}
                logger.info("No matching recipe found for user input.")

        logger.info(f"Response: {response}")
        return response
    
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {"error": "An error occurred while processing the request."}


















































































































































































