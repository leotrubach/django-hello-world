from django import forms

from .models import Owner
from .widgets import ClearableImageInput


class OwnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs['class'] = 'span5'
        self.fields['other'].widget.attrs['class'] = 'span5'

    class Meta:
        model = Owner
        exclude = ('active')
        widgets = {'photo': ClearableImageInput()}
