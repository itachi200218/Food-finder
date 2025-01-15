import mysql.connector

# Your connection function
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",         # Change this to your database host
        user="root",              # Replace with your MySQL username
        password="Chetan@0903",   # Replace with your MySQL password
        database="recipedata"     # Replace with your database name
    )

# Mock Data for Recipes (Updated with new YouTube Shorts URL)
mock_recipes = {
    

    "pasta": {
        "ingredients": ["Pasta", "Tomato Sauce", "Garlic", "Olive Oil", "Parmesan Cheese"],
        "description": "A simple pasta dish made with a flavorful tomato sauce, garlic, and a sprinkle of parmesan cheese.",
        "steps": [
            "Boil the pasta in salted water until al dente.",
            "In a pan, heat olive oil and sauté garlic until fragrant.",
            "Add tomato sauce to the pan and simmer for 5 minutes.",
            "Toss the cooked pasta in the sauce until well coated.",
            "Serve hot with a sprinkle of parmesan cheese on top."
        ],
        "url": "https://www.youtube.com/watch?v=xyz123"
    },
    "spaghetti carbonara": {
        "ingredients": ["Spaghetti", "Eggs", "Pancetta", "Parmesan Cheese", "Black Pepper"],
        "description": "A classic Italian pasta dish made with eggs, cheese, pancetta, and pepper.",
        "steps": [
            "Cook spaghetti in salted water until al dente.",
            "In a bowl, whisk eggs and parmesan cheese together.",
            "Cook pancetta in a pan until crispy.",
            "Drain the spaghetti, reserving some pasta water, and add to the pan with pancetta.",
            "Remove the pan from heat and mix in the egg mixture, adding pasta water as needed to create a creamy sauce.",
            "Serve with a sprinkle of black pepper and extra parmesan cheese."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "chicken tacos": {
        "ingredients": ["Chicken Breast", "Taco Shells", "Lettuce", "Tomatoes", "Cheese", "Sour Cream"],
        "description": "A flavorful Mexican dish made with seasoned chicken, fresh toppings, and crunchy taco shells.",
        "steps": [
            "Season the chicken with spices of your choice and cook until fully done.",
            "Shred or slice the cooked chicken into small pieces.",
            "Warm the taco shells in an oven or pan.",
            "Assemble the tacos by adding chicken, lettuce, tomatoes, and cheese.",
            "Top with sour cream and serve immediately."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "vegetable stir fry": {
        "ingredients": ["Bell Peppers", "Broccoli", "Carrots", "Soy Sauce", "Garlic", "Ginger"],
        "description": "A quick and healthy Asian-inspired stir-fry with a mix of colorful vegetables.",
        "steps": [
            "Heat oil in a wok and sauté garlic and ginger until fragrant.",
            "Add chopped vegetables and stir-fry over high heat for 5-7 minutes.",
            "Pour soy sauce over the vegetables and mix well.",
            "Cook for another 2 minutes until the vegetables are tender but crisp.",
            "Serve hot as a side dish or over steamed rice."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "grilled cheese sandwich": {
        "ingredients": ["Bread", "Cheese", "Butter"],
        "description": "A simple yet satisfying sandwich made with buttered bread and melted cheese.",
        "steps": [
            "Butter one side of each bread slice.",
            "Place cheese between two slices of bread, buttered sides out.",
            "Heat a pan and cook the sandwich on medium heat until golden brown on both sides.",
            "Press gently with a spatula to ensure the cheese melts evenly.",
            "Cut in half and serve warm."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },


    
    "caesar salad": {
        "ingredients": ["Romaine Lettuce", "Caesar Dressing", "Croutons", "Parmesan Cheese"],
        "description": "A fresh and crisp salad with romaine lettuce, creamy Caesar dressing, crunchy croutons, and a sprinkle of parmesan cheese.",
        "steps": [
            "Wash and chop the romaine lettuce into bite-sized pieces.",
            "In a large bowl, toss the lettuce with Caesar dressing until evenly coated.",
            "Add croutons and sprinkle with grated parmesan cheese.",
            "Serve immediately, optionally garnished with a lemon wedge."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "pancakes": {
        "ingredients": ["Flour", "Eggs", "Milk", "Baking Powder", "Butter", "Maple Syrup"],
        "description": "Fluffy and golden pancakes, perfect for breakfast, served with syrup and butter.",
        "steps": [
            "In a bowl, mix flour, baking powder, and a pinch of salt.",
            "In a separate bowl, whisk together eggs, milk, and melted butter.",
            "Combine the wet and dry ingredients, mixing until just combined.",
            "Heat a non-stick pan and pour a ladle of batter onto the pan.",
            "Cook until bubbles form on the surface, then flip and cook the other side until golden.",
            "Serve warm with butter and a drizzle of maple syrup."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "miso soup": {
        "ingredients": ["Miso Paste", "Tofu", "Green Onions", "Seaweed", "Dashi Broth"],
        "description": "A comforting Japanese soup made with miso paste, tofu, and a flavorful broth.",
        "steps": [
            "Prepare the dashi broth by boiling water and adding dashi granules or stock.",
            "Lower the heat and dissolve miso paste into the broth using a ladle or strainer.",
            "Add diced tofu and simmer for 2-3 minutes.",
            "Sprinkle chopped green onions and rehydrated seaweed into the soup.",
            "Serve hot as a side dish or starter."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "avocado toast": {
        "ingredients": ["Bread", "Avocado", "Salt", "Pepper", "Olive Oil"],
        "description": "A healthy and delicious toast topped with creamy avocado, seasoned with salt and pepper.",
        "steps": [
            "Toast the bread slices until golden and crisp.",
            "Mash the avocado in a bowl with a fork, adding a pinch of salt and pepper.",
            "Spread the mashed avocado evenly over the toasted bread.",
            "Drizzle with olive oil and sprinkle additional pepper if desired.",
            "Serve immediately as a snack or breakfast option."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "margherita pizza": {
        "ingredients": ["Pizza Dough", "Tomato Sauce", "Mozzarella Cheese", "Basil", "Olive Oil"],
        "description": "A simple yet tasty pizza with tomato sauce, fresh mozzarella, and basil.",
        "steps": [
            "Preheat the oven to the highest temperature (usually 250°C or 475°F).",
            "Roll out the pizza dough to your desired thickness and place it on a baking tray.",
            "Spread an even layer of tomato sauce over the dough.",
            "Top with slices of mozzarella cheese and fresh basil leaves.",
            "Drizzle with olive oil and bake for 10-12 minutes until the crust is golden and the cheese is bubbly.",
            "Serve hot and enjoy!"
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "dal tadka": {
        "ingredients": ["Toor Dal", "Onions", "Tomatoes", "Ginger", "Garlic", "Cumin Seeds", "Mustard Seeds", "Coriander"],
        "description": "A popular Indian lentil dish cooked with spices and topped with a tempering of ghee and cumin seeds.",
        "steps": [
            "Wash the toor dal and pressure cook it with water, turmeric, and a pinch of salt until soft.",
            "In a pan, heat oil or ghee and sauté cumin seeds, mustard seeds, garlic, and ginger until aromatic.",
            "Add chopped onions and tomatoes, and cook until the tomatoes are soft.",
            "Mix the cooked dal into the pan and simmer for 5-7 minutes, adjusting the consistency with water if needed.",
            "Garnish with fresh coriander leaves and serve with rice or roti."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },



    # Updated Mock Data for Recipes with Veg and Non-Veg Categories

   # Veg Recipes

    "vegetable biryani": {
        "ingredients": ["Rice", "Mixed Vegetables", "Spices", "Yogurt", "Onions", "Tomatoes"],
        "description": "Vegetable Biryani is a delightful and aromatic dish where long-grained basmati rice is cooked with a medley of fresh vegetables and fragrant spices. The addition of yogurt gives it a slightly tangy flavor, making it a wholesome and satisfying vegetarian meal.",
        "steps": [
            "Wash and soak basmati rice for 30 minutes, then cook it until 70% done and set aside.",
            "In a pan, heat oil or ghee and sauté sliced onions until golden brown.",
            "Add chopped tomatoes and cook until soft, then stir in spices such as turmeric, cumin, coriander powder, garam masala, and chili powder.",
            "Mix in the mixed vegetables (e.g., carrots, peas, beans, cauliflower) and cook until tender.",
            "Add yogurt and simmer to create a thick masala base.",
            "Layer the partially cooked rice over the vegetable mixture, sprinkle fried onions, mint, and coriander leaves, and cover with a tight lid.",
            "Cook on low heat for 15-20 minutes (dum method) and serve hot with raita."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "paneer butter masala": {
        "ingredients": ["Paneer", "Tomatoes", "Butter", "Cream", "Spices"],
        "description": "Paneer Butter Masala is a rich and creamy dish where soft paneer cubes are cooked in a velvety tomato-based gravy, infused with aromatic spices. The addition of butter and cream gives it a luscious texture, making it a favorite in Indian cuisine.",
        "steps": [
            "Heat butter in a pan and sauté onions and garlic until translucent.",
            "Add chopped tomatoes and cook until soft, then blend into a smooth puree.",
            "Return the puree to the pan and add spices such as turmeric, red chili powder, garam masala, and coriander powder.",
            "Simmer the gravy, then stir in cream to achieve a rich, creamy consistency.",
            "Add cubed paneer and cook for 5-7 minutes, ensuring the paneer absorbs the flavors.",
            "Garnish with a swirl of cream and serve hot with naan or rice."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "chole bhature": {
        "ingredients": ["Chickpeas", "Flour", "Yogurt", "Spices", "Onions", "Tomatoes"],
        "description": "Chole Bhature is a classic North Indian dish comprising spicy and flavorful chickpea curry (chole) paired with soft, deep-fried bread (bhature). The combination is hearty and indulgent, perfect for a special breakfast or lunch.",
        "steps": [
            "Soak chickpeas overnight, then pressure cook until soft.",
            "In a pan, sauté onions, garlic, and ginger until golden, then add tomatoes and cook until mushy.",
            "Add spices such as turmeric, cumin, coriander powder, garam masala, and chole masala, and cook the mixture into a thick gravy.",
            "Mix in the cooked chickpeas and simmer for 10-15 minutes, adjusting consistency with water.",
            "For bhature, knead a dough using flour, yogurt, and a pinch of baking soda. Let it rest for 30 minutes.",
            "Roll out the dough into discs and deep fry until puffed and golden.",
            "Serve the chole hot with freshly made bhature."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "palak paneer": {
        "ingredients": ["Spinach", "Paneer", "Onions", "Garlic", "Tomatoes", "Cream"],
        "description": "Palak Paneer is a healthy and delicious dish where soft paneer cubes are simmered in a creamy spinach puree seasoned with garlic, onions, and a hint of cream. This dish is as nutritious as it is tasty, offering the goodness of greens and protein.",
        "steps": [
            "Blanch spinach leaves in boiling water for 2 minutes, then immediately transfer to ice water to retain color.",
            "Blend the spinach into a smooth puree and set aside.",
            "Heat oil in a pan and sauté onions, garlic, and ginger until golden brown.",
            "Add tomatoes and cook until soft, then mix in spices such as cumin, turmeric, and garam masala.",
            "Stir in the spinach puree and simmer for 5-7 minutes.",
            "Add paneer cubes and cream, cooking for another 2-3 minutes.",
            "Serve hot with naan or steamed rice."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },
    "stuffed paratha": {
        "ingredients": ["Flour", "Potatoes", "Onions", "Spices", "Ghee"],
        "description": "Stuffed Paratha is a versatile Indian flatbread filled with spiced mashed potatoes or other vegetable fillings. It is cooked on a hot griddle with ghee until golden and crispy, making it a comforting meal when served with yogurt or pickle.",
        "steps": [
            "Boil and mash potatoes, then mix with chopped onions, spices (e.g., cumin, chili powder, coriander powder), and fresh coriander leaves.",
            "Knead a soft dough using flour, water, and a pinch of salt. Let it rest for 20 minutes.",
            "Divide the dough into small balls, flatten one ball, and add a portion of the potato filling.",
            "Seal the edges and roll it out gently into a paratha.",
            "Cook on a hot griddle, applying ghee on both sides, until golden brown and crispy.",
            "Serve hot with yogurt, pickle, or chutney."
        ],
        "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
    },


# Non-Veg Recipes
"chicken biryani": {
    "ingredients": ["Rice", "Chicken", "Spices", "Yogurt", "Onions", "Tomatoes", "Ginger-Garlic Paste", "Green Chilies", "Coriander", "Mint", "Ghee"],
    "description": "Chicken Biryani is a flavorful one-pot dish where tender marinated chicken is layered with fragrant basmati rice and cooked with aromatic spices. The slow-cooking method ensures the chicken is juicy, and the rice is infused with a rich, savory flavor.",
    "steps": [
        "Wash and soak the rice for 30 minutes. Cook until 70% done and set aside.",
        "Marinate the chicken with yogurt, ginger-garlic paste, biryani masala, and salt for 30 minutes.",
        "Heat ghee in a pot and add whole spices (bay leaf, cinnamon, cloves, cardamom). Sauté until aromatic.",
        "Add sliced onions and fry until golden brown. Remove half for layering later.",
        "Add chopped tomatoes, green chilies, and marinated chicken. Cook until chicken is tender.",
        "Layer the partially cooked rice over the chicken mixture. Add fried onions, chopped coriander, and mint between layers.",
        "Seal the pot with a lid and cook on low heat for 20-25 minutes (Dum cooking).",
        "Serve hot with raita or salad."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"butter chicken": {
    "ingredients": ["Chicken", "Butter", "Tomatoes", "Cream", "Garlic", "Ginger", "Cashews", "Spices"],
    "description": "Butter Chicken, also known as Murgh Makhani, is a globally loved Indian curry made with succulent pieces of chicken cooked in a creamy tomato-based gravy. The addition of butter and cream enhances its rich texture and mellow flavor, making it irresistible.",
    "steps": [
        "Marinate chicken with yogurt, ginger-garlic paste, red chili powder, and salt. Set aside for 1 hour.",
        "Grill or sauté the marinated chicken until cooked. Keep aside.",
        "Heat butter in a pan, add garlic, ginger, and cashews. Sauté briefly.",
        "Add pureed tomatoes and cook until oil separates. Add salt and spices (coriander, garam masala).",
        "Blend the mixture into a smooth paste and return it to the pan.",
        "Add grilled chicken pieces and simmer for 10 minutes.",
        "Stir in cream and a knob of butter. Adjust seasoning.",
        "Serve hot with naan or steamed rice."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"mutton curry": {
    "ingredients": ["Mutton", "Onions", "Tomatoes", "Ginger", "Garlic", "Spices", "Yogurt"],
    "description": "Mutton Curry is a hearty and robust dish where tender pieces of mutton are slow-cooked in a spiced onion and tomato-based gravy. The deep flavors and tender meat make it a comfort food favorite, especially when paired with rice or roti.",
    "steps": [
        "Heat oil in a pressure cooker. Add whole spices (bay leaf, cinnamon, cloves).",
        "Add sliced onions and sauté until golden brown.",
        "Add ginger-garlic paste and sauté until aromatic.",
        "Add chopped tomatoes and cook until soft. Add yogurt and mix well.",
        "Add mutton pieces, salt, and spices (turmeric, chili powder, garam masala). Mix thoroughly.",
        "Cook on high heat for 5 minutes, then add water and pressure cook for 5-6 whistles.",
        "Simmer the curry to desired consistency and garnish with fresh coriander.",
        "Serve hot with rice or roti."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"fish fry": {
    "ingredients": ["Fish", "Spices", "Lemon", "Rice Flour", "Ginger", "Garlic"],
    "description": "Fish Fry is a crispy and delicious dish where fish fillets are marinated in a blend of spices and herbs, coated in rice flour, and shallow-fried until golden. The result is a dish that is crunchy on the outside and tender inside, perfect as a starter or side dish.",
    "steps": [
        "Clean the fish and pat dry. Marinate with lemon juice, ginger-garlic paste, and spices (turmeric, chili powder, salt).",
        "Let it rest for 20 minutes to absorb the flavors.",
        "Coat the marinated fish pieces in rice flour evenly.",
        "Heat oil in a pan and shallow-fry the fish on medium heat until crispy and golden brown on both sides.",
        "Remove excess oil using a paper towel and serve hot with lemon wedges and salad."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"chicken korma": {
    "ingredients": ["Chicken", "Yogurt", "Cream", "Spices", "Almonds", "Onions"],
    "description": "Chicken Korma is a luxurious dish made with chicken cooked in a rich and creamy gravy of yogurt, cream, and ground almonds. Flavored with aromatic spices, this mildly spiced curry is perfect for special occasions or festive meals.",
    "steps": [
        "Marinate chicken with yogurt, ginger-garlic paste, and spices (turmeric, chili powder, garam masala). Set aside for 1 hour.",
        "Heat oil in a pan and sauté onions until golden brown. Blend into a paste with almonds.",
        "Add whole spices (cardamom, cloves) to the pan and sauté briefly.",
        "Add marinated chicken and cook until partially done.",
        "Stir in the onion-almond paste and cook for 10 minutes.",
        "Add cream and simmer until chicken is tender and the gravy is rich.",
        "Garnish with chopped almonds and serve hot with naan or rice."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},


    #tiffins
    
    "masala dosa": {
    "ingredients": ["Rice", "Urad Dal", "Potatoes", "Onions", "Mustard Seeds", "Curry Leaves", "Turmeric", "Salt"],
    "description": "Masala Dosa is a crispy and savory pancake made from fermented rice and lentil batter, filled with spiced potato filling. It's a staple South Indian breakfast loved across the country.",
    "steps": [
        "Soak rice and urad dal separately for 6 hours. Grind them into a smooth batter and let it ferment overnight.",
        "Boil potatoes, peel, and mash them. Heat oil in a pan and add mustard seeds, curry leaves, and chopped onions. Sauté until onions are golden brown.",
        "Add turmeric, mashed potatoes, and salt. Mix well to prepare the filling.",
        "Heat a dosa tawa (griddle), pour a ladleful of batter, and spread it thinly in a circular motion.",
        "Drizzle oil around the edges and cook until the dosa turns golden and crispy.",
        "Place the potato filling in the center and fold the dosa. Serve hot with coconut chutney and sambar."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"aloo paratha": {
    "ingredients": ["Wheat Flour", "Potatoes", "Cumin Seeds", "Coriander Powder", "Red Chili Powder", "Butter"],
    "description": "Aloo Paratha is a stuffed Indian flatbread made with whole wheat flour and filled with a spicy mashed potato mixture. It's served with yogurt, pickle, or butter.",
    "steps": [
        "Boil potatoes, peel, and mash them. Add cumin seeds, coriander powder, red chili powder, and salt to make the filling.",
        "Knead wheat flour into a soft dough and let it rest for 30 minutes.",
        "Divide the dough into equal portions and roll each portion into a small circle.",
        "Place the potato filling in the center, fold the edges, and roll it into a flat paratha.",
        "Heat a tawa, place the paratha on it, and cook on both sides until golden brown. Apply butter while cooking.",
        "Serve hot with yogurt or pickle."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"samosa": {
    "ingredients": ["Potatoes", "Green Peas", "Cumin Seeds", "Coriander", "Garam Masala", "Flour", "Oil"],
    "description": "Samosa is a popular Indian snack, consisting of a crispy triangular pastry filled with spiced potatoes and peas, deep-fried to golden perfection.",
    "steps": [
        "Prepare the dough by mixing flour, salt, and oil. Add water gradually to make a stiff dough. Let it rest for 30 minutes.",
        "Boil and mash potatoes. Sauté cumin seeds in oil, then add green peas, mashed potatoes, garam masala, and coriander. Mix well for the filling.",
        "Divide the dough into small balls, roll each into a thin circle, and cut in half to make a cone.",
        "Fill the cone with potato mixture, seal the edges with water, and shape into a triangle.",
        "Deep fry the samosas in hot oil until golden and crisp. Serve with chutney."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"pav bhaji": {
    "ingredients": ["Potatoes", "Mixed Vegetables", "Butter", "Pav Bhaji Masala", "Pav (bread rolls)"],
    "description": "Pav Bhaji is a spicy mashed vegetable curry served with butter-toasted bread rolls. It's a popular street food in India, loved for its rich flavors and textures.",
    "steps": [
        "Boil potatoes and mixed vegetables (like carrots, peas, and cauliflower) until soft. Mash them well.",
        "Heat butter in a pan, sauté chopped onions until golden brown, and add chopped tomatoes. Cook until soft.",
        "Add pav bhaji masala, chili powder, and mashed vegetables. Mix well and simmer for 10 minutes.",
        "Butter the pav (bread rolls) on a tawa and toast until golden.",
        "Serve the bhaji with buttered pav, chopped onions, and lemon wedges."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"quiche lorraine": {
    "ingredients": ["Eggs", "Cream", "Bacon", "Cheese", "Spinach", "Onion", "Pie Crust"],
    "description": "Quiche Lorraine is a classic French savory tart with a creamy custard filling, crispy bacon, melted cheese, and onions, baked in a flaky pie crust.",
    "steps": [
        "Preheat the oven to 180°C (350°F). Roll out the pie crust and place it in a tart pan. Prick the base with a fork and blind bake for 10 minutes.",
        "Cook bacon until crispy, then sauté onions and spinach in the same pan.",
        "Whisk eggs and cream together, season with salt and pepper.",
        "Layer the cooked bacon, onions, spinach, and cheese in the pie crust.",
        "Pour the egg mixture over the fillings and bake for 30-40 minutes, or until the filling is set and golden.",
        "Cool slightly before serving."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"falafel": {
    "ingredients": ["Chickpeas", "Garlic", "Parsley", "Cumin", "Coriander", "Onion", "Flour"],
    "description": "Deep-fried balls made from ground chickpeas, herbs, and spices, usually served in pita with tahini sauce. Falafel is crunchy on the outside and tender on the inside.",
    "steps": [
        "Soak chickpeas in water overnight, then drain.",
        "Blend the chickpeas with garlic, parsley, cumin, coriander, and onion until a coarse mixture forms.",
        "Add flour to the mixture to help bind the ingredients.",
        "Shape the mixture into balls or patties.",
        "Heat oil in a deep frying pan and fry the falafel until golden brown and crispy.",
        "Serve in pita with tahini sauce, and garnish with fresh vegetables."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"banh mi": {
    "ingredients": ["Baguette", "Pork", "Pickled Vegetables", "Cilantro", "Cucumber", "Jalapenos", "Mayo"],
    "description": "A Vietnamese sandwich made with a crispy baguette and savory fillings like pork, pickled vegetables, and fresh herbs, offering a combination of flavors and textures.",
    "steps": [
        "Marinate pork with soy sauce, garlic, sugar, and pepper.",
        "Grill or fry the marinated pork until cooked through.",
        "Slice the baguette lengthwise and spread a layer of mayo.",
        "Layer grilled pork, pickled vegetables, cucumber, cilantro, and jalapenos inside the baguette.",
        "Serve fresh, optionally adding more hot sauce."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"paella": {
    "ingredients": ["Rice", "Saffron", "Shrimp", "Mussels", "Chicken", "Peas", "Bell Peppers"],
    "description": "A traditional Spanish rice dish with saffron, seafood, and vegetables, cooked in one pan. Known for vibrant colors and rich flavors.",
    "steps": [
        "Sauté onions and bell peppers in oil until soft.",
        "Add rice and toast lightly, then add saffron and chicken broth.",
        "Add remaining vegetables and proteins, simmering without stirring.",
        "Add seafood (shrimp, mussels) in the last 10-15 minutes of cooking.",
        "Serve with lemon wedges and fresh parsley."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"dim sum": {
    "ingredients": ["Pork", "Shrimp", "Dumpling Wrappers", "Mushrooms", "Soy Sauce", "Ginger"],
    "description": "Small bite-sized portions of food, often served in bamboo baskets, including dumplings and buns. It's a Cantonese dish traditionally served with tea.",
    "steps": [
        "Mix ground pork, shrimp, soy sauce, ginger, and mushrooms for the filling.",
        "Place the filling in each dumpling wrapper and fold into a pleated shape.",
        "Steam the dumplings in a bamboo steamer for 10-15 minutes until fully cooked.",
        "Serve with soy sauce or your favorite dipping sauce."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},

    #sea foods
    
    "shrimp scampi": {
    "ingredients": ["Shrimp", "Garlic", "Butter", "Lemon", "Parsley", "Olive Oil", "Linguine"],
    "description": "A flavorful pasta dish made with shrimp, garlic, butter, and a splash of lemon, creating a rich and savory sauce.",
    "steps": [
        "Cook linguine pasta in salted boiling water until al dente.",
        "In a large pan, heat olive oil and sauté garlic until fragrant.",
        "Add shrimp to the pan and cook until pink and opaque.",
        "Stir in butter and lemon juice, letting it melt into the sauce.",
        "Toss the cooked linguine into the pan, mixing it well with the shrimp and sauce.",
        "Garnish with chopped parsley and serve with extra lemon wedges."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"grilled salmon": {
    "ingredients": ["Salmon Fillets", "Olive Oil", "Garlic", "Lemon", "Dill", "Salt", "Pepper"],
    "description": "Fresh salmon fillets grilled to perfection with a zesty lemon and garlic marinade, offering a smoky flavor and tender texture.",
    "steps": [
        "Preheat the grill to medium-high heat.",
        "Mix olive oil, minced garlic, lemon juice, dill, salt, and pepper in a bowl.",
        "Brush the salmon fillets with the marinade, ensuring they are well coated.",
        "Grill the salmon fillets skin-side down for about 6-8 minutes per side, or until cooked through.",
        "Serve the salmon with a wedge of lemon and a sprinkle of fresh dill."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"clam chowder": {
    "ingredients": ["Clams", "Cream", "Onions", "Potatoes", "Celery", "Butter", "Thyme"],
    "description": "A rich and creamy soup made with fresh clams, potatoes, and a touch of thyme, creating a comforting and savory dish.",
    "steps": [
        "Chop onions, potatoes, and celery into small pieces.",
        "In a large pot, melt butter and sauté onions and celery until softened.",
        "Add diced potatoes and cook for a few minutes before adding clams and their juice.",
        "Pour in the cream and bring the mixture to a simmer, cooking for 15-20 minutes until the potatoes are tender.",
        "Season with thyme, salt, and pepper to taste.",
        "Serve hot with a sprinkle of fresh parsley."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"lobster rolls": {
    "ingredients": ["Lobster", "Buns", "Mayonnaise", "Lemon", "Celery", "Butter"],
    "description": "Sweet lobster meat mixed with mayonnaise and served in a soft bun, topped with butter, offering a rich and flavorful seafood treat.",
    "steps": [
        "Cook the lobster meat by boiling or steaming it until fully cooked, then chop it into small chunks.",
        "In a bowl, mix the lobster meat with mayonnaise, lemon juice, and finely chopped celery.",
        "Butter the buns and toast them lightly on a griddle.",
        "Fill the toasted buns with the lobster mixture and serve with extra lemon wedges."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"fish tacos": {
    "ingredients": ["White Fish (like Cod)", "Corn Tortillas", "Cabbage", "Lime", "Avocado", "Sour Cream", "Chili Powder"],
    "description": "Crispy fish served in a soft tortilla with tangy slaw and a squeeze of lime, offering a delicious and fresh meal.",
    "steps": [
        "Season the fish fillets with chili powder, salt, and pepper, then cook them in a pan with olive oil until crispy.",
        "Shred the cabbage and toss with lime juice to create a fresh slaw.",
        "Warm the corn tortillas on a griddle.",
        "Assemble the tacos by placing the cooked fish in the tortillas, topping with slaw, avocado slices, and a drizzle of sour cream."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"seared tuna": {
    "ingredients": ["Tuna Steaks", "Sesame Seeds", "Soy Sauce", "Ginger", "Garlic", "Olive Oil"],
    "description": "Perfectly seared tuna steaks coated with sesame seeds and served with a soy and ginger sauce, offering a fresh and savory flavor.",
    "steps": [
        "Coat the tuna steaks with sesame seeds on both sides.",
        "Heat olive oil in a pan over medium-high heat.",
        "Sear the tuna steaks for 1-2 minutes per side, depending on desired doneness.",
        "In a small bowl, mix soy sauce, minced garlic, and grated ginger for the sauce.",
        "Serve the seared tuna with the soy-ginger sauce on top."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"paella de mariscos": {
    "ingredients": ["Shrimp", "Mussels", "Clams", "Squid", "Rice", "Saffron", "Bell Peppers", "Tomatoes"],
    "description": "A seafood version of the traditional Spanish paella, featuring a variety of shellfish and saffron rice, creating a fragrant and flavorful dish.",
    "steps": [
        "Sauté bell peppers and tomatoes in olive oil until softened.",
        "Add rice and cook for a few minutes, then add saffron and warm seafood broth.",
        "Add the shellfish (shrimp, mussels, clams, and squid) and let it cook, avoiding stirring.",
        "Simmer until the rice is fully cooked and the shellfish has opened up.",
        "Serve with lemon wedges and garnish with fresh herbs."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"oysters Rockefeller": {
    "ingredients": ["Oysters", "Spinach", "Breadcrumbs", "Parmesan Cheese", "Garlic", "Butter", "Herbs"],
    "description": "Fresh oysters topped with a rich spinach and breadcrumb mixture, then baked until golden and crispy, offering a delicious seafood appetizer.",
    "steps": [
        "Shuck the oysters and place them on a baking tray.",
        "In a pan, sauté garlic in butter and add spinach, cooking until wilted.",
        "Mix spinach with breadcrumbs, parmesan cheese, and chopped herbs.",
        "Top each oyster with the spinach-breadcrumb mixture.",
        "Bake the oysters at 375°F for 10-12 minutes, or until the topping is golden brown."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"shrimp tempura": {
    "ingredients": ["Shrimp", "Flour", "Cornstarch", "Egg", "Cold Water", "Soy Sauce"],
    "description": "Crispy battered shrimp, deep-fried to perfection, often served with a soy-based dipping sauce, offering a light and crunchy texture.",
    "steps": [
        "Peel and devein the shrimp, leaving the tails on.",
        "In a bowl, mix flour, cornstarch, egg, and cold water to make a batter.",
        "Dip the shrimp in the batter, then deep fry in hot oil until golden and crispy.",
        "Serve with a soy-based dipping sauce or sweet chili sauce."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"grilled shrimp skewers": {
    "ingredients": ["Shrimp", "Olive Oil", "Garlic", "Lemon", "Paprika", "Cilantro", "Skewers"],
    "description": "Juicy shrimp marinated in garlic, lemon, and spices, then grilled on skewers for a smoky and flavorful dish.",
    "steps": [
        "Marinate the shrimp with olive oil, minced garlic, lemon juice, paprika, and chopped cilantro for at least 30 minutes.",
        "Thread the shrimp onto skewers.",
        "Grill the skewers for 2-3 minutes per side until the shrimp are pink and cooked through.",
        "Serve with extra cilantro and lemon wedges."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},

    #egg
    "egg curry": {
    "ingredients": ["Eggs", "Onions", "Tomatoes", "Ginger", "Garlic", "Cumin Seeds", "Coriander Powder", "Turmeric", "Chili Powder", "Garam Masala", "Cilantro", "Salt", "Oil"],
    "description": "A flavorful and comforting Indian curry made with boiled eggs cooked in a rich, spicy onion-tomato gravy infused with cumin, coriander, turmeric, and garam masala. Garnished with fresh cilantro, this dish is typically served with rice or naan.",
    "steps": [
        "Heat oil in a pan, add cumin seeds and let them splutter.",
        "Add finely chopped onions and sauté until golden brown.",
        "Add grated ginger and minced garlic, sauté for 2 minutes.",
        "Add pureed tomatoes, turmeric, chili powder, coriander powder, and salt. Cook until oil separates from the masala.",
        "Add water to adjust gravy consistency and let it simmer for 5-7 minutes.",
        "Add boiled eggs (cut in half or whole) into the curry. Cook for 5 minutes to soak the flavors.",
        "Sprinkle garam masala and garnish with fresh cilantro.",
        "Serve with rice or naan."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"pani puri": {
    "ingredients": ["Semolina", "Flour", "Potatoes", "Chickpeas", "Tamarind", "Mint", "Cilantro", "Green Chilies", "Cumin Powder", "Chat Masala", "Black Salt", "Salt", "Water"],
    "description": "Pani Puri is a popular Indian street food where crispy hollow puris are filled with spiced potato and chickpea filling, then dipped into tangy and spicy mint-flavored water. Each bite is a burst of flavor and texture, making it a favorite snack.",
    "steps": [
        "Mix semolina, flour, and salt. Knead into a smooth dough.",
        "Roll dough into small balls and flatten. Deep fry in hot oil until crispy.",
        "Mash boiled potatoes and mix with boiled chickpeas, cumin powder, black salt, and chat masala.",
        "For the pani: Blend mint leaves, cilantro, green chilies, tamarind, cumin powder, chat masala, black salt, and salt with water.",
        "Fill each puri with the potato-chickpea mixture and dip into the pani.",
        "Serve immediately for a crunchy, flavorful experience."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
},
"rajma masala": {
    "ingredients": ["Kidney Beans", "Onions", "Tomatoes", "Garlic", "Ginger", "Cumin Seeds", "Garam Masala", "Turmeric", "Red Chili Powder", "Coriander Powder", "Cilantro", "Salt", "Oil"],
    "description": "Rajma Masala is a comforting North Indian curry made with red kidney beans cooked in a spiced onion-tomato gravy. The creamy texture and rich flavors make it a perfect companion for steamed basmati rice, famously known as 'Rajma Chawal'.",
    "steps": [
        "Soak kidney beans overnight and pressure cook them until soft.",
        "Heat oil in a pan, add cumin seeds and let them splutter.",
        "Add finely chopped onions and sauté until golden brown.",
        "Add ginger-garlic paste and sauté for 2 minutes.",
        "Add chopped tomatoes, turmeric, red chili powder, coriander powder, and salt. Cook until oil separates from the masala.",
        "Add the cooked kidney beans and adjust the gravy by adding water. Let it simmer for 15 minutes.",
        "Sprinkle garam masala and garnish with fresh cilantro.",
        "Serve with steamed basmati rice."
    ],
    "url": "https://youtube.com/shorts/gizichkVuYU?si=fqvDBo_n0nzssKqu"
}
}
def insert_mock_data():
    db = connect_to_db()
    cursor = db.cursor()

    # Insert each recipe into the `recipe` table
    for name, details in mock_recipes.items():
        ingredients = ", ".join(details["ingredients"])
        description = details["description"]
        steps = "; ".join(details["steps"])
        url = details.get("url", None)

        # Use INSERT INTO recipe to insert data into the correct table
        query = """
        INSERT INTO recipes (name, ingredients, description, steps, url)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (name, ingredients, description, steps, url)

        try:
            cursor.execute(query, values)
            print(f"Inserted recipe: {name}")
        except mysql.connector.Error as err:
            print(f"Error inserting {name}: {err}")

    # Commit changes to the database
    try:
        db.commit()
        print("Mock data inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Error committing changes: {err}")

    # Close the database connection
    cursor.close()
    db.close()
    print("Database connection closed.")

# Call the function
insert_mock_data()