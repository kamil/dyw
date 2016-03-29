from django.shortcuts import render_to_response
from dyw.apps.project.models import Project
from dyw.apps.milestone.models import Milestone
from dyw.apps.task.models import Task
from dyw.apps.task import models as task_m

from dyw.contrib.render import render,Redirect

@render()
def project(request,project):
    " Pokazuje tablice dla okreslonego projektu "
    
    return {
        'project' : project,
        'page_name' : 'dashboard'
    }


@render()
def show(request):
    " Pokazuje glowna strone tablicy uzytkownika "
    
    
    
    # @TODO: To nie moze tak wygladac :)
    
    closed_statuses = [item.id for item in task_m.Status.objects.filter(status=1)]
    
    tasks_assigned = task_m.Task.objects.filter( assigned = request.user ).exclude( status__in = closed_statuses ).order_by('-date_modified')
    tasks_createdby = task_m.Task.objects.filter( creator = request.user ).exclude( status__in = closed_statuses ).order_by('-date_added')
    tasks_assigned_closed_count =  task_m.Task.objects.filter( assigned = request.user ).filter( status__in = closed_statuses ).count()
    tasks_createdby_closed_count = task_m.Task.objects.filter( creator  = request.user ).filter( status__in = closed_statuses ).count()
    
    projects = Project.objects.all()
    
    observe = request.user.observers.all()
    
    return {
        'projects' : projects,
        'tasks_assigned' : tasks_assigned,
        'tasks_createdby' : tasks_createdby,
        'tasks_assigned_closed_count' : tasks_assigned_closed_count,
        'tasks_createdby_closed_count' : tasks_createdby_closed_count,
        'page_name' : 'dashboard'
    }