function openLeftControls() {
    document.getElementById("leftControls").style.width = "250px";
    document.getElementById("leftSideButton").style.opacity = 0;
}

function openRightControls() {
    document.getElementById("rightControls").style.width = "250px";
    document.getElementById("rightSideButton").style.opacity = 0;
}

function closeLeftControls() {
    document.getElementById("leftControls").style.width = "0";
    document.getElementById("leftSideButton").style.opacity = 1;
}

function closeRightControls() {
    document.getElementById("rightControls").style.width = "0";
    document.getElementById("rightSideButton").style.opacity = 1;
}