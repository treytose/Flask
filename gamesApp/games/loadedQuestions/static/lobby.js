var room_code;

/* ---------------- Host ----------------------*/
$("#hostButton").on("click", function(){
  $.getJSON('/LQ/host', function(data){ //get room code
    room_code = data.room_code;
    viewChange(".modeSelection", ".hostContent", function(){
      $("#roomCode").text(room_code);
      playerListPoll();
    });
  });
});

$("#startButton").on("click", function(){
  $.getJSON("/LQ/init/" + room_code, function(data){
    if(data.status != 200){
      alert("Error starting game :/");
    }
  });
});

//Poll server to find out which players have joined the room
function playerListPoll(){
  $.getJSON("/LQ/room_info/" + room_code, function(data){
      console.log(data);
      $("#userList1, #userList2").html("");
      for(var i = 0; i < data.nameList.length; i++){
        $("#userList1, #userList2").append("<li class='list-group-item'>" + data.nameList[i] + "</li>");
      }
      if(data.gameStarted){
        window.location = "/LQ/play";
      }
      setTimeout(playerListPoll, 2500);
  });
}

/*---------- Join -------------------*/
$("#joinButton").on("click", function(){
  viewChange(".modeSelection", ".joinContent");
});

$("#roomCodeSubmit").on("click", function(){
  room_code = $("#roomCodeInput").val().toUpperCase();

  $.getJSON("/LQ/join/" + room_code, function(data){
    if(data.status == 200){
      viewChange(".joinContent", ".waitingRoom", playerListPoll);
    } else {
      alert("Room not found!");
    }
  });
});


function viewChange(view1DOM, view2DOM, after=null){
  $(view1DOM).fadeOut(400, function(){
    if(after)
      after();
    $(view2DOM).fadeIn();
  });
}
