const fetchRecipes = async () => {
  try {
    const response = await axios.get(`${process.env.REACT_APP_API_URL}/recipes`);
    setRecipes(response.data);
  } catch (error) {
    console.error("Error fetching recipes:", error);
  }
};

const handleRecipeSaved = async (recipeData) => {
  try {
    if (selectedRecipe) {
      const response = await axios.put(`${process.env.REACT_APP_API_URL}/recipes/${selectedRecipe.id}`, recipeData);
      setRecipes((prevRecipes) =>
        prevRecipes.map((recipe) =>
          recipe.id === selectedRecipe.id ? response.data.recipe : recipe
        )
      );
    } else {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/recipes`, recipeData);
      setRecipes((prevRecipes) => [...prevRecipes, response.data.recipe]);
    }
    setSelectedRecipe(null);
  } catch (error) {
    console.error("Error saving recipe:", error);
  }
};

const handleDelete = async (id) => {
  try {
    await axios.delete(`${process.env.REACT_APP_API_URL}/recipes/${id}`);
    setRecipes((prevRecipes) => prevRecipes.filter((recipe) => recipe.id !== id));
  } catch (error) {
    console.error("Error deleting recipe:", error);
  }
};
