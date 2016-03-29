from django.db import models
from django.contrib.auth.models import User
import pickle
from docutils.core import publish_parts

from dyw.apps.milestone.models import Milestone
from dyw.apps.project.models import Project

from dyw.apps.user.const import MARKUP_SELECT

import textile

class Type(models.Model):
    project = models.ForeignKey(Project)
    date_added = models.DateTimeField( auto_now_add = True )
    
    title = models.TextField()
    
class Priority(models.Model):
    project = models.ForeignKey(Project)
    date_added = models.DateTimeField( auto_now_add = True )
    
    title = models.TextField()
    no = models.PositiveSmallIntegerField(null=True)

class Status(models.Model):
    project = models.ForeignKey(Project)
    date_added = models.DateTimeField( auto_now_add = True )
    
    title = models.TextField()
    status = models.PositiveSmallIntegerField(choices=((0,'visible'),(1,'hidden')))

class Tag(models.Model):
    " tagi :) "

    project = models.ForeignKey(Project)
    name = models.TextField()
    description = models.TextField( blank = True )
    date_added = models.DateTimeField( auto_now_add = True )


class Task(models.Model):
    " Zadanie "
    
    creator = models.ForeignKey(User)
    assigned = models.ForeignKey(User,related_name='assigned', null=True)
    project = models.ForeignKey(Project)
    milestone = models.ForeignKey(Milestone)
    
    observers = models.ManyToManyField(User, related_name='observers')
    tags = models.ManyToManyField(Tag, related_name='tasks')
    
    title = models.TextField()
    
    in_type = models.ForeignKey(Type)
    priority = models.ForeignKey(Priority)
    status = models.ForeignKey(Status)
    
    date_added = models.DateTimeField( auto_now_add = True )
    date_modified = models.DateTimeField( auto_now = True )
    
    def get_absolute_url(self):
        return "http://doyrwork.com/p/%s/tasks/%d/" % (self.milestone.project.name,self.id)
        
    def __unicode__(self):
        return "#%d %s" % (self.id,self.title)
    

    def is_closed(self):
        return self.status.status == 1


class Comment(models.Model):
    " Komentarz do zadania "
    
    creator = models.ForeignKey(User)
    task = models.ForeignKey(Task)

    comment = models.TextField()
    
    change_info = models.TextField(null=True)
    
    date_added =  models.DateTimeField( auto_now_add = True )
    
    markup = models.PositiveSmallIntegerField(choices=MARKUP_SELECT,default=0)
    

    def get_comment(self):
        " Pobiera tresc komenarza "
        
        return publish_parts(self.comment, writer_name='html').get('html_body','')
            
        #if self.markup == 1:
        #    #print textile.textile(self.comment, encoding='utf-8')
        #    return textile.textile(str(self.comment).encode('utf-8'), encoding='utf-8')


    def get_changes(self):
        try:
            return pickle.loads(self.change_info)
        except:
            return {}
            
    def set_changes(self,change):
        self.change_info = pickle.dumps(change)

    changes = property(get_changes,set_changes)
    


