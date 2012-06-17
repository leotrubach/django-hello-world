function busy_form() {
    $('#status').text('Processing...');
    $('#ownerform').find('input, textarea').attr('disabled', 'disabled');
}

function data_sent() {
    $('#status').text('Done');
    $('#ownerform').find('input, textarea').removeAttr('disabled');
}

$(function(){
    $('#ownerform').ajaxForm({success: data_sent, beforeSubmit: busy_form});
});