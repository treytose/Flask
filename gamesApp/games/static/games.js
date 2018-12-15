var images = document.querySelectorAll(".gameImage");
images[0].addEventListener("click", function(){
  document.location = "/colorsGame";
});
images[1].addEventListener("click", function(){
  document.location = "/jumpMan";
});

images[2].addEventListener("click", function(){
  document.location = "/LQ/lobby";
});

images[3].addEventListener("click", function(){
  document.location = "/trivia/lobby";
});

images[4].addEventListener("click", function() {
  document.location = "/cowtownCowboy";
});

$("img").hover(function(){
  $(this).toggleClass("highlighted");
});
