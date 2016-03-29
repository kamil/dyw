from django.shortcuts import render_to_response
from dyw.apps.project import util as project_u
from dyw.apps.milestone import forms as milestone_f
from dyw.apps.milestone.models import Milestone
from dyw.apps.task.models import Task
from django.http import HttpResponse, HttpResponseRedirect
from dyw.contrib.render import render,Redirect,projectize

@projectize()
@render()
def list(request,project):
    " Etapy "
    
    milestones = Milestone.objects.filter(project=project).order_by('date_due')
    
    for milestone in milestones:
        # tylko otwarte lub przypisane
        milestone.tasks_count = Task.objects.filter(milestone=milestone).count()
        milestone.tasks_count_closed = Task.objects.filter(milestone=milestone,status__in=[2,3] ).count()
        milestone.tasks = Task.objects.filter(milestone=milestone, status__in=[0,1]).order_by('-priority')
        if milestone.tasks_count:
            milestone.complite_percent = int(milestone.tasks_count_closed/float(milestone.tasks_count)*100)
        else:
            milestone.complite_percent = 0
        milestone.complete = milestone.complite_percent == 100
    
    return {
        'project' : project,
        'page_name' : 'milestones',
        'milestones' : milestones
    }
    
@projectize()
@render()
def new(request,project):
    
    milestone_form = milestone_f.NewMilestoneForm(request.POST if request.POST else None)
    
    if request.method == "POST" and milestone_form.is_valid():
        milestone = Milestone(
            creator = request.user,
            project = project,
            
            title = milestone_form.cleaned_data.get('title'),
            description = milestone_form.cleaned_data.get('description'), 
            date_due = milestone_form.cleaned_data.get('date_due')
            
        )
        milestone.save()
        
        request.user_success('Etap dodano')
        
        raise Redirect('/p/%s/milestones/' % project.name)

    return {
        'project' : project,
        'milestone_form' : milestone_form,
        'page_name' : 'milestones'
    }
    
@projectize()
@render()
def tasks(request,project,id):
    
    try:
        milestone = Milestone.objects.get(pk=id)
    except:
        request.error_message('Nie ma takiego etapu')
        raise Redirect('/p/%s/' % project.name)
    
    if not milestone.project == project:
        request.error_message('Milestone nie jest z projektu')
        raise Redirect('/p/%s/' % project.name)
    
    tasks = Task.objects.filter(milestone=milestone)
            
    
    
    return {
        'tasks' : tasks,
        'project' : project,
        'page_name' : 'milestones'
    }