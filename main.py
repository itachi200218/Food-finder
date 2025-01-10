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
    "description": "Vegetable Biryani is a delightful and aromatic dish where long-grained basmati rice is cooked with a medley of fresh vegetables and fragrant spices. The addition of yogurt gives it a slightly tangy flavor, making it a wholesome and satisfying vegetarian meal.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"paneer butter masala": {
    "ingredients": ["Paneer", "Tomatoes", "Butter", "Cream", "Spices"],
    "description": "Paneer Butter Masala is a rich and creamy dish where soft paneer cubes are cooked in a velvety tomato-based gravy, infused with aromatic spices. The addition of butter and cream gives it a luscious texture, making it a favorite in Indian cuisine.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"chole bhature": {
    "ingredients": ["Chickpeas", "Flour", "Yogurt", "Spices", "Onions", "Tomatoes"],
    "description": "Chole Bhature is a classic North Indian dish comprising spicy and flavorful chickpea curry (chole) paired with soft, deep-fried bread (bhature). The combination is hearty and indulgent, perfect for a special breakfast or lunch.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"palak paneer": {
    "ingredients": ["Spinach", "Paneer", "Onions", "Garlic", "Tomatoes", "Cream"],
    "description": "Palak Paneer is a healthy and delicious dish where soft paneer cubes are simmered in a creamy spinach puree seasoned with garlic, onions, and a hint of cream. This dish is as nutritious as it is tasty, offering the goodness of greens and protein.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"stuffed paratha": {
    "ingredients": ["Flour", "Potatoes", "Onions", "Spices", "Ghee"],
    "description": "Stuffed Paratha is a versatile Indian flatbread filled with spiced mashed potatoes or other vegetable fillings. It is cooked on a hot griddle with ghee until golden and crispy, making it a comforting meal when served with yogurt or pickle.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},

