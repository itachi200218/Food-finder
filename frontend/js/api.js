// Function to fetch recipe details from the backend
function fetchRecipeDetails(recipeName) {
    return fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: recipeName })
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error fetching recipe details:', error);
        throw error; // Rethrow to handle it in the calling function
    });
}

// Function to load more recipes from the backend
function loadMoreRecipes() {
    return fetch('/get-recipes')
        .then(response => response.json())
        .catch(error => {
            console.error('Error fetching recipes:', error);
            throw error;
        });
}
