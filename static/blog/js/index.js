

$(function () {
   var navBar = $("#id_navbar");
   var activeA = $("#id_active_li a");
   console.log(activeA);
   $(document).scroll(function (event) {
      if (!$(this).scrollTop()) {
         navBar.css("background-color", "rgb(34,34,34)");
         activeA.css("background-color", "rgb(8,8,8)");
      } else {
         navBar.css("background-color", "rgba(34,34,34,0.5)");
         activeA.css("background-color", "rgba(8,8,8,0.5)");

      }
   });
});