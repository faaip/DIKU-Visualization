function openNav() {
    document.getElementById("sideControls").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById("sideButton").style.opacity = 0;
}

function closeNav() {
    document.getElementById("sideControls").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.getElementById("sideButton").style.opacity = 1;
}

