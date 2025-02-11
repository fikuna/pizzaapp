from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pizza, Delivery
from .forms import PizzaForm, DeliveryForm

@login_required
def order_view(request):
    if request.method == 'POST':
        pizza_form = PizzaForm(request.POST)
        delivery_form = DeliveryForm(request.POST)
        
        if pizza_form.is_valid() and delivery_form.is_valid():
            # Save pizza order
            pizza = pizza_form.save(commit=False)
            pizza.author = request.user
            pizza.save()
            
            # Save delivery info
            delivery = delivery_form.save(commit=False)
            delivery.author = request.user
            delivery.save()
            
            return redirect('order_success')
    else:
        pizza_form = PizzaForm()
        delivery_form = DeliveryForm()
    
    context = {
        'pizza_form': pizza_form,
        'delivery_form': delivery_form
    }
    return render(request, 'pizza_app/order.html', context)


