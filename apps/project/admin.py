from django.contrib import admin
from dyw.apps.project import models as project_m

admin.site.register(project_m.Project)