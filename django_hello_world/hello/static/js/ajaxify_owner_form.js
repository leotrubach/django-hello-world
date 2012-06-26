function busy_form() {
    $('#status').text('Processing...');
    $('#ownerform').find('input, textarea').attr('disabled', 'disabled');
}

function data_sent(data) {
    if (data.status == 'success') {
        $('#status').text('Done');
        $('#ownerform').find('input, textarea').removeAttr('disabled');
    } else if (data.status == 'error') {
        $('#owner-form-container').html(data.form_html);
        activate_calendar();
    }
}

$(function(){
    $('#ownerform').ajaxForm({
        success: data_sent,
        beforeSubmit: busy_form,
        dataType: 'json'});
});
