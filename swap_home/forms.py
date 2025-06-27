from .models import *
from django import forms 

# login
class Formulario(forms.Form):
    CI = forms.IntegerField()
    contraseña = forms.CharField(widget=forms.PasswordInput)