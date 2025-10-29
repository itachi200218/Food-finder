import json
import logging
import os
import requests
from dotenv import load_dotenv
from rapidfuzz import process as rapid_process
from sqlalchemy import func, and_, or_
from models import Recipe, Category
from extensions import db
from redis import Redis

# ------------------- SETUP -------------------
load_dotenv()  # Load variables from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY not found in .env")

GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
)

# Redis setup
redis_client = Redis(host='localhost', port=6379, decode_responses=True)

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ------------------- MAIN SEARCH -------------------
def handle_recipe_search(user_input, category_name=None):
    """
    Handles intelligent recipe search with DB, fuzzy match, and Gemini fallback.
    """
    try:
        user_input = user_input.lower().strip()
        keywords = [kw.strip() for kw in user_input.split() if kw]
        logger.info(f"Searching for: '{user_input}', Category: {category_name}")

        cache_key = f"recipe_search:{user_input}:{category_name}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            logger.info("✅ Returning cached result.")
            return json.loads(cached_result)

        # Base query
        query = db.session.query(Recipe).outerjoin(Category)
        if category_name:
            query = query.filter(Category.name.ilike(f"%{category_name}%"))

        # ---- Exact or partial match ----
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
            redis_client.set(cache_key, json.dumps(response), ex=3600)
            return response

        # ---- Fuzzy match ----
        recipes = query.limit(100).all()
        recipe_names = [r.name for r in recipes]
        fuzzy_matches = rapid_process.extract(user_input, recipe_names, limit=5, score_cutoff=70)

        if fuzzy_matches:
            suggestions = [
                format_recipe_response(next(r for r in recipes if r.name == match[0]))
                for match in fuzzy_matches
            ]
            response = {"suggestions": suggestions}
            redis_client.set(cache_key, json.dumps(response), ex=3600)
            return response

        # ---- AI fallback ----
        logger.info("🤖 No DB matches found. Using Gemini AI...")
        ai_recipe = generate_ai_recipe(user_input)
        redis_client.set(cache_key, json.dumps(ai_recipe), ex=3600)
        return ai_recipe

    except Exception as e:
        logger.error(f"❌ Error in recipe search: {e}")
        return {"error": "An unexpected error occurred."}


# ------------------- GEMINI AI FALLBACK -------------------
def generate_ai_recipe(query):
    """
    Uses Gemini AI to generate a structured recipe when no database result found.
    """
    try:
        payload = {
            "contents": [{
                "parts": [{
                    "text": (
                        f"Generate a structured JSON recipe for '{query}'. "
                        f"Include:\n"
                        f"- 'name': Recipe name\n"
                        f"- 'description': Short description\n"
                        f"- 'ingredients': list of ingredients\n"
                        f"- 'steps': list of cooking steps\n"
                        f"- 'prep_time': preparation time\n"
                        f"Respond ONLY in JSON format."
                    )
                }]
            }]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        text = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        # Attempt to parse JSON from AI output
        try:
            recipe_data = json.loads(text)
        except json.JSONDecodeError:
            # Fallback: extract JSON substring if text has explanation
            json_part = extract_json_from_text(text)
            recipe_data = json.loads(json_part) if json_part else {"raw_text": text}

        logger.info("✅ Gemini AI recipe generated successfully.")
        return {"ai_generated": True, "recipe": recipe_data}

    except Exception as e:
        logger.error(f"❌ Gemini API error: {e}")
        return {"error": "Failed to generate AI recipe."}


# ------------------- UTILITIES -------------------
def extract_json_from_text(text):
    """Extracts JSON content safely if Gemini adds text before/after it."""
    import re
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def format_recipe_response(recipe):
    """Formats recipe object for output."""
    return {
        "name": recipe.name,
        "description": recipe.description,
        "ingredients": recipe.ingredients.split(", "),
        "steps": recipe.steps.split(";"),
        "url": recipe.url,
        "category": recipe.category.name if recipe.category else None
    }
