from django.db import models
from django.contrib.auth.models import User
from dyw.apps.project.models import Project
from django.template.loader import render_to_string

EVENT_TYPES = [
    # wiki
    'wiki-changed','wiki-created',
    # pliki
    'file-added',
    # etapy
    'milestone-created','milestone-date-changed','milestone-delete','milestone-complete',
    # tickety
    'task-created','task-closed','task-changed',
    # zespol
    'team-add','team-role-changed','team-remove'
]

class Event(models.Model):
    
    event_type = models.PositiveIntegerField( choices = [ (n,value) for n,value in enumerate(EVENT_TYPES) ] )

    project = models.ForeignKey(Project)

    cast_by = models.ForeignKey(User, related_name='cast_by')
    cast_to = models.ForeignKey(User, default=1, related_name='cast_to')
    
    param_first_id = models.IntegerField(default=0)
    param_second_id = models.IntegerField(default=0)
    param_comment = models.TextField(default="")
    param_dict = models.TextField(default="")

    date_added =  models.DateTimeField( auto_now_add = True ) 
    
    def get_absolute_url(self):
        return 'http://doyrwork.com/p/%s/timeline/' % self.project
        
    def __unicode__(self):
        return unicode(self.render('txt'))


"""

if event_name in ['wiki-changed','wiki-created']:
    event_p = {
        'page' : Page.objects.get(pk=self.param_first_id)
    }
elif event_name in ['task-created','task-closed']:
    event_p = {
        'task' : Task.objects.get(pk=self.param_first_id)
    }
elif event_name == 'task-changed':
    
    change = Comment.objects.get(pk=self.param_second_id)
    
    event_p = {
        'task' : Task.objects.get(pk=self.param_first_id),
        'change' : change,
        'info' : change.get_changes() 
    }




"""