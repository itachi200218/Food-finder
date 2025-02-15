import React from "react";

function RecipeList({ recipes, onEdit, onDelete }) {
  return (
    <div>
      <h2>Recipe List</h2>
      <ul>
        {recipes.map((recipe) => (
          <li key={recipe.id}>
            <h3>{recipe.name}</h3>
            <p>{recipe.description}</p>
            <button onClick={() => onEdit(recipe)}>Edit</button>
            <button onClick={() => onDelete(recipe.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RecipeList;
