//document.addEventListener("DOMContentLoaded", () => {
//  const searchInput = document.getElementById("searchInput");
//  const suggestionsBox = document.getElementById("suggestions");
//  const resultsDiv = document.getElementById("results");
//  const searchButton = document.getElementById("searchButton");
//
//  let typingTimer;
//  const typingDelay = 300;
//
//  // 🧠 Typing-based Suggestions
//  searchInput.addEventListener("input", () => {
//    clearTimeout(typingTimer);
//    const query = searchInput.value.trim();
//    if (query.length > 0) {
//      typingTimer = setTimeout(() => fetchSuggestions(query), typingDelay);
//    } else {
//      suggestionsBox.innerHTML = "";
//    }
//  });
//
//  // 🧩 Fetch suggestions from DB
//  async function fetchSuggestions(query) {
//    try {
//      const res = await fetch(`/get-suggestions?query=${encodeURIComponent(query)}`);
//      if (!res.ok) throw new Error("Failed to fetch suggestions");
//
//      const suggestions = await res.json();
//      showSuggestions(suggestions);
//    } catch (err) {
//      console.error("Error fetching suggestions:", err);
//    }
//  }
//
//  // 🪄 Show suggestions dropdown
//  function showSuggestions(suggestions) {
//    suggestionsBox.innerHTML = "";
//    if (suggestions.length === 0) {
//      suggestionsBox.style.display = "none";
//      return;
//    }
//
//    suggestionsBox.style.display = "block";
//    suggestions.forEach((name) => {
//      const div = document.createElement("div");
//      div.className = "suggestion-item";
//      div.textContent = name;
//      div.addEventListener("click", () => {
//        searchInput.value = name;
//        suggestionsBox.innerHTML = "";
//        fetchRecipeDetail(name);
//      });
//      suggestionsBox.appendChild(div);
//    });
//  }
//
//  // 🔍 Search button click
//  searchButton.addEventListener("click", () => {
//    const query = searchInput.value.trim();
//    if (query) fetchRecipeDetail(query);
//  });
//
//  // 🍳 Fetch full recipe details by ID or Name
//  async function fetchRecipeDetail(idOrName) {
//    try {
//      showLoading();
//      const res = await fetch(`/get-recipe-detail?id=${encodeURIComponent(idOrName)}`);
//      if (!res.ok) throw new Error("Failed to fetch recipe details");
//
//      const data = await res.json();
//      if (data.error) {
//        showError(data.error);
//      } else {
//        showRecipeDetail(data);
//      }
//    } catch (err) {
//      console.error("Error fetching recipe details:", err);
//      showError("Error fetching recipe details.");
//    }
//  }
//
//  // 🎡 Show fancy loading animation
//  function showLoading() {
//    resultsDiv.innerHTML = `
//      <div class="loading-container">
//        <div class="loader"></div>
//        <p>Loading your recipe...</p>
//      </div>
//    `;
//  }
//
//  // ❌ Show error message
//  function showError(msg) {
//    resultsDiv.innerHTML = `<p class="error">${msg}</p>`;
//  }
//
//  // 🍽️ Display recipe details
//  function showRecipeDetail(recipe) {
//    resultsDiv.innerHTML = `
//      <div class="recipe-card">
//        <h2>${recipe.name}</h2>
//        <p><strong>Description:</strong> ${recipe.description}</p>
//        <p><strong>Category:</strong> ${recipe.category || "N/A"}</p>
//        <h3>🧂 Ingredients</h3>
//        <ul>${recipe.ingredients.map((i) => `<li>${i}</li>`).join("")}</ul>
//        <h3>👨‍🍳 Steps</h3>
//        <ol>${recipe.steps.map((s) => `<li>${s}</li>`).join("")}</ol>
//      </div>
//    `;
//  }
//});
