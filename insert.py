import mysql.connector
import os
from db import connect_to_db



# Mock Data for Recipes (Updated with new YouTube Shorts URL)
mock_recipes = {
    

 "chicken_pakoda": {
    "ingredients": ["Chicken", "Gram Flour", "Rice Flour", "Ginger-Garlic Paste", "Red Chili Powder", "Turmeric", "Coriander Powder", "Garam Masala", "Salt", "Curry Leaves", "Green Chilies", "Oil for Frying"],
    "description": "A crispy and spicy Indian snack made with marinated chicken, coated in a flavorful batter and deep-fried to golden perfection.",
    "steps": [
      "Cut chicken into bite-sized pieces and marinate with ginger-garlic paste, turmeric, red chili powder, coriander powder, garam masala, and salt. Let it rest for 30 minutes.",
      "In a bowl, mix gram flour, rice flour, and a pinch of salt. Add curry leaves and chopped green chilies.",
      "Add the marinated chicken to the flour mixture and coat well. Sprinkle water if needed to make the coating stick.",
      "Heat oil in a deep pan. Fry the chicken pieces in small batches until golden and crispy.",
      "Serve hot with mint chutney or ketchup."
    ],
    "url": "https://www.youtube.com/watch?v=chickenpakoda123"
},
}

def insert_mock_data():
    """Insert mock recipe data into the database."""
    db = connect_to_db()
    if db is None:
        return

    cursor = db.cursor()

    # Loop through mock data and insert it into the database
    for name, details in mock_recipes.items():
        # Convert the list of ingredients and steps into strings
        ingredients = ", ".join(details["ingredients"])  # Convert list to a comma-separated string
        description = details["description"]
        steps = "; ".join(details["steps"])  # Convert list to a semicolon-separated string
        url = details.get("url", None)

        query = """
        INSERT INTO recipe (name, ingredients, description, steps, url)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        ingredients = VALUES(ingredients),
        description = VALUES(description),
        steps = VALUES(steps),
        url = VALUES(url)
        """
        values = (name, ingredients, description, steps, url)

        try:
            cursor.execute(query, values)
            print(f"Inserted/Updated recipe: {name}")
        except mysql.connector.Error as err:
            print(f"Error with recipe {name}: {err}")

    # Commit changes to the database
    try:
        db.commit()
        print("All mock data processed successfully!")
    except mysql.connector.Error as err:
        print(f"Error committing changes: {err}")

    # Close the database connection
    cursor.close()
    db.close()
    print("Database connection closed.")

# Call the function to insert/update mock data
if __name__ == "__main__":
    insert_mock_data()
