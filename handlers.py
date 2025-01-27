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
        keywords = [kw.strip() for kw in user_input.split(" ") if kw]  # Split into keywords

        # Log the received input and keywords
        logger.info(f"Received user input: '{user_input}', Keywords: {keywords}")

        # Initialize the response
        response = {}

        # Exact Match: Check if all keywords are in name, ingredients, or steps
        matched_recipe = db.session.query(Recipe).filter(
            db.and_(
                *[db.or_(
                    Recipe.name.ilike(f"%{kw}%"),
                    Recipe.ingredients.ilike(f"%{kw}%"),
                    Recipe.steps.ilike(f"%{kw}%")  # Include steps in the exact match
                ) for kw in keywords]
            )
        ).first()

        if matched_recipe:
            # Return recipe details for an exact match
            response = {
                "name": matched_recipe.name,
                "ingredients": matched_recipe.ingredients.split(", "),
                "description": matched_recipe.description,
                "steps": matched_recipe.steps.split(" | "),
                "url": matched_recipe.url,
                "suggestions": []
            }
            logger.info(f"Exact match found: {matched_recipe.name}")
            return response

        # Fuzzy matching if no exact match is found
        recipes = db.session.query(Recipe).all()
        recipe_data = [{"name": r.name, "ingredients": r.ingredients, "steps": r.steps} for r in recipes]

        # Prepare lists for fuzzy matching (including steps)
        recipe_names = [r["name"] for r in recipe_data]
        recipe_ingredients = [r["ingredients"] for r in recipe_data]
        recipe_steps = [r["steps"] for r in recipe_data]  # Add steps to fuzzy matching

        logger.debug(f"Available recipe names: {recipe_names}")
        logger.debug(f"Available recipe ingredients: {recipe_ingredients}")
        logger.debug(f"Available recipe steps: {recipe_steps}")

        # Fuzzy matching for each keyword (include steps now)
        fuzzy_matches = []
        for kw in keywords:
            matched_name = rapid_process.extract(kw, recipe_names, limit=3, score_cutoff=70)
            matched_ingredient = rapid_process.extract(kw, recipe_ingredients, limit=3, score_cutoff=70)
            matched_steps = rapid_process.extract(kw, recipe_steps, limit=3, score_cutoff=70)  # Fuzzy matching for steps
            for match in matched_name:
                if not any(m["value"] == match[0] for m in fuzzy_matches):  # Avoid duplicates
                    fuzzy_matches.append({"type": "name", "value": match[0], "score": match[1]})
            for match in matched_ingredient:
                if not any(m["value"] == match[0] for m in fuzzy_matches):  # Avoid duplicates
                    fuzzy_matches.append({"type": "ingredient", "value": match[0], "score": match[1]})
            for match in matched_steps:
                if not any(m["value"] == match[0] for m in fuzzy_matches):  # Avoid duplicates
                    fuzzy_matches.append({"type": "steps", "value": match[0], "score": match[1]})

        # Aggregate matches by recipe, considering match type weights (name, ingredients, steps)
        match_weights = {"name": 3, "ingredient": 2, "steps": 1}
        match_scores = {}
        for match in fuzzy_matches:
            if match["value"] in match_scores:
                match_scores[match["value"]] += match["score"] * match_weights.get(match["type"], 1)
            else:
                match_scores[match["value"]] = match["score"] * match_weights.get(match["type"], 1)

        # Select up to 3 best matches
        best_matches = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)[:3]

        # Fetch the recipes based on the best matches
        matched_values = [match[0] for match in best_matches]
        suggestions = db.session.query(Recipe).filter(
            Recipe.name.in_(matched_values) |
            Recipe.ingredients.in_(matched_values) |
            Recipe.steps.in_(matched_values)
        ).all()

        # Prepare the response
        suggestions_list = []
        for matched_recipe in suggestions:
            suggestions_list.append({
                "name": matched_recipe.name,
                "ingredients": matched_recipe.ingredients.split(", "),
                "description": matched_recipe.description,
                "url": matched_recipe.url,
                "steps": matched_recipe.steps.split(" | "),  # Split the steps for easier display
                "matched_keywords": [kw for kw in keywords if kw in matched_recipe.name.lower() or kw in matched_recipe.ingredients.lower() or kw in matched_recipe.steps.lower()]
            })

        if suggestions_list:
            response = {"suggestions": suggestions_list}
            logger.info(f"Suggestions found: {[s['name'] for s in suggestions_list]}")
        else:
            response = {"error": "No matching recipe found.", "suggestions": []}
            logger.info("No fuzzy match found for user input.")

        logger.info(f"Response: {response}")
        return response

    except Exception as e:
        # Log any errors
        logger.error(f"Error processing recipe search for input '{user_input}': {e}")
        return {"error": "An unexpected error occurred while processing the request.", "suggestions": []}





























































































