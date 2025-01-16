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

// Event listener for the Explore More button
let isLoading = false; // To prevent multiple clicks before loading
document.querySelector('.sidebar-button').addEventListener('click', function() {
    if (isLoading) return; // Prevent multiple requests at the same time
    isLoading = true;
    loadMoreRecipes()
        .then(recipes => {
            // Get the sidebar list where recipes are displayed
            const sidebar = document.querySelector('.sidebar ul');

            // Find the non-veg section (assuming it's the second list)
            const nonVegSection = sidebar.children[1];

            // Loop through new recipes and append them after the non-veg section
            recipes.forEach(recipe => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<i class="${recipe.icon}"></i> ${recipe.name}`;

                // Add a click event to fetch and display recipe details when clicked
                listItem.addEventListener('click', function() {
                    fetchRecipeDetails(recipe.name)
                        .then(data => displayRecipeDetails(data))
                        .catch(() => {
                            document.getElementById("recipe-details").innerHTML = `<p>Something went wrong. Please try again.</p>`;
                        });
                });

                // Add the 'extra-recipes' class for the black background styling
                listItem.classList.add('extra-recipes'); // Apply the black background class

                // Insert the new recipe after the non-veg section
                nonVegSection.after(listItem);
            });

            // Set loading state to false after the recipes are loaded
            isLoading = false;
        })
        .catch(() => {
            console.error('Error fetching recipes');
            isLoading = false; // Reset loading state in case of error
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
document.querySelector('.sidebar-button').addEventListener('click', function() {
    const menu = document.querySelector('.menu');
    menu.classList.toggle('expanded'); // Toggle expanded state

    const extraRecipesContainer = document.querySelector('.extra-recipes-container');
    extraRecipesContainer.classList.toggle('expanded'); // Toggle expanded state for extra recipes

    // Optionally, change button text or styling for the expanded state
    const button = document.querySelector('.explore-more');
    button.innerText = menu.classList.contains('expanded') ? 'Show Less' : 'Explore More';
});