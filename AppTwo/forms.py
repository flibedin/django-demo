from django import forms
from django.contrib.auth.models import User
from AppTwo.models import UserProfileInfo

class ClienteForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30 )
    last_name = forms.CharField(label='Last Name', max_length=30 )
    email = forms.CharField(label='Email', max_length=64 )

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

class UserForm( forms.ModelForm):
    password = forms.CharField( widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ( 'username', 'email', 'password' )


class UserProfileInfoForm( forms.ModelForm ):

    class Meta():
        model = UserProfileInfo
        fields = ('portfolio', 'profile_pic')
