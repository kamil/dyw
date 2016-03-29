# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from dyw.apps.project import util as project_u
from dyw.apps.milestone.models import Milestone
from dyw.apps.task.models import Task,Comment
from dyw.apps.task import models as task_m

from django.http import HttpResponse, HttpResponseRedirect
from dyw.apps.task import forms as task_f
from django.contrib.auth.models import User
from docutils.core import publish_parts
from dyw.apps.timeline import events as timeline_e
from dyw.apps.files import util as files_u
from dyw.apps.files import models as files_m

from dyw.contrib.render import render,Redirect,projectize

# TUTAJ TESTOWO
# template = 'task/assigned'
def smart_mail(user,template,args):
    pass


@projectize()
@render()
def list(request,project):
    " Lista zadan w projekcie "

    closed_statuses = [item.id for item in task_m.Status.objects.filter(status=1)]

    tasks_open = Task.objects.filter( project = project ).exclude( status__in = closed_statuses ).order_by('-priority')

    tasks_closed_or_invalid_count = Task.objects.filter(
        status__in = closed_statuses,
        project = project
    ).count()

    tags_in_project = task_m.Tag.objects.filter(project=project)

    return {
        'project' : project,
        'tasks' : tasks_open,
        'tags' : tags_in_project,
        'tasks_closed_or_invalid_count' : tasks_closed_or_invalid_count,
        'page_name' : 'tasks',
    }

@projectize()
@render('task/list')
def closed(request,project):

    closed_statuses = [item.id for item in task_m.Status.objects.filter(status=1)]


    tasks_closed = Task.objects.filter(
        status__in = closed_statuses,
        project = project
    )

    return {
        'project' : project,
        'tasks' : tasks_closed,
        'page_name' : 'tasks'
    }


@projectize()
@render()
def show(request,project,task):
    " Zadanie "

    try:
        task = Task.objects.get(pk=int(task))
    except Task.DoesNotExist:
        request.user_error('Nie ma takiego zadania')
        raise Redirect('/p/%s/tasks/' % project.name)

    comments = Comment.objects.filter(task=task).order_by('date_added')

    if request.method == "POST":
        comment = Comment(
            creator = request.user,
            task = task,
            comment = request.POST.get('comment'),
            markup = int(request.POST.get('markup'))
        )

        change = {}

        closed_event = False

        # jezeli tagi sie zmienily, sprawdzamy odrazu autkalne tagi z modelu
        # TODO: Jest czuly na kolejnosc
        # TODO: Ogolna optymalizacja :)
        if request.POST.get('tags', '') != ','.join([str(t.id) for t in task.tags.all()]):

            sp_tags = []

            if request.POST.get('tags', '') == '': # pusta lista oznacza ze wszystkie zostaly odzznaczone
                change['tags'] = []
                for t in [t for t in task.tags.all()]:
                    task.tags.remove(t)
            else:
                try:
                    sp_tags = [task_m.Tag.objects.filter(pk=t_id,project=project)[0] for t_id in request.POST.get('tags').split(',')]
                except:
                    # Jezeli ten try sie wyjebal to znaczy ze ktos nam mieszal z tagami przy requescie
                    pass
                else:

                    # KURWA PADAKA :(
                    change['tags'] = [t.id for t in sp_tags]
                    cur_tags = [t for t in task.tags.all()]
                    for t in cur_tags:
                        if t not in sp_tags:
                            task.tags.remove(t)

                    for t in sp_tags:
                        if t not in cur_tags:
                            task.tags.add(t)



        if request.POST.get('assigned',None) != '-1':

            try:
                x = User.objects.get(pk=request.POST.get('assigned'))
            except:
                pass
            else:
                change['assingned'] = request.POST.get('assigned')
                task.assigned_id = change['assingned']

        if request.POST.get('milestone',None) != '-1':
            change['milestone'] = request.POST.get('milestone')
            task.milestone_id = change['milestone']

        if request.POST.get('in_type',None) != '-1':
            change['in_type'] = request.POST.get('in_type')
            task.in_type = task_m.Type.objects.get(pk=change['in_type'])

        if request.POST.get('status',None) != '-1':
            change['status'] = request.POST.get('status')
            task.status = task_m.Status.objects.get(pk=change['status'])
            if task.status.status == 1: # Zamykamy
                timeline_e.event_task_closed(request.user,task)
                closed_event = True

        if request.POST.get('priority',None) != '-1':
            change['priority'] = request.POST.get('priority')
            task.priority = task_m.Priority.objects.get(pk=change['priority'])



        if len(comment.comment) or change or request.FILES.get('attach',False):
            task.save()

            if request.FILES.get('attach',False):
                _file = request.FILES.get('attach')
                attach = files_u.attach_file('task',task.id,request.user,_file)
                change['attach'] = attach.id

            if change:
                comment.changes = change

            comment.save()

            if not closed_event:
                timeline_e.TaskChangedEvent().cast(request.user,task,comment)

        if request.POST.get('redir',None):
            raise Redirect('/p/%s/tasks/' % (project.name) )

        request.user_success('Dodano zmianę')

        raise Redirect('/p/%s/tasks/%d/' % (project.name,task.id) )


    rest_comments = comments[1:]

    for comment in rest_comments:
        comment.post_changes = comment.changes
        comment.detail_changes = {}

        # if comment.post_changes.get('tags',None):
        #     try:
        #         comment.detail_changes['tags'] = [task_m.Tag.objects.get(pk=t_id) for t_id in comment.post_changes['tags']]
        #     except:
        #         pass
        #
        # if comment.post_changes.get('assingned',None):
        #     try:
        #         comment.detail_changes['assingned'] = User.objects.get(pk=comment.post_changes['assingned'])
        #     except:
        #         pass
        #
        # if comment.post_changes.get('milestone',None):
        #     try:
        #         comment.detail_changes['milestone'] = Milestone.objects.get(pk=comment.post_changes['milestone'])
        #     except:
        #         pass
        #
        # if comment.post_changes.get('priority',None):
        #     try:
        #         comment.detail_changes['priority'] = task_m.Priority.objects.get(pk=comment.post_changes['priority'])
        #     except:
        #         pass
        #
        # if comment.post_changes.get('status',None):
        #     try:
        #         comment.detail_changes['status'] = task_m.Status.objects.get(pk=comment.post_changes['status'])
        #     except:
        #         pass
        #
        # if comment.post_changes.get('in_type',None):
        #     try:
        #         comment.detail_changes['in_type'] = task_m.Type.objects.get(pk=comment.post_changes['in_type'])
        #     except:
        #         pass
        #
        # if comment.post_changes.get('attach',None):
        #     try:
        #         comment.detail_changes['attach'] = files_m.FileAttach.objects.get(pk=comment.post_changes['attach'])
        #     except:
        #         pass


    # rzeczy zwiazane z tagami/komponentami

    tags = task_m.Tag.objects.filter(project=project)
    xx = ','.join([str(t.id) for t in task.tags.all()])
    tags_assingned = xx

    return {
        'project' : project,
        'task' : task,
        'tags' : tags,
        'tags_assingned' : tags_assingned,
        'task_comment' : comments[0],
        'comments' : rest_comments,
        'members' : project.members.all(),
        'milestones' : Milestone.objects.filter( project = project ),
        'types' : task_m.Type.objects.all(),
        'priority' : task_m.Priority.objects.all(),
        'status' : task_m.Status.objects.all(),
        'page_name' : 'tasks',
    }

