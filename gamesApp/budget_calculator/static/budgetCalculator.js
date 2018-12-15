var netIncome;
var fortyTotalBudget;
var currentFortyBudget; //how much of the total 40% budget has NOT been spent
var totalMonthlyBudget;
var budget; //how much of the total budget has NOT been spent
var savings; //savings per month

function calculate()
{
  var totalNecessityBill = calc_total_necessity();
  var carPayment = calc_car_payment();
  var housePayment = calc_house_payment();

  netIncome = parseFloat($("#netIncome").val());
  totalMonthlyBudget = netIncome / 12;
  budget = totalMonthlyBudget;
  calc_40_budget();
  budget -= fortyTotalBudget - currentFortyBudget; //subtracts loan payments from budget
  budget -= totalNecessityBill; //subtract necessities from budget

  calculate_savings(); //updates the savings chart

  var totalLeftover = budget - savings;

  $("#totalMonthlyBudget").text(totalMonthlyBudget.toFixed(2));
  $("#totalFortyBudget").text(fortyTotalBudget.toFixed(2));
  $("#totalNecessityBill").text(totalNecessityBill.toFixed(2) + ", " + ((totalNecessityBill / totalMonthlyBudget) * 100).toFixed(2) + "%");
  $("#totalCarPayment").text(carPayment.toFixed(2) + ", " + ((carPayment / totalMonthlyBudget) * 100).toFixed(2) + "%");
  $("#totalHousePayment").text(housePayment.toFixed(2) + ", " + ((housePayment / totalMonthlyBudget) * 100).toFixed(2) + "%");
  $("#FortyBudget").text((fortyTotalBudget - currentFortyBudget).toFixed(2) + " / " + fortyTotalBudget.toFixed(2) + " spent");
  $("#totalLeftover").text(totalLeftover.toFixed(2) + ", " + ((totalLeftover / totalMonthlyBudget) * 100).toFixed(2) + "%");

  if(currentFortyBudget < 0 || totalLeftover < 0) {
    $("#summary").removeClass("alert-success").addClass("alert-danger");
  } else {
    $("#summary").removeClass("alert-danger").addClass("alert-success");
  }

}

//updates currentFortyBudget
function calc_40_budget()
{
  fortyTotalBudget = totalMonthlyBudget * 0.4;
  currentFortyBudget = fortyTotalBudget;
  currentFortyBudget -= calc_car_payment();
  currentFortyBudget -= calc_house_payment();
}

function calc_total_necessity()
{
  var total = 0;
  total += parseFloat($("#grocery").val());
  total += parseFloat($("#carGas").val());
  total += parseFloat($("#electricity").val());
  total += parseFloat($("#gas").val());
  total += parseFloat($("#water").val());
  total += parseFloat($("#internet").val());
  total += parseFloat($("#other").val());
  return total;
}

function calc_car_payment()
{
  var totalPrice = parseFloat($("#carPrice").val());
  var carInsurance = parseFloat($("#carInsurance").val());
  var loanTermMonths = parseInt($("#carLoanTerm").val());
  var downPayment = parseFloat($("#carDownPayment").val());
  var interestRate = parseFloat($("#carInterestRate").val());

  var r = (interestRate / 12) / 100;
  var P = totalPrice - downPayment;
  var carPayment = (r * P) / (1 - Math.pow(1 + r, -loanTermMonths));
  carPayment += carInsurance;
  return carPayment;
}

function calc_house_payment()
{
  var totalPrice = parseFloat($("#housePrice").val());
  var houseInsurance = parseFloat($("#houseInsurance").val());
  var loanTermYears = parseInt($("#houseLoanTerm").val());
  var downPayment = parseFloat($("#houseDownPayment").val());
  var interestRate = parseFloat($("#houseInterestRate").val());

  var r = (interestRate / 12) / 100;
  var P = totalPrice - downPayment;
  var N = loanTermYears * 12;

  var housePayment = (r * P) / (1 - Math.pow((1 + r), -N));
  housePayment += houseInsurance;

  return housePayment;
}

$("#calculate").on("click", function(){
  calculate();
});



// CHART
var dataList = []; //list of savings per year
var labelList = []; //labels for each year (year 1, year 2, etc.)
var chart; //holds the chart

function create_chart()
{
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");
  if(chart != null) {
    chart.destroy();
  }
  chart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: labelList,
          datasets: [{
              label: 'Total Savings',
              data: dataList,
              backgroundColor: 'rgba(3, 130, 33, 0.2)'
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      callback: function(value, index, values) {
                        return '$' + value;
                      }
                  }
              }]
          }
      }
  });
}
function calculate_savings()
{
  var years = 10; //num years to calculate savings
  savings = parseFloat($("#savings").val());
  var currentSavings = 0; //tracks savings for adding to datalist

  for(var i = 0; i < years; i++) {
    currentSavings += savings * 12;
    dataList[i] = currentSavings;
    labelList[i] = "Year " + (i + 1);
  }
  create_chart();
}
