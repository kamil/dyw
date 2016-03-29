# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from dyw.apps.project import util as project_u
from dyw.apps.project import models as project_m
from dyw.apps.milestone.models import Milestone
from dyw.apps.task.models import Task,Comment
from dyw.apps.task import models as task_m
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User,SiteProfileNotAvailable
from dyw.apps.user import forms as user_f
from dyw.apps.user import models as user_m
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login

from dyw.contrib.render import render,Redirect,projectize

def user_is_teammate(user,projects):
    for project in projects:
        if user in projects.members.all():
            return True
    return False

@projectize()
@render()
def show(request,user_id = None):
    " Wizytowka uzytkownika "
    
    try:
        display_user = User.objects.get(pk=user_id)
    except:
        request.user_error('Nie ma takiego uzytkownika')
        raise Redirect('/')
        
    
    projects = User.objects.get(pk=request.user.id).projects.all()
    
    
    closed_statuses = [item.id for item in task_m.Status.objects.filter(status=1)]

    
    tasks_open = Task.objects.filter( project__in = projects ).filter( assigned=display_user ).exclude( status__in = closed_statuses ).order_by('-priority')
    
    print tasks_open
    
    
    #common_projects = []
    #
    #for project in projects:
    #    if display_user in project.members.all():
    #        common_projects.extend([t for t in Task.objects.filter(project=project,assigned=display_user)])
    
    return {
        'tasks_open' : tasks_open,
        'suser' : display_user,
        'page_name' : 'user'
    }

@projectize()
@render()
def profile(request):
    " Profil uzytkownika "

    try:
        profile = request.user.get_profile()
    except:
        profile = user_m.UserProfile(user=request.user)
    
    user = request.user
    
    form = user_f.ContactForm(request.POST if request.POST else {
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
        'im_jabber' : profile.options.get('im_jabber'),
        'markup' : profile.options.get('markup')
    })
    
    # Zmiana avatara
    if request.method == 'POST' and request.FILES:
        """
        # przeniesc do modelu ?
        from PIL import Image
        
        
        thumbs = [
            (50,50),(75,75),(400,300)
        ]
        
        org = open("%s/%d_org.jpg" % (settings.AVATARS_DIR,request.user.id),'wb')
        org.write(request.FILES.get('avatar').data)
        org.close()
        
        for size in thumbs:
            img = Image.open("%s/%d_org.jpg" % (settings.AVATARS_DIR,request.user.id))
            img.thumbnail(size, Image.ANTIALIAS)
            img.save('%s/%d_%dx%d.jpg' % (settings.AVATARS_DIR,request.user.id,size[0],size[1]))
        
        
        op = profile.options
        
        op['has_photo'] = True
        
        profile.options = op
        
        profile.save()
        """
    
    # Zmiana profilu
    elif request.method == 'POST' and form.is_valid():
        
        profile.options = {
            'im_jabber' : form.cleaned_data.get('im_jabber'),
            'markup' : form.cleaned_data.get('markup')
        }
        
        profile.company_id = 1
        
        profile.save()
        
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        
        user.email = form.cleaned_data.get('email')
        
        if form.cleaned_data.get('new_password',False):
            user.set_password(form.cleaned_data.get('new_password'))
            request.user_success('Hasło zostało zmienione')
        
        request.user_success('Profil zapisany')
        user.save()
        
        
        
        
        
    
    
    return {
        'form' : form,
    }
    
