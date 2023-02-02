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