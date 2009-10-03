from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from users.forms import LoginForm, RegisterForm
import settings
from datetime import datetime, timedelta

TEST_SERVER_URL = 'http://testserver'

class AuthViewsTestCase(TestCase):

    def setUp(self):
        user = User(pk=1, username='samuel')
        user.set_password('testing')
        user.save()
        self.template_dir = 'users/'

    def testLoginUserViewGetAnonymous(self):
        """ Ensures that the login user view works properly with a GET when anonymous """
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['form']),
                          type(LoginForm()))
        self.assertTrue(response.context[-1].get('MEDIA_URL', None))    
        self.assertTrue(response.context[-1].get('user', None))
        self.assertEquals(response.template[0].name, '%s%s' % (self.template_dir, 'login.html'))

    def testLoginUserViewPostAnonymous(self):
        """ Ensures that the login user view works properly with a POST when anonymous """
        response = self.client.post(reverse('login'), {'user_id': 'samuel', 'password': 'testing', 'remember': False}, follow=True)
        self.assertEquals(response.status_code, 200)
        # should redirect to latest publications after login
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('pub_latest')))
        user = User.objects.get(username='samuel')
        # make sure user was logged in
        self.assertEquals(response.context[-1].get('user', None), user)

    def testLoginUserRememberMeEnabled(self):
        """ Ensures that the login user view works properly with remember me enabled """
        response = self.client.post(reverse('login'), {'user_id': 'samuel', 'password': 'testing', 'remember': True})
        self.assertEquals(response.client.session.get_expire_at_browser_close(), False)
        self.assertEquals(response.client.session.get_expiry_date().strftime('%Y%m%d'), (datetime.now() + timedelta(days=14)).strftime('%Y%m%d'))
        
    def testLoginUserRememberMeDisabled(self):
        """ Ensures that the login user view works properly with remember me disabled """
        response = self.client.post(reverse('login'), {'user_id': 'samuel', 'password': 'testing'})
        self.assertEquals(response.client.session.get_expire_at_browser_close(), True)

    def testLoginUserViewAuthenticated(self):
        """ Ensures that the login user view works properly when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('login'), follow=True)
        # should redirect to latest publications
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('pub_latest')))

    def testLogoutUserViewGetAuthenticated(self):
        """ Ensures that the logout user view works properly with a GET when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('logout'), follow=True)
        # should redirect to latest publications
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('pub_latest')))
        # make sure user was logged out
        self.assertEquals(response.context[-1].get('user', None), AnonymousUser())
        # make sure session expiry was reset
        self.assertEquals(response.client.session.get_expire_at_browser_close(), True)

    def testLogoutUserViewPostAuthenticated(self):
        """ Ensures that the logout user view works properly with a POST when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.post(reverse('logout'), {}, follow=True)
        # should redirect to latest publications
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('pub_latest')))
        # make sure user was logged out
        self.assertEquals(response.context[-1].get('user', None), AnonymousUser())
        # make sure session expiry was reset
        self.assertEquals(response.client.session.get_expire_at_browser_close(), True)

    def testLogoutUserViewAnonymous(self):
        """ Ensures that the logout user view works properly when anonymous """
        response = self.client.get(reverse('logout'), follow=True)
        # should redirect to latest publications
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('pub_latest')))
        # make sure session expiry was reset
        self.assertEquals(response.client.session.get_expire_at_browser_close(), True)

    def testRegisterUserViewGetAnonymous(self):
        """ Ensures that the register user view works properly with a GET when anonymous """
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['form']),
                          type(RegisterForm()))
        self.assertTrue(response.context[-1].get('MEDIA_URL', None))    
        self.assertTrue(response.context[-1].get('user', None))
        self.assertEquals(response.template[0].name, '%s%s' % (self.template_dir, 'register.html'))

    def testRegisterUserViewPostAnonymous(self):
        """ Ensures that the register user view works properly with a POST when anonymous """
        response = self.client.post(reverse('register'), {
                'user_id': 'samuelnew', 'password': 'testing',
                'password_confirm': 'testing', 'email': 'samuel@email.com'
            }, follow=True)
        self.assertEquals(response.status_code, 200)
        # should redirect to login after registration
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('login')))
        # make sure user was created
        user = User.objects.get(username='samuelnew')
        self.assertTrue(user)

    def testRegisterUserViewAuthenticated(self):
        """ Ensures that the register user view works properly when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('register'), follow=True)
        # should redirect to latest publications
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('pub_latest')))
