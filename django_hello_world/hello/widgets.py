from django.utils.safestring import mark_safe
from django.forms import FileInput, CheckboxInput, DateInput
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode


class CalendarWidget(DateInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'calendar'}
        super(CalendarWidget, self).__init__(*args, **kwargs)

    class Media:
        js = ('js/activatecalendars.js',)


class ClearableImageInput(FileInput):
    input_text = 'Change'
    clear_checkbox_label = 'Clear'

    template_with_initial = (
        u'%(initial)s %(clear_template)s<br />'
        u'%(input_text)s: %(input)s')

    template_with_clear = (
        u'<label for="%(clear_checkbox_id)s" '
        u'class="checkbox">%(clear)s %(clear_checkbox_label)s</label>')

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input, return the
        name of the clear checkbox input.
        """
        return name + '-clear'

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input,
        return the HTML id for it.
        """
        return name + '_id'

    def render(self, name, value, attrs=None):
        substitutions = {
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(
            ClearableImageInput,
            self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = (u'<img src="%s" alt="%s" />'
                                        % (escape(value.url),
                                           escape(force_unicode(value))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = (
                    conditional_escape(checkbox_name))
                substitutions['clear_checkbox_id'] = (
                    conditional_escape(checkbox_id))
                substitutions['clear'] = CheckboxInput().render(
                    checkbox_name, False,
                    attrs={'id': checkbox_id})
                substitutions['clear_template'] = (
                    self.template_with_clear % substitutions)

        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        upload = super(
            ClearableImageInput,
            self).value_from_datadict(data, files, name)
        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):
            if upload:
                # If the user contradicts themselves (uploads a
                # new file AND checks the "clear" checkbox), we
                # return a unique marker object that FileField
                # will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value,
            # as opposed to just None
            return False
        return upload
