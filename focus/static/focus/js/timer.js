function setTimerMode(workMinutes, breakMinutes) {
    clearInterval(timerInterval);
    timerInterval = null;

    currentWorkMinutes = workMinutes;
    currentBreakMinutes = breakMinutes;
    timeLeft = workMinutes * 60;

    updateDisplay();
}

function setCustomTimer() {
    const work = Number(document.getElementById("customWork").value);
    const breakTime = Number(document.getElementById("customBreak").value);

    if (!work || !breakTime || work <= 0 || breakTime <= 0) {
        alert("Please enter valid work and break times.");
        return;
    }

    setTimerMode(work, breakTime);
}