import random

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from .models import Owner
from django_hello_world.settings import MIDDLEWARE_CLASSES
from django.forms.models import model_to_dict


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name')
        self.assertContains(response, 'Last name')
        self.assertContains(response, 'Bio')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Jabber')
        self.assertContains(response, 'Skype')
        self.assertContains(response, 'Other contacts')

    def test_request_middleware(self):
        self.assertIn(
            'django_hello_world.hello.middleware.StoreRequestMiddleware',
            MIDDLEWARE_CLASSES)
        c = Client()
        response = c.get(reverse('last_requests'))
        self.assertContains(response, 'Requests')
        self.assertIn('last_requests', response.context)

    def test_context_processors(self):
        from django.conf import settings
        c = Client()
        response = c.get(reverse('home'))
        self.assertEquals(settings, response.context['settings'])

    def test_owner_photo(self):
        self.assertIn('photo', [f.name for f in Owner._meta.fields])
        c = Client()
        response = c.get(reverse('home'))
        self.assertContains(response, 'Login')
        # Login and check if there is 'Edit' link and logout link
        c.post('/login/', {'username': 'admin', 'password': 'admin'})
        response = c.get(reverse('home'))
        self.assertContains(response, 'Logout')
        self.assertContains(response, 'Edit')
        pk = Owner.objects.get(active=True).id
        response = c.get(reverse('edit_owner', kwargs={'pk': pk}))
        d = model_to_dict(response.context['form'].instance)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        randomname = ''.join([random.choice(alphabet) for i in range(8)])
        d['firstname'] = randomname
        del d['active']
        d['photo-clear'] = False
        d['photo'] = None
        c.post(reverse('edit_owner', kwargs={'pk': pk}), d)
        response = c.get(reverse('home'))
        self.assertContains(response, randomname)

    def test_calendar(self):
        from django_hello_world.hello.widgets import CalendarWidget

    def test_admintag(self):
        from django_hello_world.hello.templatetags.admintags import edit_link
        from django.template import Template, Context
        o = Owner.objects.get(active=True)
        s = '''{% load admintags %}
            {% edit_link owner %}'''
        t = Template(s)
        c = Context({'owner': o})
        self.assertIn(edit_link(o), t.render(c))
        self.assertEqual(edit_link(o), '/admin/hello/owner/%s/' % o.id)
