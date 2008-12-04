from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Publication(models.Model):
    description = models.TextField()
    added = models.DateTimeField(default=datetime.now)
    title = models.TextField()
    owner = models.ForeignKey(User)    

    def __unicode__(self):
        return self.title
    

class Quote(models.Model):
    text = models.TextField()
    publication = models.ForeignKey(Publication)
    added = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.text
