import React, { useState, useEffect } from "react";
import './RecipeForm.css'; // Import the CSS for styling
import './App.css';

function RecipeForm() {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    ingredients: "",
    steps: "",
    url: "",
    category_id: "",
    index: "", // New field for the index (optional)
  });

  const [recipes, setRecipes] = useState([]); // State to store the list of recipes
  const [selectedRecipe, setSelectedRecipe] = useState(null); // State for editing
  const [searchTerm, setSearchTerm] = useState(""); // State for search input

  useEffect(() => {
    fetchRecipes(); // Fetch recipes when the component mounts
  }, []);

  const fetchRecipes = async () => {
    try {
      const response = await fetch('http://localhost:5000/recipes');
      const data = await response.json();
      setRecipes(data);
    } catch (error) {
      console.error("Failed to fetch recipes:", error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  
  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const method = selectedRecipe ? 'PUT' : 'POST';
      const url = selectedRecipe
        ? `http://localhost:5000/recipes/${selectedRecipe.id}`
        : 'http://localhost:5000/recipes';
  
      const dataToSend = {
        ...formData,
        index: formData.index !== "" ? parseInt(formData.index, 10) : undefined,
      };
  
      console.log("Method:", method);
      console.log("URL:", url);
      console.log("Data to Send:", dataToSend);
  
      const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dataToSend),
      });
  
      const responseData = await response.json();
  
      if (!response.ok) {
        console.error("Error:", responseData);
        alert(`Error: ${responseData.error || "Failed to save the recipe"}`);
      } else {
        alert(selectedRecipe ? "Recipe updated successfully!" : "Recipe added successfully!");
        setFormData({ name: "", description: "", ingredients: "", steps: "", url: "", category_id: "", index: "" });
        setSelectedRecipe(null);
        fetchRecipes();
      }
    } catch (error) {
      console.error("An error occurred while saving the recipe:", error);
      alert("An error occurred. Please try again.");
    }
  };
  
  const handleEdit = (recipe) => {
    setFormData({
      name: recipe.name || "",
      description: recipe.description || "",
      ingredients: recipe.ingredients || "",
      steps: recipe.steps || "",
      url: recipe.url || "",
      category_id: recipe.category_id || "",
      index: recipe.index || "",
    });
    setSelectedRecipe(recipe);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this recipe?")) {
      try {
        const response = await fetch(`http://localhost:5000/recipes/${id}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          alert("Recipe deleted successfully!");
          fetchRecipes();
        } else {
          alert("Failed to delete the recipe.");
        }
      } catch (error) {
        console.error("Failed to delete recipe:", error);
      }
    }
  };

  const filteredRecipes = recipes.filter(recipe => {
    const searchValue = searchTerm.trim().toLowerCase();
  
    if (!searchValue) return true; // If no search input, show all recipes
  
    // Check if search term is a number (category ID)
    if (!isNaN(searchValue)) {
      return recipe.category_id.toString() === searchValue;
    }
  
    // Otherwise, filter by recipe name
    return recipe.name.toLowerCase().includes(searchValue);
  });
  

    return (
      <div className="recipe-form-container">
        <h2 className="form-title">{selectedRecipe ? "Edit Recipe" : "Add Recipe"}</h2>
        
        <div className="search-container">
          <input
            type="text"
            className="search-input"
            placeholder="Search recipes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button className="search-btn" onClick={fetchRecipes}>Search</button>
        </div>
  
        {/* Flex container for Sidebar & Form */}
        <div className="form-container">
          {/* Sidebar for Category Guide - Always on the left */}
          <aside className="category-sidebar">
            <h3 className="sidebar-title">Category ID Guide</h3>
            <ul className="category-list">
              {[ 
                { id: "1", name: "Veg" }, 
                { id: "2", name: "Non-Veg" }, 
                { id: "3", name: "Seafood" }, 
                { id: "4", name: "Street Food" }, 
                { id: "5", name: "Tiffins" } 
              ].map((category) => (
                <li 
                  key={category.id} 
                  onClick={() => setSearchTerm(category.id)} 
                  className="category-item"
                >
                  {category.id} - {category.name}
                </li>
              ))}
            </ul>
          </aside>
  
          {/* Recipe Form */}
          <form onSubmit={handleSubmit} className="recipe-form">
            <input
              type="text"
              name="name"
              placeholder="Recipe Name"
              value={formData.name}
              onChange={handleChange}
              required
            />
            <textarea
              name="description"
              placeholder="Description"
              value={formData.description}
              onChange={handleChange}
              required
            />
            <textarea
              name="ingredients"
              placeholder="Ingredients"
              value={formData.ingredients}
              onChange={handleChange}
              required
            />
            <textarea
              name="steps"
              placeholder="Steps"
              value={formData.steps}
              onChange={handleChange}
            />
            <input
              type="text"
              name="url"
              placeholder="Image URL (optional)"
              value={formData.url}
              onChange={handleChange}
            />
            <input
              type="number"
              name="category_id"
              placeholder="Category ID (refer to the guide)"
              value={formData.category_id}
              onChange={handleChange}
              required
            />
            <input
              type="number"
              name="index"
              placeholder="Recipe Index (optional)"
              value={formData.index}
              onChange={handleChange}
            />
            <button type="submit" className="submit-btn">
              {selectedRecipe ? "Update Recipe" : "Add Recipe"}
            </button>
          </form>
        </div>
  
        {/* Recipe List */}
        <h3 className="form-title">Recipe List</h3>
        <ul className="recipe-list">
          {filteredRecipes.length > 0 ? (
            filteredRecipes.map((recipe, i) => (
              <li key={recipe.id} className="recipe-item">
                <h4>{recipe.name}</h4>
                <p>Index: {i + 1}</p>
                <p>Category ID: {recipe.category_id}</p>
                <button onClick={() => handleEdit(recipe)} className="edit-btn">Edit</button>
                <button onClick={() => handleDelete(recipe.id)} className="delete-btn">Delete</button>
              </li>
            ))
          ) : (
            <p>No recipes found</p>
          )}
        </ul>
      </div>
    );
  };
  
  export default RecipeForm;
  