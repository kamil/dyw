from django.shortcuts import render_to_response
from dyw.apps.project import util as project_u
from dyw.apps.wiki import util as wiki_u
from dyw.apps.wiki import models as wiki_m
from dyw.apps.timeline import events
from django.http import HttpResponse, HttpResponseRedirect

from dyw.contrib.render import render,Redirect,projectize

@projectize()
@render()
def show(request,project,page):
    " Pokazuje najnowsza rewizje strony "
    
    page = wiki_u.get_page(project,page)
    
    sub_pages = wiki_m.Page.objects.filter(project=project, name__startswith = page.name).exclude(id=page.id)
    
    print sub_pages
    
    count_revision = page.count_revisions()
    
    if not page.date_added: # strona nie istnije
        return ('wiki/show_empty',{
            'project' : project,
            'page' : page
        })

    last_revision = page.get_last_revision()
  
    pages = wiki_u.get_by_project(project)
    
    for p in pages:
        if p.id == page.id:
            p.active = True
        else:
            p.active = False
  
    return {
        'project' : project,
        'page' : page,
        'revision' : last_revision,
        'pages' : pages,
        'page_name' : 'wiki',
        'count_revision' : count_revision,
        'sub_pages' : sub_pages
    }

@projectize()
@render()
def edit(request,project,page):
    " Edycja "
    
    page = wiki_u.get_page(project,page)
    
    last_revision = page.get_last_revision()
    
    count_revision = page.count_revisions()
    
    if request.method == "POST":
        
        first_revision = False
        
        if not page.date_added:
            page.creator = request.user
            first_revision = True
        
        if request.POST.get('title'):
            page.title = request.POST.get('title')
        
        page.save()
        
        if first_revision:
            events.event_wiki_created(request.user,page)
            request.user_success('Strona utworzona')
        
        
        if last_revision.content != request.POST.get('body'):
            new_revision = wiki_m.PageRevisions(
                creator = request.user,
                page = page,
                content = request.POST.get('body'),
                comment = request.POST.get('comment')
            )
            new_revision.save()
            
            if not first_revision:
                events.event_wiki_changed(request.user,page,new_revision)
                request.user_success('Strona zmieniona')
            
        raise Redirect('/p/%s/wiki/%s/' % (project.name,page.name))
    
    return {
        'project' : project,
        'page' : page,
        'revision' : last_revision,
        'count_revision' : count_revision,
        'page_name' : 'wiki',
        'user_messages' : request.get_user_messages()
    }

@projectize()
@render()
def diff(request,project,page):
    " Pokazanie roznicy miedzy stronami"
    return {}

@projectize()
@render()
def attach(request,project,page):
    " Dolacznie pliku "
    return {}