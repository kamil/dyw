from django import forms

class NewTaskForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    
class NewTagForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
