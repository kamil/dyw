# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from dyw.apps.task.models import Task,Comment
from dyw.apps.milestone.models import Milestone
from django.contrib.auth.models import User

from dyw.apps.project import util as project_u
from dyw.apps.timeline import models as timeline_m

import datetime


# TODO: Przenosimy feedy do konkretnych aplikacji i nazywamy feed.py, tutaj tylko import

# /rss/timeline/[project_name]/[key]/
class TimelineFeed(Feed):
    
    def get_object(self, bits):
        try:
            project = project_u.get_project(bits[0])
        except:
            raise FeedDoesNotExist
            
        if project.get_secret() != bits[1]:
            raise FeedDoesNotExist
        
        return project
    
    def title(self,obj):
        return obj.title

    def description(self,obj):
        return "Aktywność projektu"

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self,obj):
        return timeline_m.Event.objects.filter(project=obj,date_added__gt=datetime.datetime.now()-datetime.timedelta(hours=24) ).order_by('-date_added')[:25],

    # ????
    #def item_pubdate(self,obj):
    #    return obj.date_added
    
    def item_link(self,obj):
        return ''
        
# /rss/tasks/[project_name]/[key]/
class TasksFeed(Feed):
    
    author_link = 'http://www.example.com/' 
    
    def get_object(self, bits):
        try:
            project = project_u.get_project(bits[0])
        except:
            raise FeedDoesNotExist
            
        if project.get_secret() != bits[1]:
            raise FeedDoesNotExist
        
        
        
        return project
        #return Task.objects.filter( milestone__in = Milestone.objects.filter(project = project) )

    def title(self,obj):
        return obj.title
    
    def description(self,obj):
        return "Najnowsze zadania"
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def items(self,obj):
        return Task.objects.filter( milestone__in = Milestone.objects.filter(project = obj) ).order_by('-date_added')[:5]
    
    def item_pubdate(self,obj):
        return obj.date_added
        
        
# /rss/tasks_assigned/[project_name]/[user_id]/[key]/       
class TasksAssignedFeed(Feed):

    author_link = 'http://www.example.com/'
    

    def get_object(self, bits):
        
        try:
            project = project_u.get_project(bits[0])
        except:
            raise FeedDoesNotExist

        if project.get_secret() != bits[2]:
            raise FeedDoesNotExist

        try:
            user = User.objects.get(pk=int(bits[1]))
        except:
            raise FeedDoesNotExist
            
        self.user = user
        
        return project
        #return Task.objects.filter( milestone__in = Milestone.objects.filter(project = project) )

    def title(self,obj):
        return obj.title

    def description(self,obj):
        return "Nowo przypisane do mnie"

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self,obj):
        return Task.objects.filter( milestone__in = Milestone.objects.filter(project = obj), assigned = self.user ).order_by('-date_modified')[:5]

    def item_pubdate(self,obj):
        return obj.date_added