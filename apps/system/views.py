from dyw.contrib.render import render
from django.http import HttpResponse
from dyw.apps.system import models as system_m

@render()
def changelog(request):
    " Changelog "
    return {}

def feedback(request):
    
    if request.method == 'POST':
        feedback = system_m.Feedback(
            user = request.user,
            message = request.POST.get('message','')
        )
        
        feedback.save()
    
    return HttpResponse('OK')