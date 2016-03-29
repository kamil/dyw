from django.shortcuts import render_to_response
from dyw.apps.project import util as project_u
from dyw.apps.files import util as files_u
from django.http import HttpResponse, HttpResponseRedirect

from dyw.contrib.render import render,Redirect,projectize

@projectize()
@render()
def list(request,project):
    " Pliki "
    
    return {
        'project' : project,
        'files' : files_u.get_attachments('project',project.id),
        'page_name' : 'files'
    }

@projectize()
@render()
def add(request,project):
    " Dodanie nowego "

    if request.method == 'POST' and request.FILES.get('file',False):
        _file = request.FILES.get('file')
    
        files_u.attach_file('project',project.id,request.user,_file['filename'],_file['content'])
        
        # TODO: Nie robimy takich redirectow, wprowadzamy url-names
        raise Redirect('/p/%s/files/' % project.name)

    return {
        'project' : project,
        'page_name' : 'files'
    }