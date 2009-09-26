from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from publications.models import Publication, Reading
from publications.forms import ReadingForm, PublicationForm
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
        self.template_dir = 'publications/'

    def testLatestViewAnonymous(self):
        """ Ensures that the latest view works properly when anonymous """
        response = self.client.get(reverse('pub_latest'))
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
        
    def testLatestViewAuthenticated(self):
        """ Ensures that the latest view works properly when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('pub_latest'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['publications'].object_list[1][1]),
                          type(Reading()))

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
        self.assertEquals(response.template[0].name, '%s%s' % (self.template_dir, 'view.html'))        
        
    def testViewViewAuthenticated(self):
        """ Ensures that the view view works properly when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('pub_view', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['reading']),
                          type(Reading()))

    def testViewViewNotFound(self):
        """ Ensures the view view returns 404 for unknown publications """
        response = self.client.get(reverse('pub_view', args=[100]))
        self.assertEquals(response.status_code, 404)
        
    def testReadsViewAnonymous(self):
        """ Ensures that the reads view works properly when anonymous """
        response = self.client.get(reverse('pub_reads', args=['samuel']))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context[-1].get('header', None), 'Your reads')
        self.assertEquals(type(response.context[-1]['publications'].object_list[0][0]),
                          type(Publication()))
        self.assertEquals(response.context[-1]['publications'].object_list[1][1], None)
        self.assertEquals(type(response.context[-1]['reading_form']),
                          type(ReadingForm()))
        self.assertTrue(response.context[-1].get('MEDIA_URL', None))
        self.assertTrue(response.context[-1].get('user', None))
        self.assertEquals(response.template[0].name, '%s%s' % (self.template_dir, 'latest.html'))
        
    def testReadsViewAuthenticated(self):
        """ Ensures that the reads view works properly when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('pub_reads', args=['samuel']))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['publications'].object_list[1][1]),
                          type(Reading()))
        
    def testReadsViewNotFound(self):
        """ Ensures the reads view returns 404 for unknown usernames """
        response = self.client.get(reverse('pub_reads', args=['doesnotexist']))
        self.assertEquals(response.status_code, 404)

    def testCreateViewAnonymous(self):
        """ Ensures the create view redirects to login when anonymous """
        response = self.client.get(reverse('pub_create'), follow=True)
        self.assertEquals(response.redirect_chain[0][0],
                          '%s%s?next=%s' %
                          (TEST_SERVER_URL, settings.LOGIN_URL, reverse('pub_create')))

    def testCreateViewGetAuthenticated(self):
        """ Ensures the create view works properly with a GET when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.get(reverse('pub_create'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(type(response.context[-1]['form']),
                          type(PublicationForm()))
        self.assertTrue(response.context[-1].get('MEDIA_URL', None))
        self.assertTrue(response.context[-1].get('user', None))
        self.assertEquals(response.template[0].name, '%s%s' % (self.template_dir, 'create.html'))

    def testCreateViewPostAuthenticated(self):
        """ Ensures the create view works properly with a POST when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.post(reverse('pub_create'), {
            'title': 'unittest',
            'description': 'unit test book',
            'rating': 5
            }, follow=True)
        self.assertEquals(response.status_code, 200)
        # should redirect to latest view after creation
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('pub_latest')))
        # make sure the publication was created
        pub = Publication.objects.get(title='unittest')
        self.assertTrue(pub)

    def testReadViewAnonymous(self):
        """ Ensures the read view redirects to login when anonymous """
        response = self.client.get(reverse('pub_read', args=[1]), follow=True)
        self.assertEquals(response.redirect_chain[0][0],
                          '%s%s?next=%s' %
                          (TEST_SERVER_URL, settings.LOGIN_URL, reverse('pub_read', args=[1])))
        
    def testReadViewPostAuthenticated(self):
        """ Ensures the read view works properly with a POST when authenticated """
        self.client.login(username='samuel', password='testing')
        response = self.client.post(reverse('pub_read', args=[12]), {
            'rating': 5
            }, follow=True)
        self.assertEquals(response.status_code, 200)
        # should redirect to latest view after reading
        self.assertEquals(response.redirect_chain[0][0], '%s%s' % (TEST_SERVER_URL, reverse('pub_latest')))
        # make sure the reading was created
        user = User.objects.get(username='samuel')
        pub = Publication.objects.get(pk=12)
        reading = Reading.objects.get(user=user, publication=pub)
        self.assertTrue(reading)

    def testReadViewNotFound(self):
        """ Ensures the read view returns 404 for unknown publications """
        self.client.login(username='samuel', password='testing')
        response = self.client.post(reverse('pub_read', args=[100]), {
            'rating': 5 
            })
        self.assertEquals(response.status_code, 404)
        
    def testReadViewAlreadyRead(self):
        """ Ensures the read view returns 404 for already read publications """
        self.client.login(username='samuel', password='testing')        
        response = self.client.post(reverse('pub_read', args=[1]), {
            'rating': 5 
            })
        self.assertEquals(response.status_code, 404)
