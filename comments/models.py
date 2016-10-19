from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class ContentURL(models.Model):
    url = models.CharField(max_length=200)
    
    def  __str__(self):
        return self.url

class Comment(models.Model):
    username = models.ForeignKey(User) 
    comment = models.TextField()
    content_url = models.ForeignKey(ContentURL)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def  __str__(self):
        return self.comment[:20]
