import logging
from flask import jsonify, request, render_template
from models import Recipe, Category
from extensions import db
from sqlalchemy import or_
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.ERROR)

CHUNK_SIZE = 5
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def setup_routes(app):

    # 🏠 Home route
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    # 🤖 Chatbot API (Gemini 2.0 Flash)
    @app.route("/chatbot-api", methods=["POST"])
    def chatbot_api():
        try:
            data = request.get_json()
            user_input = data.get("prompt", "").strip()

            if not user_input:
                return jsonify({"reply": "Please type something."})

            chat = model.start_chat()

            response = chat.send_message(f"""
You are a professional cooking assistant.
When the user asks about a recipe, respond in **valid JSON only** using this structure:

{{
  "recipe_name": "string",
  "description": "string",
  "prep_time": "string",
  "ingredients": ["item1", "item2", "item3"],
  "steps": ["Step 1", "Step 2", "Step 3"]
}}

Do NOT include markdown, explanations, or text outside JSON.
User query: {user_input}
""")

            reply_text = response.text.strip()

            # Extract only JSON
            json_start = reply_text.find("{")
            json_end = reply_text.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                json_part = reply_text[json_start:json_end]
            else:
                json_part = reply_text

            try:
                structured = json.loads(json_part)
                formatted_reply = f"""
🍽️ **Recipe Name:** {structured.get('recipe_name', 'N/A')}

📝 **Description:** {structured.get('description', 'No description provided.')}

⏰ **Prep Time:** {structured.get('prep_time', 'Not specified')}

🧂 **Ingredients:**
""" + "\n".join([f"• {i}" for i in structured.get('ingredients', [])]) + """


👨‍🍳 **Steps:**
""" + "\n".join([f"{idx+1}. {s}" for idx, s in enumerate(structured.get('steps', []))])

                return jsonify({"reply": formatted_reply.strip()})

            except json.JSONDecodeError:
                return jsonify({"reply": reply_text})

        except Exception as e:
            logging.error(f"Error in chatbot API: {e}", exc_info=True)
            return jsonify({"reply": "⚠️ Error connecting to server"}), 500


    # 🍲 Get Recipes
    @app.route('/get-recipes', methods=['GET'])
    def get_recipes():
        try:
            category = request.args.get('category', '').strip()
            page = max(int(request.args.get('page', 1)), 1)
            query = db.session.query(Recipe).outerjoin(Category).group_by(Recipe.id)

            if category:
                query = query.filter(
                    or_(
                        Recipe.name.ilike(f"%{category}%"),
                        Category.name.ilike(f"%{category}%")
                    )
                )

            recipes = query.offset((page - 1) * CHUNK_SIZE).limit(CHUNK_SIZE).all()
            recipe_data = []
            for r in recipes:
                ingredients = (
                    r.ingredients.split(',') if isinstance(r.ingredients, str) else r.ingredients
                )
                steps = (
                    r.steps.split(';') if isinstance(r.steps, str) else r.steps
                )

                recipe_data.append({
                    'id': r.id,
                    'name': r.name,
                    'description': r.description,
                    'ingredients': [i.strip() for i in ingredients if i.strip()],
                    'steps': [s.strip().capitalize() for s in steps if s.strip()],
                    'url': r.url,
                    'category': r.category.name if r.category else None
                })

            return jsonify(recipe_data)
        except Exception as e:
            logging.error(f"Error fetching recipes: {e}", exc_info=True)
            return jsonify({'error': 'Error fetching recipes'}), 500


    # 📘 Get Recipe Detail
    @app.route('/get-recipe-detail', methods=['GET'])
    def get_recipe_detail():
        try:
            recipe_id = request.args.get('id', '').strip()
            if not recipe_id:
                return jsonify({'error': 'No recipe ID provided'}), 400

            recipe = db.session.query(Recipe).filter(
                (Recipe.id == recipe_id) | (Recipe.name.ilike(f"%{recipe_id}%"))
            ).first()

            if recipe:
                ingredients = (
                    recipe.ingredients.split(',') if isinstance(recipe.ingredients, str) else recipe.ingredients
                )
                steps = (
                    recipe.steps.split(';') if isinstance(recipe.steps, str) else recipe.steps
                )

                data = {
                    'id': recipe.id,
                    'name': recipe.name,
                    'description': recipe.description,
                    'ingredients': [i.strip() for i in ingredients if i.strip()],
                    'steps': [s.strip().capitalize() for s in steps if s.strip()],
                    'url': recipe.url,
                    'category': recipe.category.name if recipe.category else None
                }
                return jsonify(data)
            else:
                return jsonify({'error': 'Recipe not found'}), 404
        except Exception as e:
            logging.error(f"Error fetching recipe details: {e}", exc_info=True)
            return jsonify({'error': 'Error fetching recipe details'}), 500


    # 💡 Get Suggestions
    @app.route('/get-suggestions', methods=['GET'])
    def get_suggestions():
        try:
            query = request.args.get('query', '').strip()
            if not query:
                return jsonify([])

            suggestions = db.session.query(Recipe.name).filter(Recipe.name.ilike(f"%{query}%")).limit(10).all()
            suggestion_list = [s[0] for s in suggestions]
            return jsonify(suggestion_list)
        except Exception as e:
            logging.error(f"Error fetching suggestions: {e}", exc_info=True)
            return jsonify({'error': 'Error fetching suggestions'}), 500


    # 🤖 AI Recipe Search (Gemini powered)
    @app.route('/ai-search', methods=['POST'])
    def ai_search():
        try:
            data = request.get_json()
            query = data.get("query", "").strip()

            if not query:
                return jsonify({"error": "No query provided"}), 400

            prompt = f"""
You are a professional chef.
Suggest 5 unique, creative, and delicious recipes that can be made using: {query}.
Each recipe must include:
- recipe_name
- description
- ingredients (array of 5–10 items)
- steps (array of 5–10 clear steps)

Return the result in **valid JSON only** using this format:
[
  {{
    "recipe_name": "string",
    "description": "string",
    "ingredients": ["item1", "item2", "item3"],
    "steps": ["Step 1", "Step 2", "Step 3"]
  }}
]
Do not include markdown, explanations, or any extra text outside the JSON.
"""

            response = model.generate_content(prompt)
            ai_text = response.text.strip()

            json_start = ai_text.find("[")
            json_end = ai_text.rfind("]") + 1
            if json_start != -1 and json_end != -1:
                json_part = ai_text[json_start:json_end]
            else:
                json_part = ai_text

            recipes = json.loads(json_part)

            formatted_recipes = []
            for r in recipes:
                formatted_recipes.append({
                    "name": r.get("recipe_name", "Unknown Recipe"),
                    "description": r.get("description", ""),
                    "ingredients": r.get("ingredients", []),
                    "steps": r.get("steps", [])
                })

            return jsonify({"recipes": formatted_recipes})

        except Exception as e:
            logging.error(f"Error in ai_search: {e}", exc_info=True)
            return jsonify({"error": "Failed to fetch AI recipes"}), 500


    # 🥘 Get Recipe by Name (for AI results)
    @app.route('/recipe/<recipe_name>', methods=['GET'])
    def get_recipe_by_name(recipe_name):
        try:
            recipe = db.session.query(Recipe).filter(
                Recipe.name.ilike(f"%{recipe_name}%")
            ).first()

            if recipe:
                ingredients = (
                    recipe.ingredients.split(',') if isinstance(recipe.ingredients, str) else recipe.ingredients
                )
                steps = (
                    recipe.steps.split(';') if isinstance(recipe.steps, str) else recipe.steps
                )

                return jsonify([{
                    'id': recipe.id,
                    'name': recipe.name,
                    'description': recipe.description,
                    'ingredients': [i.strip() for i in ingredients if i.strip()],
                    'steps': [s.strip().capitalize() for s in steps if s.strip()],
                    'url': recipe.url,
                    'category': recipe.category.name if recipe.category else None
                }])
            else:
                return jsonify([])
        except Exception as e:
            logging.error(f"Error in /recipe/<recipe_name>: {e}", exc_info=True)
            return jsonify({'error': 'Error fetching recipe'}), 500
