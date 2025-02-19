from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    class Meta:
        fields = ['username', 'password']


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