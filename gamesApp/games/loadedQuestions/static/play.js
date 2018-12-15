var room_code;
var sections = $(".askerDiv, .askerPhase3, .readerDiv, .readerPhase4, .playerDiv, .playerPhase3, .playerPhase4");
var askerName = "";
var readerName = "";
var selectedCardQuestion = "";
var selectedCard;
var cardSet = 0;

$.getJSON('/LQ/whatsmyroomcode', function(data){  //Get Room Code upon entrance.
  if(data.status == 200){
    room_code = data.room_code;
    newCards();
    round_init();
  }
});

function showScore(){
  $("#roundsbPlayerList").html("");
  $("#roundsbScoreList").html("");

  $.getJSON("/LQ/room_info/" + room_code, function(data){
    for(var i = 0; i < sections.length; i++){  //hide all divs for reset
      $(sections[i]).fadeOut();
    }
    $(".col-sm-8").fadeOut();
    $(".col-sm-3").fadeOut();
    data.playerInfo.sort(function(a, b){  //sort scores
      return b.score - a.score;
    });
    for(var i = 0; i < data.playerInfo.length; i++){
      $("#roundsbPlayerList").append("<li class='list-group-item scoreBoardList'> " + capitalize(data.playerInfo[i].username) + "</li>");
      $("#roundsbScoreList").append("<li class='list-group-item scoreBoardList'> " + data.playerInfo[i].score + "</li>");
    }
    $(".betweenRoundsDiv").hide().fadeIn();
    setTimeout(round_init, 7500);
  });
}

function round_init()
{
  var inputs = $("input");
  for(var i = 0; i < inputs.length; i++){
    $(inputs[i]).val("");
  }
  $(".betweenRoundsDiv").fadeOut(400, function(){

  });
  $(".col-sm-8").fadeIn();
  $(".col-sm-3").fadeIn();
  $.getJSON("/LQ/room_info/" + room_code, function(data){ //get player role and call respective phases
    askerName = capitalize(findAsker(data.playerInfo));
    readerName = capitalize(findReader(data.playerInfo));
    if(data.role == "asker")
      askerPhase1();
    else if(data.role == "reader")
      readerPhase1(data);
    else
      playerPhase1();

    updateScoreboard(data.playerInfo);

  });
}


/* ------------- Asker -------------- */
function askerPhase1(){
  $(".askerDiv").hide().fadeIn();
  $(".askerPhase1").hide().fadeIn();
  $.getJSON('/LQ/room_info/' + room_code, function(data){ //checks if question has already been asked (user refreshed page)
      if(data.currentQuestion != '')
        askerPhase2();
  });
}

$("#askerCustomSubmit").on("click", function(){
  if($("#askerCustomQuestion").val() != null){
    $.getJSON('/LQ/ask_question/' + room_code + '/' + $("#askerCustomQuestion").val(), function(data){
      if(data.status == 200)
        askerPhase2();
    });
  }
});

$("#askerCardSubmit").on("click", function(){
  if(selectedCardQuestion != ""){
    $.getJSON('/LQ/ask_question/' + room_code + '/' + selectedCardQuestion, function(data){
      if(data.status == 200)
        askerPhase2();
    });
  }
});

function askerPhase2(){
  swapViews(".askerPhase1", ".askerPhase2");
  askerPhase2Poll();
}

function askerPhase2Poll(){
  $.getJSON('/LQ/room_info/' + room_code, function(data){
    if(data.allAnswersIn){
      askerPhase3(data.playerInfo);
    } else {
      setTimeout(askerPhase2Poll, 2500);
    }
  });
}

function askerPhase3(playerInfo){
  swapViews(".askerPhase2", ".askerPhase3", function(){
    $("#askerReaderTitle").html(readerName);
    setTimeout(askerPhase3Poll, 5000);
  });
}

function askerPhase3Poll(){
  $.getJSON('/LQ/room_info/' + room_code, function(data){

    if(data.gameStarted)
      showScore();
    else
      setTimeout(askerPhase3Poll, 2500);
  });
}


/* ------------- Reader -------------- */

function readerPhase1(data){  //waiting for question
  $(".readerDiv").hide().fadeIn();
  $(".readerPhase1").hide().fadeIn();
  $("#askerName1, #askerName2").text(askerName);
  phase1Poll();
}

function phase1Poll(){
  $.getJSON('/LQ/room_info/' + room_code, function(data){

    if(data.currentQuestion != ''){
      readerPhase2(data.currentQuestion);
    }
    else
      setTimeout(phase1Poll, 2500);
  });
}

function readerPhase2(current_question){
  swapViews(".readerPhase1", ".readerPhase2", function(){
    $("#readerQuestion").html("<b>Question:</b> " + current_question + "?");
    $.getJSON('/LQ/already_answered/' + room_code, function(data){
      if(data.answered)
        readerPhase3();
    });
  });
}

$("#readerSubmitAnswer").on("click", function(){
  $.getJSON('/LQ/answer_question/' + room_code + '/' + $("#readerAnswer").val(), function(data){
    if(data.status == 200){
      readerPhase3();
    }
  });
});


function readerPhase3(){
  swapViews(".readerPhase2", ".readerPhase3");
  setTimeout(readerPhase3Poll, 600);
}

