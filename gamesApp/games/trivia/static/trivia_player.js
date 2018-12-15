var room_code = getCookie("roomCode");
var current_question = "";
var answer_list = [];
var selected_answer = "";

setTimeout(stage1, 1000);


function newRound()
{
  current_question = "";
  answer_list = [];
  selected_answer = "";
  $("#stage4").fadeOut(1200, function(){
    stage1();
  });
}


/* ------------- Stage 1 - Waiting for the Question ---------------------- */
function stage1(){
  swapViews("#welcomeDiv", "#stage1", 1200);
  $.get("/trivia/room_info/" + room_code, function(data){     //setup the question and answerlist.
      $("#question").html(data.current_question);
      $("#answerList").html("");
      data.answer_list.forEach(function(answer){
        $("#answerList").append("<li class='list-group-item'>" + answer + "</li>");
      });
  });
  stage1Poll();
}

function stage1Poll()  //asking the server if the question's been asked
{
  $.get("/trivia/room_info/" + room_code, function(data){
    if(data.question_asked){
      stage2();
    } else {
      setTimeout(stage1Poll, 2000);
    }
  });
}


/* ------------------------ Stage 2 - Answering the Question ------------- */
var answered = false;
var stage_2_poll;

function stage2(){
  swapViews("#stage1", "#stage2")
  answered = false;
  stage2Poll();
}

$("#answerSubmit").on("click", function(){
  clearTimeout(stage_2_poll);
  $.post("/trivia/answer_question/" + room_code + "/" + selected_answer, function(data){
      if(data.status == 200){
        answered = true;
        stage3();
      }
  });
});

 $("#answerList").on("click", ".list-group-item", function(){
   items = $("#answerList .list-group-item");
   for(var i = 0; i < items.length; i++){
     $(items[i]).removeClass("colorful", 400);
   }
   if($(this).text() != selected_answer){
     $(this).addClass("colorful", 400);
     selected_answer = $(this).text();
   }
 });

 function stage2Poll(){     //if player runs out of time, skips stage 3, to stage 4.
   $.get("/trivia/room_info/" + room_code, function(data){
     if(data.times_up){
       $("#stage2").fadeOut(400, function(){
         if(!answered){
           stage3();
         }
       });
     } else {
       stage_2_poll = setTimeout(stage2Poll, 2000);
     }
   })
 }


/* ------------------------- Stage 3 - Waiting for everyone to answer ------------------- */
function stage3(){
    swapViews("#stage2", "#stage3");
    stage3Poll();
}

function stage3Poll(){
  console.log("Stage 3 poll");
  $.get("/trivia/room_info/" + room_code, function(data){
    if(data.all_answers_in || data.times_up){
      setTimeout(stage4, 1500, data);
    } else {
      setTimeout(stage3Poll, 2000);
    }
  });
}

/* ------------------------- Stage 4 - Viewing the scores ------------------------------ */
function stage4(data){
  swapViews("#stage3", "#stage4", 1200);
  stage4Polling();
}

function stage4Polling(){
  $.get("/trivia/room_info/" + room_code, function(data){
      if(data.game_started)
        newRound();
      else if(data.game_over)
        gameOver();
      else
        setTimeout(stage4Polling, 2000);
  });
}


/* ---------------------- Game Over - Prompts the player if they would like to play again. -------- */
var poll_timeout;
function gameOver(){
  swapViews("#stage4", "#gameOverStage");
  gameOverPoll();
}

$("#donePlayingButton").on("click", function(){
  window.location = "/games";
});

$("#playAgainButton").on("click", function(){
  $.post("/trivia/play_again/" + room_code, function(data){
    if(data.status == 200){
      $("#gameOverStage").fadeOut(400, function(){
        clearTimeout(poll_timeout);
        waitForHost();
      });
    }
  });
});

function gameOverPoll(){  //poll to see if player clicks "Play Again"
  $.get("/trivia/room_info/" + room_code, function(data){
    if(data.play_again){
      $("#gameOverStage").fadeOut(400, function(){
        waitForHost();
      });
    } else {
      poll_timeout = setTimeout(gameOverPoll, 3000);
    }
  });
}

function waitForHost(){
  $.get("/trivia/room_info/" + room_code, function(data){
    console.log(data.game_started);
    if(data.game_started){
      newRound();
    } else {
      setTimeout(waitForHost, 2000);
    }
  });
}
/* --------------------------- General Helper Functions---------------------- */

function swapViews(view1, view2, time=400, after=null)
{
  $(view1).fadeOut(time, function(){
    if(after){
      after();
    }
    setTimeout(function(){$(view1).hide();}, time * 2 + 500); //re-hides the div for assurance.
    $(view2).hide().fadeIn(time);
  });
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function cap(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}
