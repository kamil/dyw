from django.shortcuts import render_to_response
from dyw.apps.project import util as project_u
from dyw.apps.timeline import models as timeline_m
from dyw.contrib.render import render,Redirect,projectize

import datetime

@projectize()
@render()
def list(request,project):
    " Simple project timeline "
    
    return {
        'project' : project,
        'events' : timeline_m.Event.objects.filter(project=project,date_added__gt=datetime.datetime.now()-datetime.timedelta(hours=24) ).order_by('-date_added'),
        'page_name' : 'timeline'
    }