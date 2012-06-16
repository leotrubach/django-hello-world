"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from .models import Owner

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

    def test_reqmid(self):
        from django_hello_world.settings import MIDDLEWARE_CLASSES
        self.assertIn('django_hello_world.hello.middleware.StoreRequestMiddleware', MIDDLEWARE_CLASSES)
        c = Client()
        response = c.get(reverse('home'))
        self.assertContains(response, 'Requests')
        self.assertIn('last_requests', response.context)

    def test_context_processors(self):
        from django_hello_world.settings import TEMPLATE_CONTEXT_PROCESSORS
        self.assertIn('django_hello_world.hello.context_processors.settings', TEMPLATE_CONTEXT_PROCESSORS)
        c = Client()
        response = c.get(reverse('home'))
        self.assertIn('settings', response.context)

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
        self.assertIn('form', response.context)

    def test_calendar(self):
        from django_hello_world.hello.widgets import CalendarWidget

    def test_admintag(self):
        from django_hello_world.hello.templatetags.admintags import edit_link