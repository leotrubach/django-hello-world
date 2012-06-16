"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

import django_hello_world.settings as settings

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
        self.assertIn('django_hello_world.hello.middleware.StoreRequestMiddleware', settings.MIDDLEWARE_CLASSES)
        c = Client()
        response = c.get(reverse('home'))
        self.assertContains(response, 'Requests')
        self.assertIn('last_requests', response.context)

    def test_context_processors(self):
        TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS
        self.assertIn('django_hello_world.hello.context_processors.settings', TEMPLATE_CONTEXT_PROCESSORS)
        c = Client()
        response = c.get(reverse('home'))
        self.assertIn('settings', response.context)