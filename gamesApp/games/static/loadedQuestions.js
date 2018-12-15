var room_code = "";

$("#hostButton").on("click", function(){
  $(".modeSelection").fadeOut(400, function(){
      $.getJSON("/LQ/host" ,function(data){
        $("#roomCode").text(data.room_code);
        room_code = data.room_code;
      });
      $(".hostContent").fadeIn();
  });
  startPolling();
});

$("#joinButton").on("click", function(){
  $(".modeSelection").fadeOut(400, function(){
    $(".joinContent").fadeIn();
  });

});

$("#roomCodeSubmit").on("click", function(){
  $.getJSON("/LQ/join/" + $("#roomCodeInput").val(), function(data){
      if(data.code == "200"){
        $(".joinContent").fadeOut(400, function(){
          $(".waitingRoom").fadeIn();
        });
        startPolling();
      } else {
        alert("Failed to join room");
      }
  });
});

function startPolling(){
  setInterval(function(){
    $.getJSON("/LQ/status", function(data){

      if(data.game_started){
        window.location = "/LQGameBoard"
      }

      $(".userList").html("");
      $(".userList2").html("");
      for(var i = 0; i < data.users.length; i++){
          $(".userList").append("<p>" + data.users[i] + "</p>");
          $(".userList2").append("<p>" + data.users[i] + "</p>");
      }
    });
  }, 1000);
}


$("#startButton").on("click", function(){
  $.getJSON("/LQ/startGame", function(data){
      if(data.code != 200){
        alert("Error start game");
      }
  });
});
