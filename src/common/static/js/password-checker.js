$(function () {
   $("#psw2").keyup(function () {
      var password = $("#psw1").val();
      $("#validate-status").html(password == $(this).val() ? "Пароли совпадают" : "Пароли не совпадают");
   });

});