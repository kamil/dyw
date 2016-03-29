from django.db import models
from django.contrib.auth.models import User
from docutils.core import publish_parts

from dyw.apps.project.models import Project

class PageRevisions(models.Model):
    " Rewizja strony "
    
    creator = models.ForeignKey(User)
    
    page = models.ForeignKey('Page')
    content = models.TextField( blank = True )
    comment = models.TextField( blank = True )
    
    date_added = models.DateTimeField( auto_now_add = True )
    
    
    def get_content(self):
        return publish_parts(self.content, writer_name='html').get('html_body','')



class Page(models.Model):
    " Strona "
    
    project = models.ForeignKey(Project)
    creator = models.ForeignKey(User)
    
    name = models.TextField()
    title = models.TextField()
    
    date_added = models.DateTimeField( auto_now_add = True )
    date_modified = models.DateTimeField( auto_now = True )
    
    def get_title(self):
        if not self.title:
            return self.name
        else:
            return self.title
    
    def get_last_revision(self):
        try:
            return PageRevisions.objects.filter( page = self ).order_by('-date_added')[0]
        except:
            return PageRevisions( page = self )

    def count_revisions(self):
        return PageRevisions.objects.filter(page=self).count()