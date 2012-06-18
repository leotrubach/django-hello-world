import random

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from .models import Owner, Request
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
        c.get(reverse('home'))
        request = Request.objects.order_by('-logged_date')[0]
        self.assertEqual(request.path, reverse('home'))
        self.assertEqual(request.method, 'GET')
        c.post(reverse('last_requests'))
        request = Request.objects.order_by('-logged_date')[0]
        self.assertEqual(request.path, reverse('last_requests'))
        self.assertEqual(request.method, 'POST')

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

    def test_command(self):
        from django.core.management import call_command
        from StringIO import StringIO

        def parse_line(s):
            model_name, count = (c.strip() for c in s.split(':'))
            return model_name, int(count)

        def run_and_parse_output():
            command_output = StringIO()
            error_output = StringIO()
            call_command(
                'modelcount',
                stdout=command_output,
                stderr=error_output)
            command_output.seek(0)
            error_output.seek(0)
            std_list = command_output.readlines()
            err_list = error_output.readlines()

            self.assertEqual(len(std_list), len(err_list))
            for i in range(len(std_list)):
                self.assertEqual('error: ' + std_list[i], err_list[i])
            return dict([parse_line(s) for s in std_list])

        c = Client()
        count_before = run_and_parse_output()
        c.get(reverse('home'))
        count_after = run_and_parse_output()
        self.assertEqual(
            count_before['hello.request'] + 1,
            count_after['hello.request'])

    def test_signal(self):
        from .models import Activity
        c = Client()
        c.get(reverse('home'))
        request = Request.objects.order_by('-logged_date')[0]
        request_id = request.id
        activity = Activity.objects.order_by('-date_logged')[0]
        self.assertEqual(activity.object_pk, str(request_id))
        self.assertEqual(activity.operation, 'C')
        request.method = 'POST'
        request.save()
        activity = Activity.objects.order_by('-date_logged')[0]
        self.assertEqual(activity.object_pk, str(request_id))
        self.assertEqual(activity.operation, 'U')
        request.delete()
        activity = Activity.objects.order_by('-date_logged')[0]
        self.assertEqual(activity.object_pk, str(request_id))
        self.assertEqual(activity.operation, 'D')

    def test_priority(self):
        c = Client()
        for i in range(25):
            c.get(reverse('home'), {'priority': 0})
        last_request = Request.objects.order_by('-logged_date')[0]
        response = c.get(reverse('last_requests'), {'priority': 1})
        self.assertIn(last_request, response.context['last_requests'])
        first_request = Request.objects.order_by('logged_date')[0]
        response = c.get(reverse('last_requests'), {'priority': 0})
        self.assertIn(first_request, response.context['last_requests'])
