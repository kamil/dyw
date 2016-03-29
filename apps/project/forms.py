from django import forms
import re

from dyw.apps.project.models import Project

class NewProjectForm(forms.Form):
    title = forms.CharField( max_length = 100)
    name = forms.CharField( max_length = 20)
    description = forms.CharField(widget = forms.Textarea({ 'cols' : 30, 'rows' : 4 }))
    
    def clean_name(self):
        name = self.cleaned_data.get('name','')
        sp = re.findall('[A-Za-z0-9_]+',name)
        
        if "".join(sp) != name:
            raise forms.ValidationError('Zly zapis nazwy')
            
        if Project.objects.filter(name=name).count() > 0:
            raise forms.ValidationError('Nazwa projektu jest juz uzywana')
        
        return "".join(sp)   
    
class EditProjectForm(NewProjectForm):
    secret = forms.CharField( max_length = 32)