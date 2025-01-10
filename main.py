import os
import logging
from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import process

# Setup Flask app with the correct template and static folder
app = Flask(__name__, template_folder='templetss', static_folder='frontend')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Data for Recipes (Updated with new YouTube Shorts URL)
mock_recipes = {
    
    
    "pasta": {
        "ingredients": ["Pasta", "Tomato Sauce", "Garlic", "Olive Oil", "Parmesan Cheese"],
        "description": "A simple pasta dish made with a flavorful tomato sauce, garlic, and a sprinkle of parmesan cheese.",
        "url": "https://www.youtube.com/watch?v=xyz123"
    },
    "spaghetti carbonara": {
        "ingredients": ["Spaghetti", "Eggs", "Pancetta", "Parmesan Cheese", "Black Pepper"],
        "description": "A classic Italian pasta dish made with eggs, cheese, pancetta, and pepper.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "chicken tacos": {
        "ingredients": ["Chicken Breast", "Taco Shells", "Lettuce", "Tomatoes", "Cheese", "Sour Cream"],
        "description": "A flavorful Mexican dish made with seasoned chicken, fresh toppings, and crunchy taco shells.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "vegetable stir fry": {
        "ingredients": ["Bell Peppers", "Broccoli", "Carrots", "Soy Sauce", "Garlic", "Ginger"],
        "description": "A quick and healthy Asian-inspired stir-fry with a mix of colorful vegetables.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "grilled cheese sandwich": {
        "ingredients": ["Bread", "Cheese", "Butter"],
        "description": "A simple yet satisfying sandwich made with buttered bread and melted cheese.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "caesar salad": {
        "ingredients": ["Romaine Lettuce", "Caesar Dressing", "Croutons", "Parmesan Cheese"],
        "description": "A fresh and crisp salad with romaine lettuce, creamy Caesar dressing, and crunchy croutons.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "pancakes": {
        "ingredients": ["Flour", "Eggs", "Milk", "Baking Powder", "Butter", "Maple Syrup"],
        "description": "Fluffy and golden pancakes, perfect for breakfast, served with syrup and butter.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "miso soup": {
        "ingredients": ["Miso Paste", "Tofu", "Green Onions", "Seaweed", "Dashi Broth"],
        "description": "A comforting Japanese soup made with miso paste, tofu, and a flavorful broth.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "avocado toast": {
        "ingredients": ["Bread", "Avocado", "Salt", "Pepper", "Olive Oil"],
        "description": "A healthy and delicious toast topped with creamy avocado, seasoned with salt and pepper.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "margherita pizza": {
        "ingredients": ["Pizza Dough", "Tomato Sauce", "Mozzarella Cheese", "Basil", "Olive Oil"],
        "description": "A simple yet tasty pizza with tomato sauce, fresh mozzarella, and basil.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "dal tadka": {
        "ingredients": ["Toor Dal", "Onions", "Tomatoes", "Ginger", "Garlic", "Cumin Seeds", "Mustard Seeds", "Coriander"],
        "description": "A popular Indian lentil dish cooked with spices and topped with a tempering of ghee and cumin seeds.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },

    # Updated Mock Data for Recipes with Veg and Non-Veg Categories

    # Veg Recipes
    "vegetable biryani": {
        "ingredients": ["Rice", "Mixed Vegetables", "Spices", "Yogurt", "Onions", "Tomatoes"],
        "description": "A fragrant rice dish made with mixed vegetables, aromatic spices, and yogurt.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "paneer butter masala": {
        "ingredients": ["Paneer", "Tomatoes", "Butter", "Cream", "Spices"],
        "description": "A creamy and rich dish made with paneer in a spiced tomato-based gravy.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "chole bhature": {
        "ingredients": ["Chickpeas", "Flour", "Yogurt", "Spices", "Onions", "Tomatoes"],
        "description": "A North Indian dish consisting of spicy chickpeas served with deep-fried bread (bhature).",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "palak paneer": {
        "ingredients": ["Spinach", "Paneer", "Onions", "Garlic", "Tomatoes", "Cream"],
        "description": "A classic dish with paneer cubes cooked in a smooth spinach gravy.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "stuffed paratha": {
        "ingredients": ["Flour", "Potatoes", "Onions", "Spices", "Ghee"],
        "description": "A stuffed flatbread, usually filled with spiced mashed potatoes or other vegetables.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },

    # Non-Veg Recipes
    "chicken biryani": {
        "ingredients": ["Rice", "Chicken", "Spices", "Yogurt", "Onions", "Tomatoes"],
        "description": "A flavorful rice dish made with marinated chicken, aromatic spices, and fragrant basmati rice.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "butter chicken": {
        "ingredients": ["Chicken", "Butter", "Tomatoes", "Cream", "Garlic", "Ginger"],
        "description": "Tender chicken pieces cooked in a rich and creamy tomato-based sauce.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "mutton curry": {
        "ingredients": ["Mutton", "Onions", "Tomatoes", "Ginger", "Garlic", "Spices"],
        "description": "A hearty curry made with tender mutton cooked in a rich and flavorful gravy.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "fish fry": {
        "ingredients": ["Fish", "Spices", "Lemon", "Rice Flour", "Ginger", "Garlic"],
        "description": "Crispy fried fish pieces marinated with aromatic spices and herbs.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "chicken korma": {
        "ingredients": ["Chicken", "Yogurt", "Cream", "Spices", "Almonds", "Onions"],
        "description": "A mild and creamy chicken curry made with yogurt, cream, and aromatic spices.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    }
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Parse incoming JSON request
            data = request.get_json()
            user_input = data.get("prompt", "").lower().strip()

            # Debug: Log the user input to ensure it's coming through correctly
            logger.info(f"Received user input: {user_input}")

            # Check if the input matches any recipe names or contains certain words
            response = {}
            if user_input in mock_recipes:
                response = mock_recipes[user_input]
            else:
                # Search for recipes containing keywords in the name (fuzzy search for now)
                matched_recipe = process.extractOne(user_input, mock_recipes.keys(), score_cutoff=70)

                # If a match is found, return its details
                if matched_recipe:
                    recipe_name = matched_recipe[0]
                    response = mock_recipes[recipe_name]
                else:
                    # Return no match message
                    response = {"error": "No matching recipe found."}

            return jsonify(response)
        except Exception as e:
            # Log the error if any occurs during request handling
            logger.error(f"Error processing request: {e}")
            return jsonify({"error": "An error occurred while processing the request."}), 500
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)










