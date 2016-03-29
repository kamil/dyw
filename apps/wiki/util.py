from dyw.apps.wiki.models import Page

def get_newest_page(name):
    " Zwraca najnowsza rewizje strony "
    
    try:
        page = Page.objects.filter(name=name).order_by('-date_added')[0]
        return page
    except:
        return None

def get_by_project(project):
    return Page.objects.filter(project=project).exclude(name__contains='/')


def get_page(project,page):
    " Zwraca strone "
    
    try:
        return Page.objects.get(
            name = page,
            project = project
        )
        
    except:
        return Page(
            name = page,
            project = project
        )