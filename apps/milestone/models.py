from django.db import models
from django.contrib.auth.models import User


from dyw.apps.project.models import Project

class Milestone(models.Model):
    
    creator = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    
    title = models.TextField()
    description = models.TextField()
    
    date_due = models.DateTimeField( blank = True )
    date_modified = models.DateTimeField( auto_now = True )
    date_added =  models.DateTimeField( auto_now_add = True ) 

    