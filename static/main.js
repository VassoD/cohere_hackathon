// Get the input element
var searchInput = document.getElementById("search_query");

// Listen for keyup event on the input element
searchInput.addEventListener("keyup", function() {
  // Get the current search query
  var searchQuery = this.value;

  // Make a GET request to the server with the search query as a query parameter
  fetch(`/?search_query=${searchQuery}`)
    .then(response => response.text())
    .then(data => {
      // Update the page with the returned data
      document.getElementById("results").innerHTML = data;
    });
});
