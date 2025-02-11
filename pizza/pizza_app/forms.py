from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    email = forms.EmailField()


class PizzaForm(forms.ModelForm):
    TOPPINGS_CHOICES = [
        ('pepperoni', 'Pepperoni'),
        ('chicken', 'Chicken'),
        ('ham', 'Ham'),
        ('pineapple', 'Pineapple'),
        ('peppers', 'Peppers'),
        ('mushrooms', 'Mushrooms'),
        ('onions', 'Onions')
    ]
    toppings = forms.MultipleChoiceField(choices=TOPPINGS_CHOICES, widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'sauce', 'cheese', 'toppings']
        
class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['name', 'address', 'cvv', 'card_number', 'expiryMonth', 'expiryYear']
        