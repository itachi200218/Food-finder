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
document.addEventListener("DOMContentLoaded", function () {
    const exploreButton = document.querySelector(".sidebar-button");
    const exploreRecipesSection = document.getElementById("explore-recipes");
    const exploreRecipesList = document.getElementById("explore-recipes-list");
    const hideRecipesButton = document.getElementById("hide-recipes-button");

    // Initially hide the Explore Recipes section and the Hide Recipes button
    exploreRecipesSection.style.display = "none";
    hideRecipesButton.style.display = "none";

    // Variable to track the current page (if pagination is implemented on the backend)
    let currentPage = 1;

    // Function to load more recipes
    exploreButton.addEventListener("click", function () {
        // Show the section and the hide button
        exploreRecipesSection.style.display = "block";
        hideRecipesButton.style.display = "inline-block"; // Show the Hide button
        fetchRecipes(currentPage); // Pass current page to fetch new recipes
    });

    // Function to hide the Explore Recipes section
    hideRecipesButton.addEventListener("click", function () {
        exploreRecipesSection.style.display = "none";
        hideRecipesButton.style.display = "none"; // Hide the button too
    });

    // Fetch recipes from the backend
    async function fetchRecipes(page) {
        try {
            const response = await fetch(`/get-recipes?page=${page}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch recipes');
            }

            const recipes = await response.json();
            displayRecipes(recipes);

            // Increment page number for the next load
            currentPage++;
        } catch (error) {
            console.error("Error fetching recipes:", error);
        }
    }

    // Function to display the fetched recipes in the "Explore More" section
    function displayRecipes(recipes) {
        // Add each new recipe to the list (without clearing the existing ones)
        recipes.forEach(recipe => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <i class="${recipe.icon}"></i> ${recipe.name}
            `;
            listItem.addEventListener("click", function () {
                getRecipeDetails(recipe.name);  // Fetch the full details when clicked
            });
            exploreRecipesList.appendChild(listItem);
        });
    }

    // Fetch and display details for the clicked recipe
    async function getRecipeDetails(recipeName) {
        try {
            const response = await fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    prompt: recipeName,
                }),
            });

            const recipeDetails = await response.json();

            if (recipeDetails.error) {
                alert(recipeDetails.error);
                return;
            }

            // Update the recipe details section with the received data
            const recipeDetailsSection = document.getElementById("recipe-details");
            recipeDetailsSection.innerHTML = `
                <h3>${recipeDetails.name}</h3>
                <p>${recipeDetails.description}</p>
                <h4>Ingredients:</h4>
                <ul>
                    ${recipeDetails.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
                </ul>
                <h4>Steps:</h4>
                <ol>
                    ${recipeDetails.steps.map(step => `<li>${step}</li>`).join('')}
                </ol>
                <a href="${recipeDetails.url}" target="_blank">Full Recipe</a>
            `;
        } catch (error) {
            console.error("Error fetching recipe details:", error);
        }
    }
});
