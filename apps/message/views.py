from django.shortcuts import render_to_response
from dyw.apps.project import util as project_u
from dyw.apps.message.models import Message
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from dyw.contrib.render import render,Redirect,projectize

@projectize()
@render()
def list(request,project):
    " Komunikaty "

    return {
        'project' : project,
        'messages' : Message.objects.filter(project=project),
        'page_name' : 'messages'
    }

@projectize()
@render()
def new(request,project):
    " Nowy komunikat "

    if request.method == 'POST':
        message = Message(
            creator = request.user,
            project = project,
            priority = request.POST.get('priority',1),
            title = request.POST.get('title'),
            description = request.POST.get('description'),
        )
        message.save()
        
        if request.POST.get('users'):
            for user in request.POST.get('users').split(','):
                message.engage.add(User.objects.get(pk=user))
        return HttpResponseRedirect("/p/%s/messages/" % project.name)
    
    return {
        'project' : project,
        'users' : project.members.all(),
        'priority' : Message.PRIORITY,
        'page_name' : 'messages'
    }
    