@projectize()
@render()
def observe(request,project,task):

    task = Task.objects.get(pk=int(task))

    if request.user in task.observers.all():
        task.observers.remove(request.user)
        request.user_success('Usunięto z listy obserwowanych')
    else:
        request.user_success('Dodano do listy obserwujących')
        task.observers.add(request.user)

    raise Redirect('/p/%s/tasks/%d/' % (project.name,task.id) )


@projectize()
@render('task/tags/new')
def tag_new(request,project):


    form = task_f.NewTagForm(request.POST if request.POST else None)

    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data

        tag = task_m.Tag(
            project = project,
            name = cd.get('title'),
            description = cd.get('description')
        )

        tag.save()

        request.user_success('Dodano tag')

        raise Redirect('/p/%s/tasks/' % project.name )

    return {
        'project' : project,
        'tag_form' : form,
        'page_name' : 'tasks'
    }

@projectize()
@render()
def new(request,project):
    " Nowe zadanie "

    form = task_f.NewTaskForm(request.POST if request.POST else None)

    if request.method == 'POST' and form.is_valid():

        task = Task(
            creator = request.user,
            milestone_id = request.POST.get('milestone'),
            title = request.POST.get('title'),
            in_type = task_m.Type.objects.get(pk=request.POST.get('in_type')),
            priority = task_m.Priority.objects.get(pk=request.POST.get('priority')),
            status_id = 0,
            project = project
        )

        if request.POST.get('assigned','0') != '0':
            task.assigned_id = int(request.POST.get('assigned'))

        task.save()

        comment = Comment(
            creator = task.creator,
            task = task,
            markup = int(request.POST.get('markup')),
            comment = request.POST.get('description')
        )

        comment.save()


        timeline_e.event_task_created(request.user,task)

        request.user_success('Zadanie dodano')

        if request.POST.get('save_and_add',False):
            raise Redirect('/p/%s/tasks/new/' % project.name )
        else:
            raise Redirect('/p/%s/tasks/%d/' % (project.name,task.id) )

    return {
        'project' : project,
        'members' : project.members.all(),
        'milestones' : Milestone.objects.filter( project = project ),
        'types' : task_m.Type.objects.all(),
        'priority' : task_m.Priority.objects.all(),
        'page_name' : 'tasks',

        'form' : form
    }


class Warnings:

    def __init__(self):
        self.messages = []

    def write(self, message):
        self.messages.append(message)



from docutils.core import publish_parts
import textile
def xhr_preview(request):

    if request.GET.get('markup','') == '0':
        text = publish_parts(request.GET.get('data',''), writer_name='html').get('html_body')
    elif request.GET.get('markup','') == '1':
        try:
            text = textile.textile(request.GET.get('data','').encode('utf-8'), encoding='utf-8')
        except:
            text = 'ERROR'

    return HttpResponse(text)
