// Event listener for form submission (recipe search by keyword)
document.getElementById("recipe-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const userInput = document.getElementById("recipe-input").value;
    fetchRecipeDetails(userInput)
        .then(data => displayRecipeDetails(data))
        .catch(() => {
            document.getElementById("recipe-details").innerHTML = `<p>Something went wrong. Please try again.</p>`;
        });
});

// Event listeners for sidebar clicks
const sidebarItems = document.querySelectorAll(".sidebar ul li");
sidebarItems.forEach(item => {
    item.addEventListener("click", function () {
        const recipeName = item.textContent.trim();
        fetchRecipeDetails(recipeName)
            .then(data => displayRecipeDetails(data))
            .catch(() => {
                document.getElementById("recipe-details").innerHTML = `<p>Something went wrong. Please try again.</p>`;
            });
    });
});

// Function to display recipe details
function displayRecipeDetails(data) {
    console.log(data);  // Debug: log the incoming data to verify its structure

    const recipeDetails = document.getElementById("recipe-details");
    if (data.error) {
        recipeDetails.innerHTML = `<p>${data.error}</p>`;
    } else {
        // Extract the YouTube video ID if the URL is valid
        const videoEmbed = data.url ? `
            <h3>Watch the recipe video:</h3>
            <div class="video-container">
                <iframe width="560" height="315" 
                    src="https://www.youtube.com/embed/${extractYouTubeId(data.url)}" 
                    frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
                </iframe>
            </div>
        ` : '';

        // Display both the description, ingredients, and video
        recipeDetails.innerHTML = `
            <h2>Description:</h2>
            <p>${data.description}</p>
            <h2>Ingredients:</h2>
            <ul>
                ${data.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
            </ul>
            <h2>Steps:</h2>
            <ol>
                ${data.steps.map(step => `<li>${step}</li>`).join('')}
            </ol>
            ${videoEmbed}
        `;
    }
}

// Helper function to extract YouTube video ID from URL
function extractYouTubeId(url) {
    // Regex for extracting YouTube video ID for both regular videos and shorts
    const regex = /(?:https?:\/\/(?:www\.)?youtube\.com\/(?:v\/|e(?:mbed)?\/|\S*?[?&]v=)|(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}



    // Function to display the matching recipes based on ingredients search
    function displayRecipeResults(recipes) {
        const resultsContainer = document.getElementById("recipe-results");

        if (recipes.length === 0) {
            resultsContainer.innerHTML = `<p>No recipes found matching your ingredients.</p>`;
        } else {
            resultsContainer.innerHTML = recipes.map(recipe => {
                // Ensure data is available for name, description, ingredients, and steps
                const name = recipe.name || 'Recipe name not available';
                const description = recipe.description || 'Description not available';
                const ingredients = recipe.ingredients && recipe.ingredients.length > 0
                    ? recipe.ingredients.join(', ')
                    : 'No ingredients available';
                const steps = recipe.steps && recipe.steps.length > 0
                    ? recipe.steps.join(' | ')  // Join steps with a separator for display
                    : 'No steps available';

                return `
                    <div class="recipe-card">
                        <h3>${name}</h3>
                        <p>${description}</p>
                        <p><strong>Ingredients:</strong> ${ingredients}</p>
                        <p><strong>Steps:</strong> ${steps}</p>  <!-- Added steps here -->
                        <a href="#" onclick="displayRecipeDetails(${JSON.stringify(recipe)})">View Recipe</a>
                    </div>
                `;
            }).join('');
        }
    }

    // Function to handle the form submission
    function searchRecipe(event) {
        event.preventDefault();  // Prevent page reload
        const userInput = document.getElementById("recipe-input").value;
        
        // Send the search input to the backend
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Display suggestions from the response
            displaySuggestions(data.suggestions);
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to display multiple recipe suggestions
    function displaySuggestions(suggestions) {
        const container = document.getElementById("suggestionsContainer");
        container.innerHTML = '';  // Clear previous suggestions

        if (suggestions && suggestions.length > 0) {
            suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement("div");
                suggestionItem.classList.add("suggestion");
                suggestionItem.innerHTML = `<p>${suggestion.name}</p>`;

                // When a suggestion is clicked, display recipe details
                suggestionItem.addEventListener("click", function() {
                    displayRecipeDetails(suggestion);
                });

                container.appendChild(suggestionItem);
            });
        } else {
            container.innerHTML = '<p>No suggestions found.</p>';
        }
    }
// Function to display recipe details
function displayRecipeDetails(recipe) {
    const detailsContainer = document.getElementById("recipe-details");
    detailsContainer.innerHTML = `
        <h2>${recipe.name}</h2>
        <h3>Ingredients:</h3>
        <ul>
            ${recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
        </ul>
        <h3>Description:</h3>
        <p>${recipe.description}</p>
        <h3>Steps:</h3>
        <ol>
            ${recipe.steps.map(step => `<li>${step}</li>`).join('')}
        </ol>
        <a href="${recipe.url}" target="_blank">Recipe Link</a>
    `;
}
// Attach the searchRecipe function to the form submission
document.getElementById("recipe-form").addEventListener("submit", searchRecipe);
let currentPage = 1; // Track current page for pagination
let maxRecipes = 5;  // Max number of recipes per page

function toggleExploreMore(categoryId, categoryName) {
    const categoryList = document.getElementById(categoryId);
    const exploreButton = document.querySelector(`#${categoryId} + .sidebar-button`);
    const sidebar = document.querySelector('.sidebar');

    if (exploreButton.innerText === "Explore More") {
        // Expand sidebar
        sidebar.classList.add('expanded');

        // Fetch 5 recipes per page based on currentPage
        fetch(`/get-recipes?category=${categoryName}&page=${currentPage}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    data.forEach(recipe => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <a href="${recipe.url}" target="_blank" class="recipe-title">
                                <i class="fas fa-utensils"></i> ${recipe.name}
                            </a>
                            <div class="recipe-description">
                                <p><strong>Description:</strong> ${recipe.description}</p>
                            </div>
                            <div class="recipe-ingredients">
                                <p><strong>Ingredients:</strong> ${recipe.ingredients}</p>
                            </div>
                            <div class="recipe-steps">
                                <p><strong>Steps:</strong> ${recipe.steps}</p>
                            </div>
                            <div class="recipe-more-info">
                                <p><strong>More Info:</strong> <a href="${recipe.url}" target="_blank">Visit Recipe Page</a></p>
                            </div>
                        `;
                        categoryList.appendChild(li);
                    });

                    // Ensure sidebar scrolls to the bottom to show newly added recipes
                    sidebar.scrollTop = sidebar.scrollHeight;

                    // Update button text and increase the page number
                    exploreButton.innerText = "Show Less";
                    currentPage++;
                } else {
                    alert("No more recipes available.");
                }
            })
            .catch(error => {
                console.error('Error fetching recipes:', error);
            });
    } else {
        // Collapse the category list and hide extra recipes
        collapseCategoryList(categoryList);
        exploreButton.innerText = "Explore More";
        sidebar.classList.remove('expanded');
        sidebar.scrollTop = 0; // Reset scroll position
    }
}

function collapseCategoryList(categoryList) {
    const allRecipes = categoryList.getElementsByTagName('li');
    // Remove all recipes except the first 5
    while (allRecipes.length > maxRecipes) {
        categoryList.removeChild(allRecipes[allRecipes.length - 1]);
    }
}
