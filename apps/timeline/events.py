from dyw.apps.timeline.models import Event,EVENT_TYPES,EVENT_CLASS
from dyw.apps.task.models import Task


class CastEvent():
    
    def render_template(self,template,context):
        return render_to_string('timeline/events/%s' % template,{
            'e' : self,
            'p' : context
        })
    
    
    def render(self):
        raise NotImplementedError
    
    def event(self,**kwargs):
        # TODO: Pewnie da sie zrobic lepiej
        new_event = Event()
        for name,value in kwargs:
            setattr(new_event,name,value)
        return new_event.save()
        
        

        

class TaskChangedEvent(CastEvent):

    def render(self,ext='html'):
        return self.render_template('task-changed.%s' % ext,{
            'task' : Task.objects.get(pk=self.param_first_id)
        })

    def cast(self,who,task,change):
        self.event(
            event_type = EVENT_TYPES.index('task-changed'),
            project = task.project,
            cast_by = who,
            param_first_id = task.id,
            param_second_id = change.id
        )    
        
        
EVENT_CLASS[EVENT_TYPES.index('task-changed')] = TaskChangedEvent



def event_wiki_changed(who,page,revision):
    e = Event(
        project = page.project,
        event_type = EVENT_TYPES.index('wiki-changed'),
        cast_by = who,
        param_first_id = page.id,
        param_second_id = revision.id,
        param_comment = page.name,
    )
    e.save()
    return e

def event_task_created(who,task):
    e = Event(
        project = task.project,
        event_type = EVENT_TYPES.index('task-created'),
        cast_by = who,
        param_first_id = task.id
    )
    e.save()
    return e
    
def event_task_closed(who,task):
    e = Event(
        project = task.project,
        event_type = EVENT_TYPES.index('task-closed'),
        cast_by = who,
        param_first_id = task.id
    )
    e.save()
    return e

def event_task_changed(who,task,change):
    e = Event(
        project = task.project,
        event_type = EVENT_TYPES.index('task-changed'),
        cast_by = who,
        param_first_id = task.id,
        param_second_id = change.id
    )
    e.save()
    return e


    
def event_wiki_created(who,page):
    e = Event(
        project = page.project,
        event_type = EVENT_TYPES.index('wiki-created'),
        cast_by = who,
        param_first_id = page.id,
        param_comment = page.name,
    )
    e.save()
    return e






