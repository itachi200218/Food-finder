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


// Store the page for fetching the recipes based on category
// Initialize current page for each category and store past recipes
let currentPages = {};
let pastRecipes = {};

// Function to fetch recipes for a specific category
function fetchCategoryRecipes(categoryId, categoryName) {
    const categoryList = document.getElementById(categoryId);

    if (!currentPages[categoryName]) currentPages[categoryName] = 1;
    if (!pastRecipes[categoryName]) pastRecipes[categoryName] = [];

    fetch(`/get-recipes?category=${categoryName}&page=${currentPages[categoryName]}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                pastRecipes[categoryName].push(...data);

                data.forEach(recipe => {
                    const li = document.createElement('li');
                    li.classList.add('recipe-item');
                    li.setAttribute('data-id', recipe.id);

                    li.innerHTML = `
                        <div class="recipe-link">
                            <i class="fas fa-utensils"></i> <span class="recipe-name">${recipe.name}</span>
                            <div class="recipe-description">
                                <p><strong>Description:</strong> ${recipe.description}</p>
                            </div>
                        </div>
                    `;

                    categoryList.appendChild(li);
                });

                // Attach click event to each new recipe item (icon, name, and description)
                document.querySelectorAll('.recipe-item').forEach(item => {
                    item.addEventListener('click', (e) => {
                        e.preventDefault();
                        const recipeId = item.getAttribute('data-id');
                        showRecipeDetail(recipeId);
                    });
                });

                currentPages[categoryName]++;
            } else {
                console.log(`No more recipes found for ${categoryName}.`);
            }
        })
        .catch(error => console.error(`Error fetching recipes for ${categoryName}:`, error));
}

// Function to fetch full recipe details by recipe ID and display them
function showRecipeDetail(recipeId) {
    if (!recipeId) {
        console.error('Invalid recipe ID:', recipeId);
        return;
    }

    console.log(`Fetching details for recipe ID: ${recipeId}`);
    fetch(`/get-recipe-detail?id=${recipeId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            displayRecipeDetails(data);
        })
        .catch(error => {
            console.error('Error fetching recipe details:', error);
            document.getElementById("recipe-details").innerHTML = `<p>Failed to load recipe details. Please try again later.</p>`;
        });
}


// Function to display the recipe details in the main section
function displayRecipeDetails(data) {
    const recipeDetailsContainer = document.getElementById("recipe-details");

    const videoEmbed = data.url ? `
        <h3>Watch the recipe video:</h3>
        <div class="video-container">
            <iframe width="560" height="315" 
                src="https://www.youtube.com/embed/${extractYouTubeId(data.url)}" 
                frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
        </div>` : '';

    recipeDetailsContainer.innerHTML = `
        <h1>${data.name}</h1>
        <h2>Description:</h2>
        <p>${data.description}</p>
        <h2>Ingredients:</h2>
        <ul>${data.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}</ul>
        <h2>Steps:</h2>
        <ol>${data.steps.map(step => `<li>${step}</li>`).join('')}</ol>
        ${videoEmbed}
    `;
}

// Helper function to extract YouTube video ID from URL
function extractYouTubeId(url) {
    const match = url.match(/(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|\.be\/)([a-zA-Z0-9_-]{11})/);
    return match ? match[1] : '';
}


