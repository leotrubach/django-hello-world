from django import template
from django.db.models import Model
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def edit_link(obj):
    if isinstance(obj, Model):
        app_label = obj._meta.app_label
        model_name = obj.__class__.__name__.lower()
        view_str = 'admin:%s_%s_change' % (app_label, model_name)
        return reverse(view_str, args=(obj.id,))
