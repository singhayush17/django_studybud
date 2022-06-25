from dataclasses import field
from msilib.schema import File
from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields =['name','email','username','password1','password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields='__all__' #will create a form for Room with all its fields
        exclude = ['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields =['avatar','name','email','username','bio']