@projectize()
@render('user/team/list')
def team_list(request,project):
    " Lista ludzi w projekcie "
    
    
    invite_form = user_f.InviteForm(request.POST if request.POST else None)
    
    if request.method == 'POST' and invite_form.is_valid():
        
        try:
            project.members.add(User.objects.get(email=invite_form.cleaned_data.get('email')))
        except: 
            request.user_success('Wyslano zaproszenie do %s' % invite_form.cleaned_data.get('email'))
            
            # wysylanie zaproszenia
            
            invitation = project_m.Invitation(
                creator = request.user,
                project = project,
                email = invite_form.cleaned_data.get('email')
            )
            
            invitation.save()
            
            
            send_mail(  
                'Zaproszenie do DYW',
                'Dostales zaproszenie do projektu %(project_name)s, nie masz jeszcze konta w DYW, Rejestracja - http://doyrwork.com/register/ (Pamietaj aby przy rejestracji uzyc %(email)s)' % { 
                    'project_name' : project.name,
                    'email' : invite_form.cleaned_data.get('email')
                },
                'robot@doyrwork.com',
                [invite_form.cleaned_data.get('email')]
            )
            
            raise Redirect('/p/%s/team/' % project.name )
            
        request.user_success('Dodano do zespołu')
        raise Redirect('/p/%s/team/' % project.name ) 

    
    return {
        'form' : invite_form,
        'project' : project,
        'users' : project.members.all(),
        'page_name' : 'team'
    }

@projectize()
@render('user/team/add')
def team_add(request,project):
    " Dodawanie czlowieka do projektu "

    if request.method == 'POST':
        users = request.POST.get('users','').split(',')
        for user in users:
            project.members.add(User.objects.get(pk=user))
    
        raise Redirect('/p/%s/team/' % project.name ) 
    
    return {
        'project' : project,
        'users' : User.objects.all(),
        'page_name' : 'team'
    }

@projectize()
def team_xhr_ac(request,project):
    list = []
    
    for user in User.objects.all():
        list.append('%s %s|%d' % (user.first_name,user.last_name,user.id))
    
    return HttpResponse("\n".join(list))


@render('user/crowd/list')
def crowd_list(request):
    " Lista ludzi "
    
    companies = user_m.Company.objects.all()
    
    for company in companies:
        company.members = User.objects.filter(company=company) 
   
    return {
        'users' : User.objects.all(),
        'companies' : companies,
        'page_name' : 'crowd'
    }
    
    
@render()
def login(request):
    
    post = request.POST.copy()
   
    form_login = user_f.LoginForm(post if post else None)
    
    if request.method == 'POST' and form_login.is_valid():
        
        
        user = User.objects.filter(email = form_login.cleaned_data.get('login'))
        if not user:
            user = User.objects.filter(username = form_login.cleaned_data.get('login'))
        if not user:
            return {
                'wrong' : True,
                'form' : form_login
            }
        
        user = user[0]
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        
        if user.check_password(form_login.cleaned_data.get('password')):
            
            # czyli jestesmy zalogowani
            
            # @TODO: Tylko przy pierwszym logowaniu
            
            for inv in  project_m.Invitation.objects.filter( email=user.email):
                inv.project.members.add(user)
                inv.delete()
                # @TODO: Sprawdzic czy dobrze sie usuwaja invitki
            
            
            auth_login(request,user)
            raise Redirect('/')
        else:
            return {
                'wrong' : True,
                'form' : form_login
            }
    
    return {
        'form' : form_login
    }

from django.core.mail import send_mail
from random import choice
@render()
def register(request):
    
    form_register = user_f.RegisterForm(request.POST if request.POST else None)
    
    
    if request.method == 'POST' and form_register.is_valid():
        user = User()
        
        cd = form_register.cleaned_data
        
        
        user.username = cd.get('email')
        user.email = cd.get('email')
        user.first_name = cd.get('first_name')
        user.last_name = cd.get('last_name')
        
        password = ''.join([choice('abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789') for i in range(8)])
        
        user.set_password(password)
        
        user.is_active = 1
        
        user.save()
        
        send_mail(  
            'Rejestracja DYW',
            'Twoje hasło to : "%(password)s", mozesz je zmienic po zalogowaniu' % { 
                #'email' : user.email, 
                'password' : password
            },
            'robot@doyrwork.com',
            [user.email]
        )
        
        return ('user/register_ok',{
            'provider' : user.email.split('@')[1],
            'email' : user.email
        })
        
    return {
        'form' : form_register
    }




