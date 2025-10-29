import React, { useState, useEffect } from "react";
import './RecipeForm.css';
import './App.css';

function RecipeForm() {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    ingredients: "",
    steps: "",
    url: "",
    category_id: "",
    index: "",
  });

  const [recipes, setRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchRecipes();
  }, []);

  const fetchRecipes = async (category="", name="") => {
    try {
      let url = "http://localhost:5000/recipes";
      const params = new URLSearchParams();
      if (category) params.append("category_id", category);
      if (name) params.append("name", name);
      if (params.toString()) url += "?" + params.toString();

      const response = await fetch(url);
      const data = await response.json();
      setRecipes(data);
    } catch (error) {
      console.error("Failed to fetch recipes:", error);
    }
  };

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });
  const handleSearch = (e) => setSearchTerm(e.target.value);

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

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dataToSend),
      });

      const responseData = await response.json();

      if (!response.ok) {
        alert(`Error: ${responseData.error || "Failed to save the recipe"}`);
      } else {
        alert(selectedRecipe ? "Recipe updated successfully!" : "Recipe added successfully!");
        setFormData({ name: "", description: "", ingredients: "", steps: "", url: "", category_id: "", index: "" });
        setSelectedRecipe(null);
        fetchRecipes();
      }
    } catch (error) {
      console.error("Error saving recipe:", error);
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
    if (!window.confirm("Are you sure you want to delete this recipe?")) return;
    try {
      const response = await fetch(`http://localhost:5000/recipes/${id}`, { method: 'DELETE' });
      if (response.ok) {
        alert("Recipe deleted successfully!");
        fetchRecipes();
      } else {
        alert("Failed to delete the recipe.");
      }
    } catch (error) {
      console.error("Delete failed:", error);
    }
  };

  // Filter recipes by searchTerm locally
  const filteredRecipes = recipes.filter(recipe => {
    const searchValue = searchTerm.trim().toLowerCase();
    if (!searchValue) return true;
    if (!isNaN(searchValue)) return recipe.category_id.toString() === searchValue;
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
          onChange={handleSearch}
        />
        <button className="search-btn" onClick={() => fetchRecipes()}>Search</button>
      </div>

      <div className="form-container">
        <aside className="category-sidebar">
          <h3 className="sidebar-title">Category ID Guide</h3>
          <ul className="category-list">
            {[ 
              { id: "1", name: "Veg" }, 
              { id: "2", name: "Non-Veg" }, 
              { id: "3", name: "Seafood" }, 
              { id: "4", name: "Street Food" }, 
              { id: "5", name: "Tiffins" } 
            ].map((cat) => (
              <li key={cat.id} onClick={() => setSearchTerm(cat.id)} className="category-item">
                {cat.id} - {cat.name}
              </li>
            ))}
          </ul>
        </aside>

        <form onSubmit={handleSubmit} className="recipe-form">
          <input type="text" name="name" placeholder="Recipe Name" value={formData.name} onChange={handleChange} required />
          <textarea name="description" placeholder="Description" value={formData.description} onChange={handleChange} required />
          <textarea name="ingredients" placeholder="Ingredients" value={formData.ingredients} onChange={handleChange} required />
          <textarea name="steps" placeholder="Steps" value={formData.steps} onChange={handleChange} />
          <input type="text" name="url" placeholder="Image URL (optional)" value={formData.url} onChange={handleChange} />
          <input type="number" name="category_id" placeholder="Category ID" value={formData.category_id} onChange={handleChange} required />
          <input type="number" name="index" placeholder="Recipe Index (optional)" value={formData.index} onChange={handleChange} />
          <button type="submit" className="submit-btn">{selectedRecipe ? "Update Recipe" : "Add Recipe"}</button>
        </form>
      </div>

      <h3 className="form-title">Recipe List</h3>
      <ul className="recipe-list">
        {filteredRecipes.length > 0 ? filteredRecipes.map((recipe, i) => (
          <li key={recipe.id} className="recipe-item">
            <h4>{recipe.name}</h4>
            <p>Index: {i + 1}</p>
            <p>Category ID: {recipe.category_id}</p>
            <button onClick={() => handleEdit(recipe)} className="edit-btn">Edit</button>
            <button onClick={() => handleDelete(recipe.id)} className="delete-btn">Delete</button>
          </li>
        )) : <p>No recipes found</p>}
      </ul>
    </div>
  );
}

export default RecipeForm;
