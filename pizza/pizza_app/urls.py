from django.urls import path
from . import views
from .forms import *

urlpatterns = [
    path('order', views.order_view, name='order'),
]