// Function to toggle expand/collapse for a category and add infinite scrolling
function toggleCategory(categoryId, categoryName) {
    const categoryDiv = document.getElementById(categoryId);
    const button = document.querySelector(`button[onclick="toggleCategory('${categoryId}', '${categoryName}')"]`);
    const sidebar = document.querySelector('.sidebar');  // To control sidebar
    const isExpanded = categoryDiv.style.display === "block";

    // Apply styles for the expand/collapse button
    button.classList.add("expand-btn");

    // Add or remove category background color
    if (isExpanded) {
        categoryDiv.style.display = "none"; // Collapse
        categoryDiv.classList.remove("category-expanded"); // Remove expanded background
        categoryDiv.classList.add("category-collapsed"); // Set collapsed background
        button.textContent = `Expand ${categoryName}`;
    } else {
        categoryDiv.style.display = "block"; // Expand
        categoryDiv.classList.remove("category-collapsed"); // Remove collapsed background
        categoryDiv.classList.add("category-expanded"); // Set expanded background
        button.textContent = `Collapse ${categoryName}`;

        if (!categoryDiv.hasAttribute('data-loaded')) {
            fetchCategoryRecipes(categoryId, categoryName); // Initial fetch
            categoryDiv.setAttribute('data-loaded', 'true');
        }

        // Add scroll listener for infinite scroll
        categoryDiv.addEventListener('scroll', function () {
            if (categoryDiv.scrollTop + categoryDiv.clientHeight >= categoryDiv.scrollHeight - 50) {
                console.log(`Fetching more recipes for ${categoryName}`);
                fetchCategoryRecipes(categoryId, categoryName);
            }
        });
    }

    // Expanding Sidebar Logic
    if (!isExpanded) {
        sidebar.classList.add('expanded');  // Expand the sidebar
    } else {
        sidebar.classList.remove('expanded');  // Collapse the sidebar
    }
}


// To handle the infinite scrolling when the sidebar is scrolled
document.querySelector('.sidebar').addEventListener('scroll', function() {
    const sidebar = document.querySelector('.sidebar');
    const categoryContainers = sidebar.querySelectorAll('.category-container');
    const lastCategory = categoryContainers[categoryContainers.length - 1];

    // Check if the sidebar has reached the bottom
    if (sidebar.scrollTop + sidebar.clientHeight >= sidebar.scrollHeight - 10) {
        console.log("Reached the bottom of the sidebar, scroll to next category.");
        scrollToNextCategory();  // Scroll to the next category in the sidebar
    }
});
function toggleCategories() {
    const categoriesContainer = document.getElementById('categories-container');
    if (categoriesContainer.style.display === 'none' || categoriesContainer.style.display === '') {
        categoriesContainer.style.display = 'block';  // Show categories
    } else {
        categoriesContainer.style.display = 'none';  // Hide categories
    }
}
// Event listener for handling search input and showing suggestions
document.getElementById("recipe-input").addEventListener("input", showSuggestions);

async function showSuggestions() {
    const input = document.getElementById("recipe-input").value.trim();
    const suggestionsContainer = document.getElementById("suggestionsContainer");

    if (input.length < 2) {
        suggestionsContainer.innerHTML = ""; // Clear suggestions if input is too short
        return;
    }

    try {
        const response = await fetch(`/get-recipes?category=${input}`);
        const suggestions = await response.json();

        if (suggestions.length > 0) {
            suggestionsContainer.innerHTML = suggestions
                .map(recipe => `<div class="suggestion-item" data-recipe-id="${recipe.id}">${recipe.name}</div>`)
                .join("");

            suggestionsContainer.addEventListener("click", function (event) {
                if (event.target.classList.contains("suggestion-item")) {
                    const recipeId = event.target.getAttribute("data-recipe-id");
                    fetchRecipeDetail(recipeId);
                }
            });

        } else {
            suggestionsContainer.innerHTML = "<p>No recipes found.</p>";
        }
    } catch (error) {
        console.error("Error fetching suggestions:", error);
        suggestionsContainer.innerHTML = "<p>Error fetching suggestions.</p>";
    }
}

async function fetchRecipeDetail(recipeId) {
    const recipeDetailsContainer = document.getElementById("recipe-details");

    try {
        const response = await fetch(`/get-recipe-detail?id=${encodeURIComponent(recipeId)}`);
        const recipe = await response.json();

        if (recipe.error) {
            recipeDetailsContainer.innerHTML = `<p>${recipe.error}</p>`;
        } else {
            displayRecipeDetails(recipe);
        }
    } catch (error) {
        console.error("Error fetching recipe details:", error);
        recipeDetailsContainer.innerHTML = "<p>Error fetching recipe details.</p>";
    }
}
