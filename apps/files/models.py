import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


ATTACH_TYPE = {
    'project' : 1,
    'task' : 2
}

class FileAttach(models.Model):

    ATTACH_TYPE = [(v,k) for k,v in ATTACH_TYPE.items()]

    attach_type = models.PositiveSmallIntegerField(choices=ATTACH_TYPE)
    attach_id = models.IntegerField()
    attach_text = models.CharField( max_length = 255, null = True )
    
    creator = models.ForeignKey(User)
    
    title = models.CharField( max_length = 255, null = True )
    description = models.TextField( null = True)
    
    filename = models.CharField(max_length=255)
    
    date_modified = models.DateTimeField( auto_now = True )
    date_added =  models.DateTimeField( auto_now_add = True ) 
    
    def attach_filename(self):
        return "%d-%d-%s" % (self.id,self.attach_id,self.filename)
        
    def get_url(self):
        return "/s/f/attach/%s" % self.attach_filename()
    
    def get_file_ext(self):
        filename, ext= os.path.splitext(self.filename)
        return ext[1:]