from django.shortcuts import render, redirect
from django.http import *
from django.contrib import messages
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *

def index(request):
    toppings = Toppings.objects.all()
    if request.user.is_authenticated:
        pizzas = Pizza.objects.filter(author=request.user)
    else:
        pizzas = []
    return render(request, 'index.html', {'pizzas':pizzas, 'user':request.user}, {'toppings':toppings})

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})

class LoginView(LoginView):
    template_name = 'login.html'
       
    
def log_out(request):
    logout(request)
    return redirect('index')
@login_required(login_url='index')

def create_order(request):
    toppings = Toppings.objects.all()

    if request.method == 'POST':
        form = PizzaForm(request.POST)

        if form.is_valid():
            pizza = form.save(commit=False)
            pizza.author = request.user
            pizza.save()
            request.session['pending_pizza_id'] = pizza.id
            return redirect('/delivery')
        else:
            return render(request, 'order.html', {'form': form, "toppings": toppings})

    else:
        form = PizzaForm()
        return render(request, 'order.html', {'form': form, "toppings": toppings})

def delivery_page(request):
    pizza_id = request.session.get('pending_pizza_id')
    if not pizza_id:
        messages.error(request, "Please create a pizza order first")
        return redirect('order')

    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.author = request.user
            
            # Connect the pizza to this delivery
            pizza = Pizza.objects.get(id=pizza_id)
            delivery.pizza = pizza
            delivery.save()
            
            # Clear the pending pizza from session
            del request.session['pending_pizza_id']
            
            messages.success(request, "Order has been placed successfully!")
            return redirect('/')
    else:
        form = DeliveryForm()
    
    return render(request, 'delivery_page.html', {'form': form})

def orders_page(request):
    deliveries = Delivery.objects.filter(author=request.user)
    return render(request, 'user_orders.html', {'deliveries': deliveries})