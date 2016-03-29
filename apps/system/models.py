from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User)
    message = models.TextField()
    
    date_added = models.DateTimeField( auto_now_add = True )
    
    
class FromMail(models.Model):
    to = models.TextField()
    sender = models.TextField()
    subject = models.TextField()
    body = models.TextField()
    
    date_added = models.DateTimeField( auto_now_add = True )
    