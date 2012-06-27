import random
from unittest import SkipTest

from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase
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
        response = c.get(reverse('requests'))
        self.assertContains(response, 'Requests')
        self.assertIn('requests', response.context)
        c.get(reverse('home'))
        request = Request.objects.order_by('-logged_date')[0]
        self.assertEqual(request.path, reverse('home'))
        self.assertEqual(request.method, 'GET')
        c.post(reverse('requests'))
        request = Request.objects.order_by('-logged_date')[0]
        self.assertEqual(request.path, reverse('requests'))
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
        activity = Activity.objects.order_by('-date_logged')[0]
        self.assertEqual(activity.content_object, request)
        self.assertEqual(activity.operation, 'C')
        request.method = 'POST'
        request.save()
        activity = Activity.objects.order_by('-date_logged')[0]
        self.assertEqual(activity.content_object, request)
        self.assertEqual(activity.operation, 'U')
        request_id = request.id
        request.delete()
        activity = Activity.objects.order_by('-date_logged')[0]
        self.assertEqual(activity.object_id, str(request_id))
        self.assertEqual(activity.operation, 'D')

    def test_priority(self):
        r = Request()
        r.method = 'GET'
        r.path = '/'
        r.save()
        self.assertEqual(r.priority, 0)


class SeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
    	try:
            from selenium.webdriver import Chrome
        except ImportError:
            raise SkipTest
        from selenium.common.exceptions import WebDriverException
        try:
            cls.selenium = Chrome()
        except WebDriverException:
            raise SkipTest
        super(SeleniumTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SeleniumTest, cls).tearDownClass()
        cls.selenium.quit()

    def test_login(self):
	from selenium.webdriver.support.wait import WebDriverWait
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username = self.selenium.find_element_by_name('username')
        username.send_keys('admin')
        password = self.selenium.find_element_by_name('password')
        password.send_keys('admin')
        self.selenium.find_element_by_xpath(
            '//input[@value="Log in"]').click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        pk = Owner.objects.get(active=True).id
        
        self.selenium.get(
            '%s%s' % (self.live_server_url, 
                      reverse('edit_owner', kwargs={'pk': pk})))
        self.selenium.find_element_by_name('birthday').click()
        dp = self.selenium.find_element_by_id('ui-datepicker-div')
        self.assert_(dp.is_displayed())
