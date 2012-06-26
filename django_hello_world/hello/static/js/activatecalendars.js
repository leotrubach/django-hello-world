function activate_calendar(){
  $('.calendar').datepicker({
      dateFormat: "yy-mm-dd",
      changeMonth: true,
      changeYear: true,
      yearRange: '1900:2012'
})}

$(activate_calendar);
