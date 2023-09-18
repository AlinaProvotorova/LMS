// no usage

function startEdit() {
   // Включаем редактирование элемента.
   var element = document.getElementById("editableDiv");
   element.contentEditable = true;
}

function stopEdit() {
   // Отключаем редактирование элемента.
   var element = document.getElementById("editableDiv");
   element.contentEditable = false;

   // Выводим редактируемый текст в окне сообщения
   alert("Ваш отредактированный текст: \n" + element.innerHTML);
}