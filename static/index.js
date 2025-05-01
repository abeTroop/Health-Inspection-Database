//script for opening/hiding advanced search

document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-button");
    const advancedSearch = document.getElementById("advanced-search");

    if (advancedSearchButton && advancedSearch) 
    {
        advancedSearchButton.addEventListener("click", function () 
        { 
            const isHidden = advancedSearch.style.display === "none" || advancedSearch.style.display === "";
            advancedSearch.style.display = isHidden ? "block" : "none";
            advancedSearchButton.textContent = isHidden ? "Basic Search" : "Advanced Search";
        }
        );
    } 
});

