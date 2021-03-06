from django import forms
from django.contrib.auth.models import User
from security.models import UserProfileInfo

# este form solo lo utilizo para el registro
class UserForm( forms.ModelForm):
    password = forms.CharField( widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ( 'username', 'email', 'password' )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

# con este form actualizo los datos completos de un usuario
class UserFullForm( forms.ModelForm ):

    class Meta():
        model = User
        fields = ( 'first_name', 'last_name', 'email' )

    def __init__(self, *args, **kwargs):
        super(UserFullForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'


class UserProfileInfoForm( forms.ModelForm ):

    class Meta():
        model = UserProfileInfo
        fields = ('portfolio', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super(UserProfileInfoForm, self).__init__(*args, **kwargs)
        self.fields['portfolio'].widget.attrs['class'] = 'form-control'
        self.fields['profile_pic'].widget.attrs['class'] = 'form-control'
