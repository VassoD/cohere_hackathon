$(document).ready(function() {
  $('#search_query').focus(function() {
    if (this.value == 'Generate a News Headline') {
      this.value = '';
    }
  });

  $('#search_query').blur(function() {
    if (this.value == '') {
      this.value = 'Generate a News Headline';
    }
  });
});

$(document).ready(function () {
  $("#search_query").on("input", function () {
      if ($(this).val().length > 0) {
          $("#search-submit").removeAttr("disabled").css("background-color", "#B08383");
          $("#search-submit").hover(function () {
              $(this).css("background-color", "#ccc");
          }, function () {  // on mouseout
              $(this).css("background-color", "#B08383");
          });
      } else {
          $("#search-submit").attr("disabled", "disabled").css("background-color", "#ccc");
      }
  });
});


// const form = document.querySelector('form');
// const result = document.querySelector('#results_box');


// // Add a submit event listener to the form
// form.addEventListener('submit', (e) => {
//     e.preventDefault();

//     // Get the value of the feedback textarea
//     const feedback = form.querySelector('search_query').value;

//     // Send a POST request to the server with the feedback data
//     fetch('/', {
//         method: 'POST',
//         body: JSON.stringify({
//             feedback
//         }),
//         headers: {
//             'Content-Type': 'application/json'
//         },
//     })
//         .then(res => res.json())
//         .then(data => {
//             // Extract the prediction property
//             const prediction = data.prediction;
//             // Update the result element with the prediction
//             if (prediction === "negative") {
//                 result.innerHTML = `<p>😡</p>`;
//             } else if (prediction === "positive") {
//                 result.innerHTML = `<p>😊</p>`;
//             } else {
//                 result.innerHTML = `<p>😐</p>`;
//             }
//         });

// });


// Get the footer element
var footer = document.getElementById("footer");

// Add an event listener for the scroll event
window.addEventListener("scroll", function() {
  // Get the current scroll position
  var scrollPosition = window.pageYOffset || document.documentElement.scrollTop;

  // Get the height of the main content
  var mainContentHeight = document.querySelector(".main-content").offsetHeight;

  // Get the height of the viewport
  var viewportHeight = window.innerHeight || document.documentElement.clientHeight;

  // Check if the user has scrolled to the end of the page
  if (scrollPosition + viewportHeight >= mainContentHeight) {
    // Show the footer
    footer.classList.add("show-footer");
  } else {
    // Hide the footer
    footer.classList.remove("show-footer");
  }
});