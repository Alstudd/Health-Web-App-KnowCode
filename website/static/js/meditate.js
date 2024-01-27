
var timerDisplay = document.querySelector('.timer-display');
var duration = timerDisplay.dataset.duration;
var timerId;

function startTimer() {
  timerId = setInterval(function() {
    duration--;
    if (duration < 0) {
      clearInterval(timerId);
      // code to be executed after the timer ends
    } else {
      updateDisplay(duration);
    }
  }, 1000);
}

function updateDisplay(duration) {
  var minutes = Math.floor(duration / 60);
  var seconds = duration % 60;
  timerDisplay.innerHTML = (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
}

updateDisplay(duration);