# Non-Veg Recipes
"chicken biryani": {
    "ingredients": ["Rice", "Chicken", "Spices", "Yogurt", "Onions", "Tomatoes"],
    "description": "Chicken Biryani is a flavorful one-pot dish where tender marinated chicken is layered with fragrant basmati rice and cooked with aromatic spices. The slow-cooking method ensures the chicken is juicy, and the rice is infused with a rich, savory flavor.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"butter chicken": {
    "ingredients": ["Chicken", "Butter", "Tomatoes", "Cream", "Garlic", "Ginger"],
    "description": "Butter Chicken, also known as Murgh Makhani, is a globally loved Indian curry made with succulent pieces of chicken cooked in a creamy tomato-based gravy. The addition of butter and cream enhances its rich texture and mellow flavor, making it irresistible.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"mutton curry": {
    "ingredients": ["Mutton", "Onions", "Tomatoes", "Ginger", "Garlic", "Spices"],
    "description": "Mutton Curry is a hearty and robust dish where tender pieces of mutton are slow-cooked in a spiced onion and tomato-based gravy. The deep flavors and tender meat make it a comfort food favorite, especially when paired with rice or roti.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"fish fry": {
    "ingredients": ["Fish", "Spices", "Lemon", "Rice Flour", "Ginger", "Garlic"],
    "description": "Fish Fry is a crispy and delicious dish where fish fillets are marinated in a blend of spices and herbs, coated in rice flour, and shallow-fried until golden. The result is a dish that is crunchy on the outside and tender inside, perfect as a starter or side dish.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"chicken korma": {
    "ingredients": ["Chicken", "Yogurt", "Cream", "Spices", "Almonds", "Onions"],
    "description": "Chicken Korma is a luxurious dish made with chicken cooked in a rich and creamy gravy of yogurt, cream, and ground almonds. Flavored with aromatic spices, this mildly spiced curry is perfect for special occasions or festive meals.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},

    #tiffins
    
    
    "masala dosa": {
        "ingredients": ["Rice", "Urad Dal", "Potatoes", "Onions", "Mustard Seeds", "Curry Leaves", "Turmeric", "Salt"],
        "description": "A crispy and savory pancake made from fermented rice and lentil batter, filled with spiced potato filling.",
        "steps": [
            "Soak rice and urad dal for 4-6 hours, then grind into a smooth batter and ferment overnight.",
            "Boil potatoes, mash them, and sauté with mustard seeds, curry leaves, onions, and turmeric to make the filling.",
            "Heat a non-stick pan, pour a ladleful of batter, and spread into a thin circle.",
            "Cook until golden, place the filling in the center, fold, and serve hot with coconut chutney and sambar."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "aloo paratha": {
        "ingredients": ["Wheat Flour", "Potatoes", "Cumin Seeds", "Coriander Powder", "Red Chili Powder", "Butter"],
        "description": "A stuffed flatbread with spiced mashed potatoes, served with yogurt or pickle.",
        "steps": [
            "Prepare dough using wheat flour, water, and a pinch of salt. Let it rest for 20 minutes.",
            "Boil and mash potatoes, then mix in cumin seeds, coriander powder, red chili powder, and salt.",
            "Roll out a small dough ball, place the potato filling in the center, and seal the edges.",
            "Roll it out gently and cook on a hot griddle with butter until golden on both sides."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "samosa": {
        "ingredients": ["Potatoes", "Green Peas", "Cumin Seeds", "Coriander", "Garam Masala", "Flour"],
        "description": "A popular deep-fried snack filled with spiced potatoes and peas.",
        "steps": [
            "Make dough using flour, salt, and oil, then let it rest for 30 minutes.",
            "Prepare the filling by boiling potatoes, mashing them, and mixing with green peas, cumin seeds, coriander, and garam masala.",
            "Roll out the dough, cut into semi-circles, fold into a cone, and fill with the potato mixture.",
            "Seal the edges, deep-fry in hot oil until golden, and serve hot."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "pav bhaji": {
        "ingredients": ["Potatoes", "Mixed Vegetables", "Butter", "Pav Bhaji Masala", "Pav (bread rolls)"],
        "description": "A spicy mashed vegetable curry served with buttered bread rolls.",
        "steps": [
            "Boil and mash potatoes and other mixed vegetables like peas, carrots, and cauliflower.",
            "Sauté onions, add tomatoes, and cook until soft. Mix in pav bhaji masala and the mashed vegetables.",
            "Simmer the mixture with butter, adjusting seasoning as needed.",
            "Serve hot with buttered pav rolls, garnished with cilantro and a slice of lemon."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "quiche lorraine": {
        "ingredients": ["Eggs", "Cream", "Bacon", "Cheese", "Spinach", "Onion", "Pie Crust"],
        "description": "A savory tart filled with eggs, cream, cheese, and bacon, baked to perfection.",
        "steps": [
            "Prepare a pie crust or use a store-bought one, and blind bake it for 10 minutes.",
            "Cook bacon until crispy, then sauté onions and spinach in the same pan.",
            "Whisk together eggs, cream, and cheese, and add the cooked bacon and vegetables.",
            "Pour the mixture into the crust, bake at 180°C (350°F) for 30-40 minutes, and serve warm."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },

    #sea foods
    
    "shrimp scampi": {
        "ingredients": ["Shrimp", "Garlic", "Butter", "Lemon", "Parsley", "Olive Oil", "Linguine"],
        "description": "A flavorful pasta dish made with shrimp, garlic, butter, and a splash of lemon.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "grilled salmon": {
        "ingredients": ["Salmon Fillets", "Olive Oil", "Garlic", "Lemon", "Dill", "Salt", "Pepper"],
        "description": "Fresh salmon fillets grilled to perfection with a zesty lemon and garlic marinade.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "clam chowder": {
        "ingredients": ["Clams", "Cream", "Onions", "Potatoes", "Celery", "Butter", "Thyme"],
        "description": "A rich and creamy soup made with fresh clams, potatoes, and a touch of thyme.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "lobster rolls": {
        "ingredients": ["Lobster", "Buns", "Mayonnaise", "Lemon", "Celery", "Butter"],
        "description": "Sweet lobster meat mixed with mayonnaise and served in a soft bun, topped with butter.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "fish tacos": {
        "ingredients": ["White Fish (like Cod)", "Corn Tortillas", "Cabbage", "Lime", "Avocado", "Sour Cream", "Chili Powder"],
        "description": "Crispy fish served in a soft tortilla with tangy slaw and a squeeze of lime.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "seared tuna": {
        "ingredients": ["Tuna Steaks", "Sesame Seeds", "Soy Sauce", "Ginger", "Garlic", "Olive Oil"],
        "description": "Perfectly seared tuna steaks coated with sesame seeds and served with a soy and ginger sauce.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "paella de mariscos": {
        "ingredients": ["Shrimp", "Mussels", "Clams", "Squid", "Rice", "Saffron", "Bell Peppers", "Tomatoes"],
        "description": "A seafood version of the traditional Spanish paella, featuring a variety of shellfish and saffron rice.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "oysters Rockefeller": {
        "ingredients": ["Oysters", "Spinach", "Breadcrumbs", "Parmesan Cheese", "Garlic", "Butter", "Herbs"],
        "description": "Fresh oysters topped with a rich spinach and breadcrumb mixture, then baked until golden.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "shrimp tempura": {
        "ingredients": ["Shrimp", "Flour", "Cornstarch", "Egg", "Cold Water", "Soy Sauce"],
        "description": "Crispy battered shrimp, deep-fried to perfection, often served with a soy-based dipping sauce.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "grilled shrimp skewers": {
        "ingredients": ["Shrimp", "Olive Oil", "Garlic", "Lemon", "Paprika", "Cilantro", "Skewers"],
        "description": "Juicy shrimp marinated in garlic, lemon, and spices, then grilled on skewers for a smoky flavor.",
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    #egg
    "egg curry": {
    "ingredients": ["Eggs", "Onions", "Tomatoes", "Ginger", "Garlic", "Cumin Seeds", "Coriander Powder", "Turmeric", "Chili Powder", "Garam Masala", "Cilantro", "Salt", "Oil"],
    "description": "A flavorful and comforting Indian curry made with boiled eggs cooked in a rich, spicy onion-tomato gravy infused with cumin, coriander, turmeric, and garam masala. Garnished with fresh cilantro, this dish is typically served with rice or naan.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"pani puri": {
    "ingredients": ["Semolina", "Flour", "Potatoes", "Chickpeas", "Tamarind", "Mint", "Cilantro", "Green Chilies", "Cumin Powder", "Chat Masala", "Black Salt", "Salt", "Water"],
    "description": "Pani Puri is a popular Indian street food where crispy hollow puris are filled with spiced potato and chickpea filling, then dipped into tangy and spicy mint-flavored water. Each bite is a burst of flavor and texture, making it a favorite snack.",
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"rajma masala": {
    "ingredients": ["Kidney Beans", "Onions", "Tomatoes", "Garlic", "Ginger", "Cumin Seeds", "Garam Masala", "Turmeric", "Red Chili Powder", "Coriander Powder", "Cilantro", "Salt", "Oil"],
    "description": "Rajma Masala is a comforting North Indian curry made with red kidney beans cooked in a spiced onion-tomato gravy. The creamy texture and rich flavors make it a perfect companion for steamed basmati rice, famously known as 'Rajma Chawal'.",
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























