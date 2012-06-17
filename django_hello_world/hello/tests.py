from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django_hello_world.settings import MIDDLEWARE_CLASSES


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
        from django_hello_world.settings import TEMPLATE_CONTEXT_PROCESSORS
        self.assertIn('django_hello_world.hello.context_processors.add_settings', TEMPLATE_CONTEXT_PROCESSORS)
        c = Client()
        response = c.get(reverse('home'))
        self.assertIn('settings', response.context)
