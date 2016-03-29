# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from dyw.apps.task import models as task_m
from dyw.apps.project import util as project_u
from django.contrib.auth.models import User

# /rss/task/[project_name]/[task_id]/[key]/   
class TaskFeed(Feed):
    
    def get_object(self, bits):
        
        try:
            project = project_u.get_project(bits[0])
        except:
            raise FeedDoesNotExist

        if project.get_secret() != bits[2]:
            raise FeedDoesNotExist

        try:
            task = task_m.Task.objects.get(pk=int(bits[1]))
        except:
            raise FeedDoesNotExist
            
        self.task = task
        
        return project
        
    def title(self,obj):
        return obj.title

    def description(self,obj):
        return "Zadanie %s" % self.task.title

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self,obj):
        return task_m.Comment.objects.filter(task=self.task).order_by('-date_added')[:5]

    def item_pubdate(self,obj):
        return obj.date_added