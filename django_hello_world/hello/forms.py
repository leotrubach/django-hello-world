from django import forms

from .models import Owner
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

class PriorityForm(forms.Form):
    priority = forms.TypedChoiceField(
        choices=((0, 'ascending'), (1, 'descending')),
        coerce=int,
        label='priority',
        required=False)
