from django.db import models
from django.contrib.auth.models import User

import pickle


class Company(models.Model):
    title = models.TextField()

class UserProfile(models.Model):

    user = models.ForeignKey( User, unique=True )
    company = models.ForeignKey(Company)
    
    _options = models.TextField()
    
    date_modified = models.DateTimeField( auto_now = True )
    
    def get_options(self):
        try:
            return pickle.loads(self._options)
        except:
            return {}
    
    def set_options(self,setto):
        self._options = pickle.dumps(setto)
    
    options = property(get_options,set_options)
