function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>');
    return false;
}

 $(document).on('click', '.add_answer', function(e){
e.preventDefault();
    cloneMore('.form-row:last', 'form');
    return false;
});

 $(document).on('click', '.add_question', function(e){
e.preventDefault();
    cloneMore('.form-row-q:last', 'form');
    return false;
});
//
//$(document).on('click', '.add_answer', function(){
//$(this).before(`<label class="answer">
//               <input type="text" id="answer1" placeholder="Ответ X" required>
//               <input type="checkbox">
//               </label><br>`)
//})
//
//// Добавление Вопроса
//$('.add_question').on('click', function() {
//
//$(this).before(`<div class="question answer"><label class="question" for="question">
//<h3>Введите свой вопрос</h3></label><br>
//<textarea name="question" id="question" cols="100" rows="10" placeholder="Введите текст своего вопроса" required></textarea>
//              <br>
//
//              <label class="answer"><input type="text" id="answer1" placeholder="Ответ 1" required>
//                <input type="checkbox">
//              </label><br>
//              <label class="answer"><input type="text" id="answer2" placeholder="Ответ 2" required>
//                <input type="checkbox">
//              </label><br>
//              <button class="btn-block add_answer" type="button">Добавить ответ</button>
//            </div>`
//)})