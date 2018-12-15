var squares = document.querySelectorAll(".square");
var colorIndex = 0;
var colorToGuess = "";
var colorTitle = document.getElementById("sColor");
var messageDisplay = document.querySelector("#message");
var h1 = document.querySelector("h1");
var resetButton = document.querySelector("#reset");
var easyButton = document.getElementById("easy");
var hardButton = document.getElementById("hard");
var hardMode = true;

easyButton.addEventListener("click", function(){
  easyButton.classList.add("selected");
  hardButton.classList.remove("selected");
  hardMode = false;
  setColors();
});
hardButton.addEventListener("click", function(){
  easyButton.classList.remove("selected");
  hardButton.classList.add("selected");
  hardMode = true;
  setColors();
});


//add events listeners
for(var i = 0; i < squares.length; i++){
  squares[i].addEventListener("click", function(){
    var clickedColor = this.style.backgroundColor;
    if(clickedColor === colorToGuess){
      messageDisplay.textContent = "Correct!";
      changeColors(clickedColor);
      resetButton.textContent = "Play Again?";
    } else{
      this.style.backgroundColor = "#232323";
      messageDisplay.textContent = "Try Again";
    }
  });
}

setColors();
//set colors
function setColors(){
  if(hardMode){
    for(var i = 0; i < squares.length; i++){
      var color = "rgb(" + rand(255) + ", " + rand(255) + ", " + rand(255) + ")";
      squares[i].style.backgroundColor = color;
      squares[i].style.display = "block";
    }
    colorIndex = rand(squares.length - 1);
  }
  else{
      for(var i = 0; i < squares.length; i++){
        var color = "rgb(" + rand(255) + ", " + rand(255) + ", " + rand(255) + ")";
        squares[i].style.backgroundColor = color;
        if(i > squares.length / 2 -1){
          squares[i].style.display = "none";
        }
      }
      colorIndex = rand(squares.length / 2 - 1);
  }
    colorToGuess = colorTitle.textContent = squares[colorIndex].style.backgroundColor;

}

resetButton.addEventListener("click", function(){
  setColors();
  messageDisplay.textContent = "";
  resetButton.textContent = "New Colors"
  h1.style.background = "linear-gradient(to right, #4A569D, #DC2424)";
});


function changeColors(color){
  for(var i = 0; i < squares.length; i++){
    squares[i].style.backgroundColor = color;
  }
  h1.style.backgroundColor = color;
}

function rand(max){
  return (Math.round(Math.random() * max)).toString();
}
