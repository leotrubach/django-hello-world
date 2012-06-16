from django.forms.widgets import DateInput

class CalendarWidget(DateInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'calendar'}
        super(CalendarWidget, self).__init__(*args, **kwargs)

    class Media:
        js = ('js/activatecalendars.js',)