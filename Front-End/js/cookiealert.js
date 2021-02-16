// The used cookie alert structure was created by Wruczek, https://github.com/Wruczek/Bootstrap-Cookie-Alert
(function () {
    "use strict";

    var cookieAlert = document.querySelector(".cookiealert");
    var acceptCookies = document.querySelector(".acceptcookies");
    let settings = ["originalImageCheck","keywordsImageCheck","allCheck","nyTimesCheck","foxCheck","cnbcCheck","yahooCheck","nbcCheck","cbsCheck"];

    if (!cookieAlert) {
       return;
    }

    // Force browser to trigger reflow (https://stackoverflow.com/a/39451131)
    cookieAlert.offsetHeight;

    // Show the alert if we cant find the "acceptCookies" cookie
    if (!getCookie("acceptCookies")){
        cookieAlert.classList.add("show");
    }

    $("#disagreeCookiesButton").click(function(){
        document.querySelector(".cookiealert").classList.remove("show");
    });  

    // When clicking on the agree button, create a 1 year cookie to remember user's choice and close the banner
    // Set the firstVisit to false and save the set settings
    acceptCookies.addEventListener("click", function () {
        setCookie("acceptCookies", true, 365);
        cookieAlert.classList.remove("show");
        for (var i = 0; i < settings.length; i++) {
            localStorage.setItem(settings[i], document.getElementById(settings[i]).checked);
        }
        // Dispatch the accept event
        window.dispatchEvent(new Event("cookieAlertAccept"));
    });
})();

// Cookie functions from w3schools
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// Global array variables for settings checkboxes and info buttons
var newsSites = ["nyTimes","yahoo","nbc","cbs","fox","cnbc"];
var newsSitesCheck = newsSites.map(j => j + 'Check');
var newsSitesHashTag = newsSitesCheck.map(i => '#' + i);
var queryArray = [];
for (var i = 0; i < newsSitesHashTag.length; i++) {
  queryArray.push(document.querySelector(newsSitesHashTag[i]));
}
var infoButtonArr = newsSites.map(i => '#' + i + 'InfoButton');
var queryInfoButtonArr = [];
for (var i = 0; i < infoButtonArr.length; i++) {
  queryInfoButtonArr.push(document.querySelector(infoButtonArr[i]));
}
var infoCloseButtonArr = newsSites.map(i => '#' + i + 'InfoCloseButton');
var queryInfoCloseButtonArr = [];
for (var i = 0; i < infoCloseButtonArr.length; i++) {
  queryInfoCloseButtonArr.push(document.querySelector(infoCloseButtonArr[i]));
}