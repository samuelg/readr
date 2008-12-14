from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class Publication(models.Model):
    description = models.TextField()
    added = models.DateTimeField(default=datetime.now)
    title = models.TextField()
    owner = models.ForeignKey(User, related_name='owner_publication_set')
    readers = models.ManyToManyField(User, through='Reading', related_name='reader_publication_set')

    def __unicode__(self):
        return self.title

class Reading(models.Model):
    user = models.ForeignKey(User)
    publication = models.ForeignKey(Publication)
    readDate = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __unicode__(self):
        return '%s has read %s' % (self.user.username, self.publication)

class Quote(models.Model):
    text = models.TextField()
    publication = models.ForeignKey(Publication)
    added = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.text
