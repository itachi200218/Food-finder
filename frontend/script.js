// Event listener for form submission (recipe search by keyword)
document.getElementById("recipe-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const userInput = document.getElementById("recipe-input").value;

    fetchRecipeDetails(userInput);
});

// Event listeners for sidebar clicks
const sidebarItems = document.querySelectorAll(".sidebar ul li");
sidebarItems.forEach(item => {
    item.addEventListener("click", function () {
        const recipeName = item.textContent.trim();
        fetchRecipeDetails(recipeName);
    });
});

// Function to fetch recipe details
function fetchRecipeDetails(recipeName) {
    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: recipeName })
    })
    .then(response => response.json())
    .then(data => {
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
            recipeDetailsDiv.innerHTML = `
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
    })
    .catch(error => {
        document.getElementById("recipe-details").innerHTML = `<p>Something went wrong. Please try again.</p>`;
    });
}

// Helper function to extract YouTube video ID from URL
function extractYouTubeId(url) {
    // Regex for extracting YouTube video ID for both regular videos and shorts
    const regex = /(?:https?:\/\/(?:www\.)?youtube\.com\/(?:v\/|e(?:mbed)?\/|\S*?[?&]v=)|(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}













































