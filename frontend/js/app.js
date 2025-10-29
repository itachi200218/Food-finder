// ===============================
// ✅ Unified Form Submission: DB → AI fallback
// ===============================
document.getElementById("recipe-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const userInput = document.getElementById("recipe-input").value.trim();
    const recipeDetailsContainer = document.getElementById("recipe-details");
    const suggestionsContainer = document.getElementById("suggestionsContainer");
    const aiStatus = document.getElementById("ai-status"); // 👈 added

    if (!userInput) {
        recipeDetailsContainer.innerHTML = "<p>Please enter a recipe name.</p>";
        return;
    }

    recipeDetailsContainer.innerHTML = "<p>Loading...</p>";
    suggestionsContainer.innerHTML = "";

    // 👇 Show AI status indicator before searching
    aiStatus.style.display = "block";
    aiStatus.textContent = "🤖 Searching with AI... please wait";

    try {
        // 🔹 1. Try to find recipe in Database
        const dbResponse = await fetch(`/get-recipes?category=${userInput}`);
        const dbData = await dbResponse.json();

        if (dbData && dbData.length > 0) {
            // Found in DB → display result
            aiStatus.style.display = "none"; // ✅ hide AI indicator
            displayRecipeDetails(dbData[0]);
            return;
        }

        // 🔹 2. If not found → use AI search
        console.log("Recipe not found in DB. Trying AI search...");
        aiStatus.textContent = "🤖 Not found in DB... Searching with AI...";

        const aiResponse = await fetch("/ai-search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: userInput })
        });
        const aiData = await aiResponse.json();

        if (aiData.recipes && aiData.recipes.length > 0) {
            window.latestAIRecipes = aiData.recipes;
            aiStatus.style.display = "none"; // ✅ hide when done
            displayRecipeDetails(aiData.recipes[0]);
        } else {
            aiStatus.style.display = "none";
            recipeDetailsContainer.innerHTML = "<p>No AI recipes found.</p>";
        }

    } catch (error) {
        console.error("AI search error:", error);
        aiStatus.style.display = "none";
        recipeDetailsContainer.innerHTML = "<p>Error fetching recipe details.</p>";
    }
});

// ===============================
// 🍴 Category Handling
// ===============================
let currentPages = {};
let pastRecipes = {};

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

