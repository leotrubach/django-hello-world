function busy_form() {
    $(this).find('input').attr('disabled', 'disabled');
}

function data_sent() {
    $(this).find('input').removeAttr('disabled');
}

$(function(){
    $('.requestform').ajaxForm({success: data_sent, beforeSubmit: busy_form});
});