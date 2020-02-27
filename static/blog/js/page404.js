
var num = 6;

function redirect() {
    num--;
    document.getElementById("num").innerHTML = num;
    if (num < 0) {
        document.getElementById("num").innerHTML = 0;
        location.href = "/";
    }
}

var bodyObj = window.document.getElementById("id_body");

bodyObj.onload = redirect;

setInterval("redirect()", 1000);