function showRecipeDetail(recipeId) {
    if (!recipeId) {
        console.error('Invalid recipe ID:', recipeId);
        return;
    }

    console.log(`Fetching details for recipe ID: ${recipeId}`);
    fetch(`/get-recipe-detail?id=${recipeId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            displayRecipeDetails(data);
        })
        .catch(error => {
            console.error('Error fetching recipe details:', error);
            document.getElementById("recipe-details").innerHTML = `<p>Failed to load recipe details. Please try again later.</p>`;
        });
}

// ===============================
// ✅ Updated Display Function (Fixed for AI)
// ===============================
function displayRecipeDetails(data) {
    const recipeDetailsContainer = document.getElementById("recipe-details");

    if (!data) {
        recipeDetailsContainer.innerHTML = `<p>No recipe data available.</p>`;
        return;
    }

    console.log("Rendering recipe:", data); // Debug log

    const ingredients = Array.isArray(data.ingredients)
        ? data.ingredients.map(i =>
            typeof i === "string" ? i : (i.item || i.name || JSON.stringify(i))
        )
        : typeof data.ingredients === "string"
            ? data.ingredients.split(/[,.\n]/).map(i => i.trim()).filter(i => i)
            : [];

    const steps = Array.isArray(data.steps)
        ? data.steps.map(s =>
            typeof s === "string" ? s : (s.step || s.name || JSON.stringify(s))
        )
        : typeof data.steps === "string"
            ? data.steps.split(/[\n.]/).map(s => s.trim()).filter(s => s)
            : [];

    const videoEmbed = data.url ? `
        <h3>Watch the recipe video:</h3>
        <div class="video-container">
            <iframe width="560" height="315"
                src="https://www.youtube.com/embed/${extractYouTubeId(data.url)}"
                frameborder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
        </div>` : '';

    recipeDetailsContainer.innerHTML = `
        <h1>${data.name || "Recipe Details"}</h1>
        <h2>Description:</h2>
        <p>${data.description || "No description available."}</p>
        <h2>Ingredients:</h2>
        <ul>${ingredients.map(i => `<li>${i}</li>`).join('') || "<li>No ingredients listed.</li>"}</ul>
        <h2>Steps:</h2>
        <ol>${steps.map(s => `<li>${s}</li>`).join('') || "<li>No steps provided.</li>"}</ol>
        ${videoEmbed}
    `;
}

function extractYouTubeId(url) {
    const match = url.match(/(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|\.be\/)([a-zA-Z0-9_-]{11})/);
    return match ? match[1] : '';
}

// ===============================
// 📂 Sidebar & Infinite Scroll
// ===============================
function toggleCategory(categoryId, categoryName) {
    const categoryDiv = document.getElementById(categoryId);
    const button = document.querySelector(`button[onclick="toggleCategory('${categoryId}', '${categoryName}')"]`);
    const sidebar = document.querySelector('.sidebar');
    const isExpanded = categoryDiv.style.display === "block";

    button.classList.add("expand-btn");

    if (isExpanded) {
        categoryDiv.style.display = "none";
        categoryDiv.classList.remove("category");
        categoryDiv.classList.add("category-collapsed");
        button.textContent = `Expand ${categoryName}`;
    } else {
        categoryDiv.style.display = "block";
        categoryDiv.classList.remove("category-collapsed");
        categoryDiv.classList.add("category");
        button.textContent = `Collapse ${categoryName}`;

        if (!categoryDiv.hasAttribute('data-loaded')) {
            fetchCategoryRecipes(categoryId, categoryName);
            categoryDiv.setAttribute('data-loaded', 'true');
        }

        categoryDiv.addEventListener('scroll', function () {
            if (categoryDiv.scrollTop + categoryDiv.clientHeight >= categoryDiv.scrollHeight - 50) {
                console.log(`Fetching more recipes for ${categoryName}`);
                fetchCategoryRecipes(categoryId, categoryName);
            }
        });
    }

    if (!isExpanded) sidebar.classList.add('expanded');
    else sidebar.classList.remove('expanded');
}

document.querySelector('.sidebar').addEventListener('scroll', function () {
    const sidebar = document.querySelector('.sidebar');
    const categoryContainers = sidebar.querySelectorAll('.category-container');
    const lastCategory = categoryContainers[categoryContainers.length - 1];
    if (sidebar.scrollTop + sidebar.clientHeight >= sidebar.scrollHeight - 10) {
        console.log("Reached the bottom of the sidebar.");
    }
});

function toggleCategories() {
    const container = document.getElementById('categories-container');
    container.style.display = (container.style.display === 'none' || container.style.display === '') ? 'block' : 'none';
}

// ===============================
// 🔍 Suggestions (Improved with 5 AI suggestions + cache)
// ===============================
let aiRecipesCache = [];

document.getElementById("recipe-input").addEventListener("input", showSuggestions);
document.getElementById("suggestionsContainer").addEventListener("click", handleSuggestionClick);

async function showSuggestions() {
    const input = document.getElementById("recipe-input").value.trim();
    const suggestionsContainer = document.getElementById("suggestionsContainer");
    const aiStatus = document.getElementById("ai-status");

    if (input.length < 2) {
        suggestionsContainer.innerHTML = "";
        aiStatus.style.display = "none"; // hide when input is small
        return;
    }

    try {
        // 👇 Show “loading” status before searching
        aiStatus.style.display = "block";
        aiStatus.textContent = "🔎 Searching recipes...";

        const response = await fetch(`/get-recipes?category=${input}`);
        const suggestions = await response.json();

        if (suggestions.length > 0) {
            aiStatus.style.display = "none"; // ✅ hide after getting DB results
            suggestionsContainer.innerHTML = suggestions
                .map(recipe => `<div class="suggestion-item" data-recipe-id="${recipe.id}">${recipe.name}</div>`)
                .join("");
        } else {
            console.log("No recipes in DB. Using AI search...");
            aiStatus.textContent = "🤖 Not found in DB... Searching with AI...";

            const aiResponse = await fetch("/ai-search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: input })
            });
            const aiData = await aiResponse.json();

            if (aiData.recipes && aiData.recipes.length > 0) {
                aiStatus.style.display = "none"; // ✅ hide when AI is done
                aiRecipesCache = aiData.recipes.slice(0, 5);
                window.latestAIRecipes = aiData.recipes;

                suggestionsContainer.innerHTML = aiRecipesCache
                    .map((r, index) => `<div class="suggestion-item ai-item" data-index="${index}">${r.name}</div>`)
                    .join("");
            } else {
                aiStatus.style.display = "none";
                suggestionsContainer.innerHTML = "<p>No recipes found (even by AI).</p>";
            }
        }
    } catch (error) {
        console.error("Error fetching suggestions:", error);
        aiStatus.style.display = "none";
        suggestionsContainer.innerHTML = "<p>Error fetching suggestions.</p>";
    }
}


async function handleSuggestionClick(event) {
    const target = event.target;
    if (!target.classList.contains("suggestion-item")) return;

    const recipeId = target.getAttribute("data-recipe-id");
    const index = target.getAttribute("data-index");
    const recipeName = target.textContent.trim();

    // ✅ 1. Handle AI-generated recipe click
    if (target.classList.contains("ai-item")) {
        const foundRecipe =
            aiRecipesCache[index] ||
            aiRecipesCache.find(r => r.name === recipeName) ||
            window.latestAIRecipes?.find(r => r.name === recipeName); // <-- NEW

        if (foundRecipe) {
            console.log("🧠 Displaying AI recipe directly:", foundRecipe);

            displayRecipeDetails({
                name: foundRecipe.name || foundRecipe.recipe_name,
                description: foundRecipe.description || "No description available.",
                ingredients: foundRecipe.ingredients || [],
                steps: foundRecipe.steps || [],
                source: "AI"
            });
            return;
        } else {
            document.getElementById("recipe-details").innerHTML = "<p>No AI recipe details found.</p>";
            return;
        }
    }

   if (recipeId) {
       fetchRecipeDetails(target.textContent.trim());
       return;
   }


    try {
        const response = await fetch(`/get-recipe-detail?id=${encodeURIComponent(recipeName)}`);
        const recipe = await response.json();

        if (recipe.error) {
            document.getElementById("recipe-details").innerHTML = `<p>${recipe.error}</p>`;
        } else {
            displayRecipeDetails(recipe);
        }
    } catch (error) {
        console.error("Error fetching recipe details:", error);
    }
}
async function fetchRecipeDetails(recipeName) {
    console.log("Clicked recipe:", recipeName);

    // 🔹 1. Check AI cache or global fallback
    const aiRecipe =
        aiRecipesCache.find(r => r.name.toLowerCase().trim() === recipeName.toLowerCase().trim()) ||
        (window.latestAIRecipes
            ? window.latestAIRecipes.find(r => r.name.toLowerCase().trim() === recipeName.toLowerCase().trim())
            : null);

    if (aiRecipe) {
        console.log("⚡ Using AI cached recipe:", aiRecipe);
        displayRecipeDetails(aiRecipe);
        return;
    }

    // 🔹 2. Otherwise, check the Flask DB
    try {
        const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeName}`);
        const data = await response.json();
        console.log("Fetched recipe data:", data);

        if (!data || (Array.isArray(data) && data.length === 0)) {
            console.log("No recipe in DB or cache.");
            document.getElementById("recipe-details").innerHTML =
                `<p>No details found for ${recipeName}.</p>`;
        } else if (Array.isArray(data)) {
            displayRecipeDetails(data[0]);
        } else {
            displayRecipeDetails(data);
        }
    } catch (error) {
        console.error("Error fetching recipe details:", error);
        document.getElementById("recipe-details").innerHTML =
            `<p>Error fetching recipe details.</p>`;
    }
    // Show AI search status
    const aiStatus = document.getElementById("ai-status");
    aiStatus.style.display = "block"; // show when AI search starts



}
