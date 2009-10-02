from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from users.forms import LoginForm, RegisterForm
import settings

TEST_SERVER_URL = 'http://testserver'

class AuthViewsTestCase(TestCase):

    def setUp(self):
        user = User(pk=1, username='samuel')
        user.set_password('testing')
        user.save()
        self.template_dir = 'auth/'

    def testLoginUserViewAnonymous(self):
        """ Ensures that the login user view works properly when anonymous """
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context[-1].get('header', None), 'Latest reads')
        self.assertEquals(type(response.context[-1]['publications'].object_list[0][0]),
                          type(Publication()))
        self.assertEquals(response.context[-1]['publications'].object_list[1][1], None)
        self.assertEquals(type(response.context[-1]['reading_form']),
                          type(ReadingForm()))
        self.assertTrue(response.context[-1].get('MEDIA_URL', None))
        self.assertTrue(response.context[-1].get('user', None))
        self.assertEquals(response.template[0].name, '%s%s' % (self.template_dir, 'latest.html'))        
        
    def testLoginUserViewAuthenticated(self):
        """ Ensures that the login user view works properly when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['publications'].object_list[1][1]),
                          type(Reading()))
