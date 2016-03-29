from dyw.apps.project.models import Project

def get_project(project_name):
    " Zwraca projekt o podanej nazwie "
    return Project.objects.get(name=project_name)
    
def get_members(project_name):
    " Zwraca ludzi z projektu o podanej nazwie "
    return Project.objects.get(name=project_name).members.all()