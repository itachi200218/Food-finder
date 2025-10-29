import React, { useState, useEffect } from "react";

function RecipeForm({ selectedRecipe, onRecipeSaved }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    ingredients: "",
    steps: "",
    url: "",
  });

  useEffect(() => {
    if (selectedRecipe) {
      setFormData(selectedRecipe);
    } else {
      setFormData({
        name: "",
        description: "",
        ingredients: "",
        steps: "",
        url: "",
      });
    }
  }, [selectedRecipe]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onRecipeSaved(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
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
      <button type="submit">Save Recipe</button>
    </form>
  );
}

export default RecipeForm;
