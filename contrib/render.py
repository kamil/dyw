# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from dyw.apps.project import util as project_u

import re

class RenderException(Exception):
    def run(self):
        pass

class Redirect(RenderException):
    def __init__(self, url):
        if not url:
            raise RenderException('No url specified in redirect!')
        self.url = url
    def run(self):
        return HttpResponseRedirect(self.url)
        
def projectize():
    def decorator(view):
        def _wrapper(request, *args, **kwargs):
            if kwargs.get('project',False):
                
                try:
                    project = project_u.get_project(kwargs['project'])
                except:
                    request.user_error('Nie ma takiego projektu')
                    return HttpResponseRedirect('/')
                
                if User.objects.get(pk=request.user.id) not in project.members.all():
                    request.user_error('Nie jestes w zespole %s' % project.name)
                    return HttpResponseRedirect('/')
                
                
                kwargs['project'] = project
                
            return view(request, *args, **kwargs)
        return _wrapper
    return decorator

def render(template = None,**options):
    def decorator(view):
        
        view_app_template = ''.join([re.search('([^.]+)[.]views', view.__module__).group(1),'/',view.__name__,'.html'])
        
        def _wrapper(request, *args, **kwargs):
            template_name = template
            render_options = options
            context = {}
            
            try:
                context = view(request, *args, **kwargs)
            except RenderException, e:
                return e.run()
            else:
                if isinstance(context, (list, tuple)):
                    template_name, context = context

            # @TODO: Przerobic na RequestContext
            context['user_messages'] = request.get_user_messages()
            context['user'] = request.user
            context['request'] = request

            if template_name:
                return render_to_response("%s.html" % template_name,context)
            else:
                return render_to_response("%s" % view_app_template,context)
                    
        return _wrapper
    return decorator
