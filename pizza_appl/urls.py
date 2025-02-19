from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import *
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('create_pizza/', views.create_order, name='create_pizza'),
    path('delivery/', views.delivery_page, name='delivery'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('accounts/profile/', views.profile_view, name='profile'),

]

