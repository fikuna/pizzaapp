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
    if request.user.is_authenticated:
        pizzas = Pizza.objects.filter(author=request.user).prefetch_related('toppings').order_by('-date')
        return render(request, 'index.html', {'pizzas': pizzas})
    return render(request, 'index.html')


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


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            
    return render(request, 'login.html')

    
def log_out(request):
    logout(request)
    return redirect('index')
@login_required(login_url='/login')
def create_order(request):
    toppings = Toppings.objects.all()

    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save(commit=False)
            pizza.author = request.user
            pizza.save()
            form.save_m2m()

            pending_pizza_ids = request.session.get('pending_pizza_ids', [])
            pending_pizza_ids.append(pizza.id)
            request.session['pending_pizza_ids'] = pending_pizza_ids
            
            return redirect('delivery')

    else:
     form = PizzaForm()
    return render(request, 'order.html', {'form': form, "toppings": toppings})

@login_required(login_url='/login')
def delivery_page(request):
    pizza_ids = request.session.get('pending_pizza_ids', [])
    if not pizza_ids:
        return redirect('create_pizza')

    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.author = request.user
            delivery.save()
            
            # Associate each pizza with the delivery
            for pizza_id in pizza_ids:
                pizza = Pizza.objects.get(id=pizza_id)
                pizza.delivery = delivery  # Set the delivery field
                pizza.save()
            
            # Store the delivery ID in the session
            request.session['latest_delivery_id'] = delivery.id
            
            del request.session['pending_pizza_ids']
            return redirect('order_confirmation')
    else:
        form = DeliveryForm()
    
    return render(request, 'delivery_page.html', {'form': form})

def orders_page(request):
    deliveries = Delivery.objects.filter(author=request.user)
    return render(request, 'order_view.html', {'deliveries': deliveries})

@login_required
def profile_view(request):
    orders = Pizza.objects.all().filter(author=request.user)

    return render(request, 'profile.html', {'orders' : orders})
@login_required(login_url='/login')
@login_required(login_url='/login')
def order_confirmation(request):
    try:
        # Get the most recent delivery for this user
        delivery = Delivery.objects.filter(author=request.user).latest('id')
        # Get the associated pizza with all its toppings
        pizza = Pizza.objects.filter(author=request.user).prefetch_related('toppings').latest('date')
        
        context = {
            'delivery': delivery,
            'pizza': pizza
        }
        
        return render(request, 'order_view.html', context)
    except (Delivery.DoesNotExist, Pizza.DoesNotExist):
        return redirect('create_pizza')
