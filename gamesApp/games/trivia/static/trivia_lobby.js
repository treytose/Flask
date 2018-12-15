var room_code = "";

/* ------------------ Host ----------------- */
$("#hostButton").on("click", function(){
  $.post("/trivia/create_room", function(data){
    if(data.status == 200){
      room_code = data.room_code;
      setCookie("roomCode", room_code, 1);
      $("#roomCode").text(room_code);
      $("#selectionDiv").fadeOut(400, function(){
          $("#hostDiv").hide().fadeIn();
      });
      hostPolling();
    }
  });
//  $("#hostDiv").append("<iframe style='display: none;' width='0' height='0' src='https://www.youtube.com/embed/VBlFHuCzPgY?autoplay=1&start=1'></iframe>");
});


function hostPolling(){
  $.get("/trivia/room_info/" + room_code, function(data){
    $("#playerList2").html(""); //clear playerList
    data.players.forEach(function(player){                  //update player list
      $("#playerList2").append("<li class='list-group-item'>" + player.username + "</li>");
    });
      if(data.game_started){
        window.location = "/trivia/host";
      } else {
        setTimeout(hostPolling, 2000);
      }
  });
}



/* ------------- Join ----------------------- */
$("#joinButton").on("click", function(){      //player clicks join
  $("#selectionDiv").fadeOut(400, function(){
      $("#joinDiv").hide().fadeIn();        //display room code input
  });
});

var first_player = false; //The first player to join will start the game.

$("#roomCodeSubmit").on("click", function(){  //player eneters room code
  room_code = $("#roomCodeInput").val();
  setCookie("roomCode", room_code, 1);
  $.post("/trivia/join_room/" + room_code + "/" + $("#teamName").val(), function(data){
    if(data.status != 200){
      alert("Room not found!");
    } else {
      first_player = data.first_player;

      $("#joinDiv").fadeOut(400, function(){    //show joinDiv2
        $("#joinDiv2").hide().fadeIn();
        if(first_player){
          $("firstPlayerDiv").hide().fadeIn(); //if first_player then show the "everyones in" button
        }
      });
      playerPolling();      //begin player polling
    }
  })
});

function playerPolling(){   //player polling for playerlist and game_started bool
  $.get("/trivia/room_info/" + room_code, function(data){

      $("#playerList1").html(""); //clear playerList
      data.players.forEach(function(player){                  //update player list
        $("#playerList1").append("<li class='list-group-item'>" + player.username + "</li>");
      });
      if(data.game_started){
        window.location = "/trivia/play";
      } else {
        setTimeout(playerPolling, 2000);
      }
  });
}


$("#allInButton").on("click", function(){
  $.post("/trivia/next_turn/" + room_code, function(data){
      console.log(data);
  });
});


/* ------------------------------------------------------- */

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
