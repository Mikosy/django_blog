
  function changeBackgroundColor() {
    var body = document.body;
    var anchors = document.getElementsByTagName("a");
    var buttons = document.getElementsByTagName("button");
    
    var currentColor = body.style.backgroundColor;
  
    if (currentColor === "white" || currentColor === "") {
      body.style.backgroundColor = "#181a2a";
      body.style.transition = "1s"
      body.style.color = "#fff";
  
      for (var i = 0; i < anchors.length; i++) {
        anchors[i].style.color = "#ff4828";
      }
      for (var i = 0; i < buttons.length; i++) {
        buttons[i].style.color = "#fff";
        buttons[i].style.backgroundColor = "#ff4828";
      }

    } else {
      body.style.backgroundColor = "white";
      body.style.color = "#222";
  
      for (var i = 0; i < anchors.length; i++) {
        anchors[i].style.color = "#222";
      }

      for (var i = 0; i < buttons.length; i++) {
        buttons[i].style.color = "#222";
        buttons[i].style.backgroundColor = "transparent";
      }

    }
  };

  const searchIcon = document.getElementById('search-icon');
  const closeButton = document.getElementById('close-button');
  const searchField = document.getElementById('hide-form');

  searchIcon.addEventListener('click', function(){
    console.log('i am clicked!');
    setTimeout(function() {
      searchField.style.display = "block";
      searchField.style.transition = "1s";
    }, 300);
    

  });
  closeButton.addEventListener('click', function(){
    console.log('close Menu');
    searchField.style.display = "none"
    searchField.style.transition = "1s"
  });


// Adding Post 
  $(document).ready(function (){
    $("#add-post").submit(function (event){
      event.preventDefault();

      
      
      $.ajax({
        type: "POST",
        url: "{% url 'app:search' %}",
        data: formData,
        success: function(data){
          $("#post-list").append(data.html);
        },
        error: function(xhr, errmsg, err){
          console.log("Error", err);
        },
      });
    });
  });
  
// Search

// $(document).ready(function () {
//   $("#search-form").submit(function (event) {
//       event.preventDefault();

//       var query = $("#search-query").val();

//       $.ajax({
//           type: "POST",
//           url: "{% url 'app:search' %}",  
//           data: { 'query': query },
//           success: function (data) {
//               $("#search-results").html(data.results.join('<br>'));
//           },
//           error: function (xhr, errmsg, err) {
//               console.log("Error:", err);
//           },
//       });
//   });
// });




function hideButton() {
  document.getElementById('message-button').style.display = 'none'
}
