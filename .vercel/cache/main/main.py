import os
import logging
from flask import Flask, render_template, request, jsonify

# Setup Flask app with the correct template and static folder
app = Flask(__name__, template_folder='templetss', static_folder='frontend')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Data for Recipes (Updated with new YouTube Shorts URL)
mock_recipes = {
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
    "chocolate cake": {
        "ingredients": ["Flour", "Cocoa Powder", "Sugar", "Eggs", "Butter", "Baking Powder", "Vanilla Extract"],
        "description": "A rich and moist chocolate cake, perfect for any occasion.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "beef stew": {
        "ingredients": ["Beef", "Carrots", "Potatoes", "Onions", "Garlic", "Beef Broth", "Thyme"],
        "description": "A hearty and comforting stew made with tender beef and vegetables.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "butter chicken": {
        "ingredients": ["Chicken", "Butter", "Tomato Puree", "Cream", "Garlic", "Ginger", "Garam Masala"],
        "description": "A rich and creamy Indian dish made with marinated chicken cooked in a spiced butter sauce.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "fish tacos": {
        "ingredients": ["White Fish Fillets", "Taco Shells", "Cabbage", "Lime", "Avocado", "Sour Cream"],
        "description": "A light and fresh Mexican dish made with grilled fish, topped with cabbage and creamy sauce.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "chocolate chip cookies": {
        "ingredients": ["Flour", "Sugar", "Butter", "Eggs", "Chocolate Chips", "Vanilla Extract", "Baking Soda"],
        "description": "Classic cookies loaded with chocolate chips, perfect for dessert or a snack.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "vegetable curry": {
        "ingredients": ["Mixed Vegetables", "Coconut Milk", "Curry Powder", "Ginger", "Garlic", "Onions"],
        "description": "A flavorful curry made with a variety of vegetables and aromatic spices.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "chicken curry": {
        "ingredients": ["Chicken", "Onions", "Tomatoes", "Garlic", "Ginger", "Curry Powder", "Yogurt"],
        "description": "A spicy and rich chicken curry made with aromatic spices and served with rice.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "apple pie": {
        "ingredients": ["Apples", "Sugar", "Butter", "Cinnamon", "Pie Crust", "Lemon Juice"],
        "description": "A warm and sweet dessert made with spiced apples in a flaky pie crust.",
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
                for recipe_name, recipe_info in mock_recipes.items():
                    if user_input in recipe_name:
                        response = recipe_info
                        break

            # Check if the response was found
            if response:
                logger.info(f"Ingredients: {response['ingredients']}")
                return jsonify(response)
            else:
                # No matching recipe found
                return jsonify({"error": "Recipe not found."}), 404

        except Exception as e:
            # Log error and return a failure message
            logger.error(f"Error processing request: {str(e)}")
            return jsonify({"error": "An error occurred while processing your request."}), 500

    return render_template("index.html")

# Run the app for local development
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))



