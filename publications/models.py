from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import admin

RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class Publication(models.Model):
    title = models.TextField(unique=True)
    description = models.TextField()
    added = models.DateTimeField(default=datetime.now)
    owner = models.ForeignKey(User, related_name='owner_publication_set')
    readers = models.ManyToManyField(User, through='Reading', related_name='reader_publication_set')

    def __unicode__(self):
        return self.title

class Reading(models.Model):
    user = models.ForeignKey(User)
    publication = models.ForeignKey(Publication)
    readDate = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = ('user', 'publication')

    def __unicode__(self):
        return '%s has read %s' % (self.user.username, self.publication)

class Quote(models.Model):
    text = models.TextField()
    publication = models.ForeignKey(Publication)
    added = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ('publication', 'text')

    def __unicode__(self):
        return self.text

admin.site.register(Publication)
admin.site.register(Reading)
admin.site.register(Quote)
