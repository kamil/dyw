from django.shortcuts import render_to_response
from dyw.apps.project import util as project_u
from dyw.apps.project.models import Project
from dyw.apps.task.models import Task
from dyw.apps.milestone.models import Milestone
from django.http import HttpResponse, HttpResponseRedirect
from dyw.apps.project import forms as project_f
from dyw.contrib.render import render,Redirect,projectize

@render()
def list(request):
    " Projekty "
    
    print '%r' % dir(request)
    
    projects_all = Project.objects.all()
    projects = []
    
    
    # tylko dla teamu i zalozyciela
    for project in projects_all:
        if request.user in project.members.all() or project.creator == request.user:
            projects.append(project)
    
    for project in projects:
        project.milestones = Milestone.objects.filter(project=project)
        
        for milestone in project.milestones:
            milestone.count_tickets = Task.objects.filter(milestone=milestone).count()
            milestone.closed_tickets = Task.objects.filter(milestone=milestone, status = 3 ).count()
            
    
    return {
        'page_name' : 'projects',
        'projects' : projects,
    }
    
def start_redirect(request,project):
    " Redirect ze strony glownej projektu na wybrana "
    project = project_u.get_project(project)
    return HttpResponseRedirect("/p/%s/wiki/Start/" % project.name )

@render()
def new(request):
    " Dodawanie nowego projektu "
    
    # @TODO: Dorobic validacje nazwy, tylko - bez spacji..
    
    form = project_f.NewProjectForm(request.POST if request.POST else None)
    
    if request.method == "POST" and form.is_valid():
        project = Project(
            creator = request.user,
            name  = form.cleaned_data.get('name'),
            title = form.cleaned_data.get('title'),
            description = form.cleaned_data.get('description'), 
        )
        project.save()
        
        project.members.add(request.user)
        
        request.user_success('Dodano nowy projekt')
        
        request.user.add_row_perm(project,'admin')
        
        raise Redirect('/projects/')

    return {
        'page_name' : 'projects',
        'form' : form
    }


@projectize()
@render()
def edit(request,project):
    " Edytowanie projektu "
    
    if not request.user.has_row_perm(project,'admin'):
        request.user_error('Nie masz uprawnien do edycji projektu')
        raise Redirect('/p/%s/' % project.name)
    
    
    form = project_f.EditProjectForm(request.POST if request.POST else {
        'title' : project.title,
        'secret' : project.get_secret(),
        'name' : project.name,
        'description' : project.description
    })
    
    return {
        'form' : form,
        'page_name' : 'edit',
        'project' : project
    }

@projectize()
@render()
def backup(request,project):
    return {
        'project' : project
    }
    
    