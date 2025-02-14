from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, help_text='Required')
    last_name = forms.CharField(max_length=100, required=True, help_text='Required')
    email = forms.EmailField(required=True, help_text='Enter a valid email')


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        help_texts = {
            'username': 'Letters, digits and @/./+/-/_ only',
            'password1' : 'Your password must contain at least 8 characters.',
            'password2' : 'Enter the same password as before.'
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ["size",
                  "crust",
                  "sauce",
                  "cheese",
                  "toppings"
                  ]
        widgets = {
            'toppings': forms.CheckboxSelectMultiple()
        }

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ["name",
                  "address",
                  "cardNo",
                  "expMonth",
                  "expYear",
                  "cvv"
                  ]