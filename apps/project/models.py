from django.db import models
from django.contrib.auth.models import User

import md5

class Project(models.Model):
    " Projekt "

    creator = models.ForeignKey(User)
    
    name = models.TextField()
    title = models.TextField()
    description = models.TextField()
    
    date_modified = models.DateTimeField( auto_now = True )
    date_added =  models.DateTimeField( auto_now_add = True )
    
    members = models.ManyToManyField(User, related_name = 'projects')
    
    def get_secret(self):
        return md5.md5('%r-%r-8h9ub9u7v8g(&Gagwu4vabiudsnc8a9)' % (self.name,self.date_added) ).hexdigest()
        
    def get_absolute_url(self):
        return 'http://doyrwork.com/p/%s/' % self.name
    
    def __unicode__(self):
        return self.title

class Invitation(models.Model):
    " Zaproszenie do projektu "
    
    creator = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    
    date_added =  models.DateTimeField( auto_now_add = True )
    
    email = models.TextField()
    