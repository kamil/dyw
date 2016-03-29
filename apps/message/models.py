from django.db import models
from django.contrib.auth.models import User
from dyw.apps.project.models import Project

class Message(models.Model):
    
    PRIORITY = (
        (0,'low'),
        (1,'normal'),
        (2,'high'),
        (3,'urgent') 
    )
    
    creator = models.ForeignKey(User, related_name = 'creator')
    project = models.ForeignKey(Project)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY)
    
    title = models.TextField()
    description = models.TextField()
    
    date_modified = models.DateTimeField( auto_now = True )
    date_added =  models.DateTimeField( auto_now_add = True ) 

    engage = models.ManyToManyField(User, related_name = 'engage')
    