$(function () {

   var newFields = $('');
   $('#id_rooms').bind('blur keyup change', function () {
      var n = this.value || 0;
      if (n + 1) {
         if (n > newFields.length) {
            addFields(n);
         } else {
            removeFields(n);
         }
      }
   });
});