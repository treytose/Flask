var title_letters = $("h1 span");

$(title_letters).on("click", function(){
  $(this).fadeOut(800);
});


/* weather */
updateWeather();
function updateWeather(){
  var zipcode = $("#zipCode").val().toString();
  if(zipcode == "")
    zipcode = "73102";
  $("#weatherTitle, #timestamp, #condition, #temperature, #feelsLike").fadeOut();

  $.getJSON("/api/weatherData/" + zipcode, function(data){
    if(!data.status == 200){
      alert("Weather data not found for " + zipcode);
      return;
    }
    $("#weatherTitle").html(data.location);
    $("#timestamp").html(data.timestamp);
    $("#condition").html(data.condition);
    $("#temperature").html(data.temperature);
    $("#feelsLike").html(data.feelsLike);
    $("#weatherTitle, #timestamp, #condition, #temperature, #feelsLike").fadeIn();

  });
}

$("#zipSubmit").on("click", updateWeather);
