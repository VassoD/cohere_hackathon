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

$(document).ready(function(){
  $(".navbar-toggler").click(function(){
    $(".navbar-collapse").slideToggle();
  });
});