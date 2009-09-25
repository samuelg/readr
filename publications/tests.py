from django.test import TestCase
from publications.models import Publication, Reading
from django.contrib.auth.models import User
from django.db import IntegrityError

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

    def testView(self):
        pass
