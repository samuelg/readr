from django.test import TestCase
from publications.models import Publication

class PublicationTestCase(TestCase):
    fixtures = ['publications']
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPublication(self):
        pub = Publication.objects.get(pk=1)
        self.assertEquals(pub.title, 'something')


