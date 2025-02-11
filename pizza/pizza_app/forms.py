from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserForm(UserCreationForm):
    firstName = forms.CharField()
    lastName = forms.CharField()
    
    email = forms.EmailField()
    password1 = forms.CharField(label= ("Password"), strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Confirm Password"), strip=False, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["firstName", "lastName", "email", "password1", "password2"]
        help_texts = {
            "username": None,
            "password1": None,
            "password2": None,
            "email": None
            }
class UserLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)

class PizzaForm(forms.ModelForm):

    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'sauce', 'cheese', 'toppings']
        
class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['name', 'address', 'cardNo', 'expMonth', 'expYear', 'cvv']
