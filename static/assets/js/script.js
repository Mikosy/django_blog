
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
  }
  