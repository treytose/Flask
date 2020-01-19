var room_code = getCookie("roomCode");
var current_question = "";
var answer_list = [];
var all_answers_in = false;

var max_score = 15;
var initial_intro = true;

playAudio("introAudio", function(){
  setTimeout(stage1, 400, 9);
});

function newRound()
{
  current_question = "";
  answer_list = [];
  all_answers_in = false;
  $.post("/trivia/next_turn/" + room_code, function(data){
    $("#stage3").fadeOut(400, function(){
      stage1(7);
    });
  });
}

/* ------------------------- Stage 1 ------------------------- */
function stage1(timer){

  if(initial_intro){
    setTimeout(playAudio, 7000, "letsGetStarted");
    initial_intro = false;
  } else {
    setTimeout(playAudio, 3500, "nextQuestion");
  }

  $.get("/trivia/room_info/" + room_code, function(data){
    answer_list = data.answer_list;
    current_question = data.current_question;
    $("#question").html(current_question);
    $("#answerList").html("");
    answer_list.forEach(function(answer){
      $("#answerList").append("<li class='list-group-item'>" + answer + "</li>");
    });
  });
  swapViews("#welcomeDiv", "#incomingQuestion", 400);
  questionTimer(timer);
}

function questionTimer(time){           //time to indicate how many seconds until the next question is asked
  $("#questionTimer").html(time);
  if(time > 0)
    setTimeout(questionTimer, 1000, time-1);
  else{

    swapViews("#incomingQuestion", "#stage1", 1200);

    $.post("/trivia/question_asked/" + room_code);
    playAudio("jeopardy");
    setTimeout(answerTimer, 1000, 31);
    setTimeout(stage1Poll, 1000);
  }
}

function answerTimer(time){       //time players have left to answer
  $("#answerTimer").html(time);
  if(time > 0 && !all_answers_in)
    setTimeout(answerTimer, 1000, time-1);
  else{
    $.post("/trivia/times_up/" + room_code);
    $.get("/trivia/room_info/" + room_code, function(data){
      stage2(data);
    });
  }
}

function stage1Poll(){    //polling to see if all_answers_are_in
  $.get("/trivia/room_info/" + room_code, function(data){
      if(data.all_answers_in){
        all_answers_in = true;
      } else {
        setTimeout(stage1Poll, 2000);
      }
  });
}
/* ------------------------------------------------------------------------ */
/* ------------------------- Stage 2 - ALl answers are in ----------------- */

function stage2(data){
  stopAudio("jeopardy");
  playAudio("everyone_answered");
  $("#correctAnswer").text(data.current_answer);
  $("#answerRevealList").html("");
  data.players.forEach(function(player){
    if(player.answer_correct){
      $("#answerRevealList").append("<li class='list-group-item success'>" +
            cap(player.username) + " answered: " + cap(player.answer) + "</li>");
    }
    else if(player.answer == ""){
      $("#answerRevealList").append("<li class='list-group-item danger'> " +
          cap(player.username) + " " + getRandomExcuse() + "</li>");
    }
    else{
      $("#answerRevealList").append("<li class='list-group-item danger'> " +
          cap(player.username) + " answered: " + cap(player.answer) + "</li>");
    }
  });
  swapViews("#stage1", "#stage2", 1200, function(){
    setTimeout(swapViews, 1500, "#message1", "#message2", 1200);
    setTimeout(stage3, 7500, data);
  });
}



function stage3(data){
  swapViews("#stage2", "#stage3", 1200, showScores);

  var winners = [];
  data.players.forEach(function(player){    //checking if anyone won the game
    if(player.score >= max_score){
      winners.push(player);
    }
  });

  if(winners.length > 1){
    setTimeout(tieStage, 7500, winners);
  } else if(winners.length == 1){
    setTimeout(winnerStage, 7500, winners);
  } else {
    setTimeout(newRound, 7500);
  }

}
/*-------------------- Game Over Stages -------------------------------- */
function tieStage(winners){
  playAudio("tieAudio");
  swapViews("#stage3", "#tieStage", function(){
    winners.forEach(function(player){
      $("#tieStage").append("<h2> " + player.username + " has won! </h2>");
    });
  });

  $.post("/trivia/game_over/" + room_code);
  setTimeout(gameOverPoll, 5000);
}

function winnerStage(winners){
  playAudio("winnerAudio");
  swapViews("#stage3", "#winnerStage", function(){
    $("#winnerLabel").text(winners[0].username);
  });

  $.post("/trivia/game_over/" + room_code, function(data){
    console.log(data);
  });
  setTimeout(gameOverPoll, 5000);
}

function gameOverPoll(){  //poll to see if player clicks "Play Again"
  $.get("/trivia/room_info/" + room_code, function(data){
    if(data.play_again){
      $("#winnerStage, #tieStage").fadeOut(400, function(){
        newRound();
      });
    } else {
      setTimeout(gameOverPoll, 3000);
    }
  });
}



/* ---------------------------------------------------------------------- */
function showScores()
{
  $.get("/trivia/room_info/" + room_code, function(data){
    $("#scoreboard").html("");
    data.players.sort(function(a, b) {
        return b.score - a.score;
    })

    for(var i = 0; i < data.players.length; i++)
    {
       var progress = $("<div class='progress'> </div>");
       var bar = $("<div> </div>");
       $(bar).addClass("bar");

       $("#scoreboard").append(progress);
       $(progress).append(bar);

       if(i == 0){
         scoreBar(data.players[i].score, cap(data.players[i].username), 'albert_einstein.jpg', bar, progress);
       } else if(i == data.players.length-1){
         scoreBar(data.players[i].score, cap(data.players[i].username), 'dumber.jpg', bar, progress);
       } else {
         scoreBar(data.players[i].score, cap(data.players[i].username), null, bar, progress);
       }
    }
});


  function scoreBar(score, username, image, bar, progress){
    var original_score = score; //if score = 0 then dont place an image inside the bar div
    score *= (100 / max_score);

//style='top: 0; position: relative;  margin: 0px 0px;'
    if(image && original_score != 0){
      $(bar).append("<h3 style='top: 0; position: relative;  margin: 0px 0px;'>" + username + " </h3> <img class='user-image' src='/trivia/games/trivia/static/" + image + "'/>");
    } else {
      $(bar).append("<h3>" + username + "</h3>");
    }

    var width = 1;
    var id = setInterval(frame, 10);
    function frame(){
      if(width >= score){
        clearInterval(id);
      } else {
        width += 0.25;
        $(bar).css("width", width + "%");
      }
    }
  }

}














/* ------------------ Helpers ------------------------- */
function swapViews(view1, view2, time=400, after=null)
{
  $(view1).fadeOut(time, function(){
    if(after){
      after();
    }
    $(view2).fadeIn(time);
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

function getRandomExcuse(){
  var excuses = ["was sleeping...", "fell asleep...", "had to go to the batroom..",
  "was daydreaming...", "can't read...", "was pondering lifes most meaningful questions...", "was watching a squirrel...",
  "had a brain fart...", "was distracted by a bird", "couldn't see the question..."];
  return excuses[getRandomInt(0, excuses.length)];
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}


function playAudio(id, func=null)
{
  var audio = document.getElementById(id);
  if(func){
    audio.onended = func;
  }

  audio.play();

}

function stopAudio(id, func=null){
  var audio = document.getElementById(id);
  audio.pause();
  audio.currentTime = 0;
}
