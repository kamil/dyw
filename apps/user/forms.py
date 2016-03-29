from django import forms
from dyw.apps.user import const as user_c
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField()
    im_jabber = forms.EmailField(required=False)
    markup = forms.ChoiceField(choices=user_c.MARKUP_SELECT, required=False)
    new_password = forms.CharField(required=False,widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField()

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data.get('email'))
        except:
            return self.cleaned_data.get('email')
        else:
            raise forms.ValidationError('Juz jest taki mail')
        
class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class InviteForm(forms.Form):
    email = forms.EmailField()