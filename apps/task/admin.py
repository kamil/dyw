from django.contrib import admin
from dyw.apps.task import models as task_m

admin.site.register(task_m.Task)