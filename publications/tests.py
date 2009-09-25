from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from publications.models import Publication, Reading
from publications.forms import ReadingForm
import settings

TEST_SERVER_URL = 'http://testserver'

class ReadingModelTestCase(TestCase):
    fixtures = ['publications']
    
    def setUp(self):
        user = User(pk=1, username='samuel')
        user.save()

    def testReadingUniqueness(self):
        """ Ensures readings are unique """
        pub = Publication.objects.get(pk=1)
        user = User.objects.get(pk=1)
        reading = Reading(publication=pub, rating=1, user=user)
        self.assertRaises(IntegrityError, reading.save)

    def testReadingUnicode(self):
        """ Ensures __unicode__ returns expected output """
        reading = Reading.objects.get(pk=1)
        self.assertEquals(str(reading), 'samuel has read something')

class PublicationModelTestCase(TestCase):
    fixtures = ['publications']

    def testPublicationUnicode(self):
        """ Ensures __unicode__ returns expected output """
        pub = Publication.objects.get(pk=1)
        self.assertEquals(str(pub), 'something')

class PublicationsViewsTestCase(TestCase):
    fixtures = ['publications']

    def setUp(self):
        user = User(pk=1, username='samuel')
        user.set_password('testing')
        user.save()

    def testLatestViewAnonymous(self):
        """ Ensures that the latest view works properly when anonymous """
        response = self.client.get(reverse('pub_latest'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context[-1].get('header', None), 'Latest reads')
        self.assertEquals(type(response.context[-1]['publications'].object_list[0][0]),
                          type(Publication()))
        self.assertEquals(response.context[-1]['publications'].object_list[0][1], None)
        self.assertEquals(type(response.context[-1]['reading_form']),
                          type(ReadingForm()))
        self.assertTrue(response.context[-1].get('MEDIA_URL', None))
        self.assertTrue(response.context[-1].get('user', None))
        
    def testLatestViewAuthenticated(self):
        """ Ensures that the latest view works properly when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('pub_latest'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['publications'].object_list[0][0]),
                          type(Publication()))

    def testRestrictedViews(self):
        """ Ensures restricted views are restricted """
        response = self.client.get(reverse('pub_create'), follow=True)
        self.assertEquals(response.redirect_chain[0][0],
                          '%s%s?next=%s' %
                          (TEST_SERVER_URL, settings.LOGIN_URL, reverse('pub_create')))
        response = self.client.get(reverse('pub_read', args=[1]), follow=True)
        self.assertEquals(response.redirect_chain[0][0],
                          '%s%s?next=%s' %
                          (TEST_SERVER_URL, settings.LOGIN_URL, reverse('pub_read', args=[1])))

    def testViewViewAnonymous(self):
        """ Ensures that the view view works properly when anonymous """
        response = self.client.get(reverse('pub_view', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context[-1]['reading'], None)
        self.assertEquals(type(response.context[-1]['publication']),
                          type(Publication()))
        self.assertEquals(type(response.context[-1]['reading_form']),
                          type(ReadingForm()))
        self.assertTrue(response.context[-1].get('MEDIA_URL', None))
        self.assertTrue(response.context[-1].get('user', None))
        
    def testViewViewAuthenticated(self):
        """ Ensures that the view view works properly when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('pub_view', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['reading']),
                          type(Reading()))
