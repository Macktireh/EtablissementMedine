const containerInputSearch = document.querySelector(".input-search");
const searchResult = document.getElementById("search-results");
const inputSearch = document.querySelector(".input-search input");

let resultsVisible = false;

// Gérez le clic sur l'input de recherche
inputSearch.addEventListener("focus", (e) => {
  resultsVisible = true;
  showResults();
});

// Gérez le clic sur l'icône de suppression
searchResult.addEventListener("click", (e) => {
  if (e.target.tagName === "A") {
    window.location.href = e.target.href;
    return;
  }

  // Si l'icône de suppression a été cliquée
  if (e.target.classList.contains("delete-suggestion")) {
    e.preventDefault();
    e.stopPropagation();

    // Obtenez le terme de recherche associé à cette icône
    // const searchTerm = e.target.getAttribute("data-search-term");

    // // Supprimez la suggestion visuellement
    // e.target.parentElement.parentElement.remove();

    // Vous pouvez également effectuer une action supplémentaire ici, comme supprimer le terme de recherche de l'historique

    // Rétablissez le focus sur l'input de recherche
    // inputSearch.focus();
  }
});

// Affichez les résultats de recherche
function showResults() {
  if (resultsVisible) {
    searchResult.style.display = "flex";
  }
}

// Gérez le blur de l'input de recherche
inputSearch.addEventListener("blur", (e) => {
  if (e.target.value === "") {
    resultsVisible = false;
    hideResults();
  }
});

// Gérez le clic ailleurs dans le document
document.addEventListener("click", (e) => {
  if (!containerInputSearch.contains(e.target)) {
    resultsVisible = false;
    hideResults();
  }
});

// Masquez les résultats de recherche
function hideResults() {
  searchResult.style.display = "none";
}