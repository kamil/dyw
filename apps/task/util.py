from dyw.apps.task import models as task_m

def get_statuses(project):
    #return task_m.Status.objects.filter(project=project)
    return taks_m.Status.objects.all()