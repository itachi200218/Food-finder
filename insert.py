from app import create_app
from extensions import db
from models import Recipe, Category
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Data for Recipes
mock_recipes = {
    "Chicken Pakoda": {
        "ingredients": "Chicken, Gram Flour, Rice Flour, Ginger-Garlic Paste, Red Chili Powder, Turmeric, Coriander Powder, Garam Masala, Salt, Curry Leaves, Green Chilies, Oil for Frying",
        "description": "A crispy and spicy Indian snack made with marinated chicken, coated in a flavorful batter and deep-fried to golden perfection.",
        "steps": "Cut chicken into bite-sized pieces and marinate with ginger-garlic paste, turmeric, red chili powder, coriander powder, garam masala, and salt. Let it rest for 30 minutes.; In a bowl, mix gram flour, rice flour, and a pinch of salt. Add curry leaves and chopped green chilies.; Add the marinated chicken to the flour mixture and coat well. Sprinkle water if needed to make the coating stick.; Heat oil in a deep pan. Fry the chicken pieces in small batches until golden and crispy.; Serve hot with mint chutney or ketchup.",
        "url": "https://www.youtube.com/watch?v=chickenpakoda123",
        "category": "Snacks"
    },
    # You can add more recipes here
}

def insert_mock_data():
    """Insert or update mock recipe data into the database using SQLAlchemy."""
    app = create_app()
    with app.app_context():
        # Ensure tables are created
        db.create_all()
        logger.info("Database tables checked/created.")

        # Loop through mock data and insert/update it into the database
        for name, details in mock_recipes.items():
            try:
                # --- Category Handling ---
                category_name = details.get("category")
                category = None
                if category_name:
                    # Check if category exists
                    category = Category.query.filter_by(name=category_name).first()
                    if not category:
                        # If not, create it
                        category = Category(name=category_name)
                        db.session.add(category)
                        # We don't need to flush here, SQLAlchemy handles relationships
                        logger.info(f"Creating new category: {category_name}")

                # --- Recipe Handling (Upsert) ---
                # Check if recipe exists
                recipe = Recipe.query.filter_by(name=name).first()

                if recipe:
                    # Update existing recipe
                    logger.info(f"Updating existing recipe: {name}")
                    recipe.description = details["description"]
                    recipe.ingredients = details["ingredients"]
                    recipe.steps = details["steps"]
                    recipe.url = details.get("url")
                    recipe.category = category
                else:
                    # Create new recipe
                    logger.info(f"Inserting new recipe: {name}")
                    recipe = Recipe(
                        name=name,
                        description=details["description"],
                        ingredients=details["ingredients"],
                        steps=details["steps"],
                        url=details.get("url"),
                        category=category
                    )
                    db.session.add(recipe)

            except Exception as e:
                logger.error(f"Error processing recipe '{name}': {e}")
                db.session.rollback() # Rollback on error for this item
                continue # Continue to the next recipe

        # Commit all changes to the database
        try:
            db.session.commit()
            logger.info("All mock data processed and committed successfully!")
        except Exception as e:
            logger.error(f"Error committing changes to the database: {e}")
            db.session.rollback()

    logger.info("Script finished.")

# Call the function to insert/update mock data
if __name__ == "__main__":
    insert_mock_data()
