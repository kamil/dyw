from django import forms

class NewMilestoneForm(forms.Form):
    title = forms.CharField( max_length = 100)
    description = forms.CharField(widget = forms.Textarea)
    date_due = forms.DateField(required=True)
    
    