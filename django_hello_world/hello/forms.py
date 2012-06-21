from django import forms

from .models import Owner, Request
from .widgets import ClearableImageInput, CalendarWidget


class OwnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs['class'] = 'span5'
        self.fields['other'].widget.attrs['class'] = 'span5'

    class Meta:
        model = Owner
        exclude = ('active')
        widgets = {'photo': ClearableImageInput(),
                   'birthday': CalendarWidget()}

    class Media:
        js = ('js/jquery.form.js', 'js/ajaxify_owner_form.js')


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('priority',)

    class Media:
        js = ('js/ajaxify_request_form.js',)