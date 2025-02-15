import json
from rapidfuzz import process as rapid_process
from sqlalchemy import func, and_, or_
from models import Recipe, Category
from extensions import db
from redis import Redis
import logging

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Redis client setup
redis_client = Redis(host='localhost', port=6379, decode_responses=True)

def handle_recipe_search(user_input, category_name=None):
    """Handles a basic recipe search with caching, exact match, and fuzzy matching."""
    try:
        user_input = user_input.lower().strip()
        keywords = [kw.strip() for kw in user_input.split() if kw]
        logger.info(f"Received user input: '{user_input}', Keywords: {keywords}, Category: {category_name}")

        cache_key = f"recipe_search:{user_input}:{category_name}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            logger.info("Returning cached result.")
            return json.loads(cached_result)

        query = db.session.query(Recipe).join(Category, Recipe.category_id == Category.id)
        if category_name:
            query = query.filter(Category.name.ilike(f"%{category_name}%"))

        # Exact Match
        matched_recipe = query.filter(
            and_(*[
                or_(
                    Recipe.name.ilike(f"%{kw}%"),
                    Recipe.ingredients.ilike(f"%{kw}%"),
                    Recipe.steps.ilike(f"%{kw}%")
                ) for kw in keywords
            ])
        ).first()

        if matched_recipe:
            response = format_recipe_response(matched_recipe)
            logger.info(f"Exact match found: {matched_recipe.name}")
            redis_client.set(cache_key, json.dumps(response), ex=3600)  # Cache for 1 hour
            return response

        # Fuzzy Matching
        recipes = query.limit(100).all()  # Limit to 100 for performance
        recipe_names = [r.name for r in recipes]

        fuzzy_matches = rapid_process.extract(user_input, recipe_names, limit=5, score_cutoff=70)
        suggestions = [
            format_recipe_response(next(r for r in recipes if r.name == match[0]))
            for match in fuzzy_matches
        ]

        response = {"suggestions": suggestions or [{"error": "No matching recipe found."}]}
        redis_client.set(cache_key, json.dumps(response), ex=3600)  # Cache for 1 hour
        return response

    except Exception as e:
        logger.error(f"Error processing recipe search: {e}")
        return {"error": "An unexpected error occurred."}

def handle_advanced_recipe_search(user_input, category_name=None, limit=5):
    """Handles an advanced recipe search using full-text search with caching and fuzzy matching fallback."""
    try:
        user_input = user_input.lower().strip()
        cache_key = f"advanced_search:{user_input}:{category_name}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            logger.info("Returning cached result.")
            return json.loads(cached_result)

        query = db.session.query(Recipe).join(Category, Recipe.category_id == Category.id)
        if category_name:
            query = query.filter(Category.name.ilike(f"%{category_name}%"))

        # Full-text search for exact matches (MySQL FULLTEXT)
        matched_recipes = query.filter(
            func.match(Recipe.name, Recipe.ingredients, Recipe.steps).against(user_input)
        ).limit(limit).all()

        if matched_recipes:
            response = {"recipes": [format_recipe_response(recipe) for recipe in matched_recipes]}
            redis_client.set(cache_key, json.dumps(response), ex=3600)  # Cache for 1 hour
            return response

        # Fuzzy Matching as a fallback
        recipes = query.limit(100).all()
        recipe_names = [r.name for r in recipes]

        fuzzy_matches = rapid_process.extract(user_input, recipe_names, limit=5, score_cutoff=70)
        suggestions = [
            format_recipe_response(next(r for r in recipes if r.name == match[0]))
            for match in fuzzy_matches
        ]

        response = {"suggestions": suggestions or [{"error": "No matching recipe found."}]}
        redis_client.set(cache_key, json.dumps(response), ex=3600)  # Cache for 1 hour
        return response

    except Exception as e:
        logger.error(f"Error processing advanced recipe search: {e}")
        return {"error": "An unexpected error occurred."}

def format_recipe_response(recipe):
    """Helper function to format a recipe response into a dictionary."""
    return {
        "name": recipe.name,
        "ingredients": recipe.ingredients.split(", "),
        "description": recipe.description,
        "steps": recipe.steps.split(" | "),
        "url": recipe.url,
        "category": recipe.category.name
    }






