function readerPhase3Poll(){    //polling for allquestionsanswered
  $.getJSON('/LQ/room_info/' + room_code, function(data){
    if(data.allAnswersIn){
      readerPhase4(data.playerInfo, data.answer_list);
    } else {
      setTimeout(readerPhase3Poll, 2500);
    }
  });
}


function readerPhase4(playerInfo, answerList){
  swapViews(".readerPhase3", ".readerPhase4");
  $("#readerAskerName, #readerAskerName2").html(askerName);
  $("#readerAnswerList").html("");
  $("#readerPlayerList").html("");
  for(var i = 0; i < answerList.length; i++)
  {
    $("#readerPlayerList").append("<li class='list-group-item list responsiveFont'>" +   capitalize(answerList[i].user) + "</li>");
    $("#readerAnswerList").append("<li class='list-group-item list'>" + answerList[i].answer + "</li>");
  }
}

$("#scoreSubmit").on("click", function(){
  $.getJSON("/LQ/submit_score/" + room_code + "/" + $("#scoreInput").val(), function(){
    showScore();
  });
});

/* ------------- Player -------------- */

function playerPhase1(){
  $(".playerDiv").hide().fadeIn();
  $(".playerPhase1").hide().fadeIn();
  $("#aName, #aName2", "#aName3").text(askerName);
  playerPhase1Poll();
  function playerPhase1Poll(){
    $.getJSON('/LQ/room_info/' + room_code, function(data){

      if(data.currentQuestion != ''){
        playerPhase2(data.currentQuestion);
      }
      else
        setTimeout(playerPhase1Poll, 2500);
    });
  }
}


function playerPhase2(currentQuestion){
  swapViews(".playerPhase1", ".playerPhase2", function(){
    $("#playerQuestion").html("<b>Question:</b> " + currentQuestion + "?");
    $.getJSON('/LQ/already_answered/' + room_code, function(data){
      if(data.answered)
        playerPhase3();
    });
  });
}

$("#playerSubmitAnswer").on("click", function(){
  $.getJSON('/LQ/answer_question/' + room_code + '/' + $("#playerAnswer").val(), function(data){
    if(data.status == 200){
      playerPhase3();
    }
  });
});

function playerPhase3(){
  swapViews(".playerPhase2", ".playerPhase3");
  setTimeout(playerPhase3Poll, 600);

  function playerPhase3Poll(){    //polling for allquestionsanswered
    $.getJSON('/LQ/room_info/' + room_code, function(data){
      if(data.allAnswersIn){
        playerPhase4(data);
      } else {
        setTimeout(playerPhase3Poll, 2500);
      }
    });
  }
}

function playerPhase4(data)
{
  swapViews(".playerPhase3", ".playerPhase4");
  setTimeout(readerPhase4Poll, 5000);
  $("#pQuestionTitle1").html("Question: " + data.currentQuestion);
  function readerPhase4Poll(){
    $.getJSON('/LQ/room_info/' + room_code, function(data){
      if(data.gameStarted)
        showScore();
      else
        setTimeout(readerPhase4Poll, 2500);
    });
  }
}



/* ------ General -----------*/
function updateScoreboard(playerInfo)
{
  playerInfo.sort(function(a, b){
    return b.score - a.score;
  });
  $("#sbPlayerList").html("");
  $("#sbScoreList").html("");
  for(var i = 0; i < playerInfo.length; i++){
    $("#sbPlayerList").append("<li class='list-group-item scoreBoardList'> " + capitalize(playerInfo[i].username) + "</li>");
    $("#sbScoreList").append("<li class='list-group-item scoreBoardList'> " + playerInfo[i].score + "</li>");
  }
}
function findAsker(playerInfo){
  for(var i = 0; i < playerInfo.length; i++){
    if(playerInfo[i].role == "asker"){
      return playerInfo[i].username;
    }
  }
}

function findReader(playerInfo){
  for(var i = 0; i < playerInfo.length; i++){
    if(playerInfo[i].role == "reader"){
      return playerInfo[i].username;
    }
  }
}

function swapViews(view1, view2, after=null){
  $(view1).hide().fadeOut(400, function(){
    if(after)
      after();
    $(view2).hide().fadeIn();
  });
}

function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

/*--------- Cards ------------- */
refreshOnClickCards();  //put in function so when we get new cards they also react to a click by calling this function.
function refreshOnClickCards(){
  $(".card").on("click", function(){
    $(this).css("border-color", "orange");
    if(selectedCard){
      $(selectedCard).css("border-color", "#141E30");
    }
    selectedCard = $(this);
    selectedCardQuestion = $(this).text();
  });
}

function newCards(){
  $.getJSON("/LQ/cardList/" + cardSet, function(data){
    if(!data.moreCards)
      cardSet = 0;  //card set above max sets returns set 0, so then restart at 1 as to not return set 0 twice...

    cardSet++;

    $("#cardList").html("");
    for(var i = 0; i < data.cards.length; i++){
        $("#cardList").append("<li class='list-group-item card'> " + data.cards[i] + "</li>");
    }
    refreshOnClickCards();
  });
}
$("#newCards").on("click", newCards);
