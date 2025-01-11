# handlers.py
from rapidfuzz import process as rapid_process
from data import mock_recipes
import logging

logger = logging.getLogger(__name__)

# Function to handle the recipe search request
def handle_recipe_search(user_input):
    try:
        user_input = user_input.lower().strip()

        # Log the user input for debugging
        logger.info(f"Received user input: {user_input}")

        response = {}
        if user_input in mock_recipes:
            response = mock_recipes[user_input]
        else:
            # Fuzzy search for recipes containing keywords in the name
            matched_recipe = rapid_process.extractOne(user_input, mock_recipes.keys(), score_cutoff=70)
            if matched_recipe:
                recipe_name = matched_recipe[0]
                response = mock_recipes[recipe_name]
            else:
                response = {"error": "No matching recipe found."}
        
        return response
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {"error": "An error occurred while processing the request."}


























