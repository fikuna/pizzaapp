from django.db import models
from django.contrib.auth.models import User

######################## PIZZA CONFIG 
# The original static choices (now commented out):
#
# pizzaSizes = (
#     ("small", "small"),
#     ("medium", "medium"),
#     ("large", "large"),
# )
#
# pizzaCrustSize = (
#     ("thin", "thin"),
#     ("normal", "normal"),
#     ("thick", "thick"),
#     ("gluten free", "gluten free"),
# )
#
# pizzaSauce = (
#     ("tomato", "tomato"),
#     ("vegan", "bbq"),
# )
#
# pizzaCheese = (
#     ("mozzarella", "mozzarella"),
#     ("vegan", "vegan"),
#     ("low fat", "low fat"),
# )

# models to hold items
class PizzaSizes(models.Model):
    size = models.CharField(max_length=20)

    def __str__(self):
        return self.size

class PizzaCrust(models.Model):
    crust = models.CharField(max_length=20)

    def __str__(self):
        return self.crust

class PizzaCheese(models.Model):
    cheese = models.CharField(max_length=20)

    def __str__(self):
        return self.cheese

class PizzaSauce(models.Model):
    sauce = models.CharField(max_length=20)

    def __str__(self):
        return self.sauce

# Build choice tuples from database entries.
# Because this code runs at import time, we use try/except blocks to fall back on defaults.
try:
    size_items = PizzaSizes.objects.all()
    pizzaSizes = tuple((item.size, item.size) for item in size_items) or (('medium', 'medium'),)
except Exception:
    pizzaSizes = (('medium', 'medium'),)

try:
    crust_items = PizzaCrust.objects.all()
    pizzaCrustSize = tuple((item.crust, item.crust) for item in crust_items) or (('normal', 'normal'),)
except Exception:
    pizzaCrustSize = (('normal', 'normal'),)

try:
    sauce_items = PizzaSauce.objects.all()
    pizzaSauce = tuple((item.sauce, item.sauce) for item in sauce_items) or (('tomato', 'tomato'),)
except Exception:
    pizzaSauce = (('tomato', 'tomato'),)

try:
    cheese_items = PizzaCheese.objects.all()
    pizzaCheese = tuple((item.cheese, item.cheese) for item in cheese_items) or (('mozzarella', 'mozzarella'),)
except Exception:
    pizzaCheese = (('mozzarella', 'mozzarella'),)

######################## PIZZA MODEL
class Pizza(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, choices=pizzaSizes, default='medium')
    crust = models.CharField(max_length=20, choices=pizzaCrustSize, default='normal')
    sauce = models.CharField(max_length=20, choices=pizzaSauce, default='tomato')
    cheese = models.CharField(max_length=20, choices=pizzaCheese, default='mozzarella')
    
    # Toppings can be stored as a comma-separated string.
    toppings = models.CharField(max_length=500, blank=True)
    
    # Automatically set the order date when the pizza is created.
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Pizza by {self.author.username} on {self.date.strftime('%Y-%m-%d')}"

############# DELIVERY CONFIG

# Month choices for expiration date
MONTH_CHOICES = (
    ("January", "January"),
    ("February", "February"),
    ("March", "March"),
    ("April", "April"),
    ("May", "May"),
    ("June", "June"),
    ("July", "July"),
    ("August", "August"),
    ("September", "September"),
    ("October", "October"),
    ("November", "November"),
    ("December", "December"),
)

# Year choices for expiration date
YEAR_CHOICES = tuple((year, year) for year in range(2022, 2050))

class Delivery(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    # For card numbers, consider using a CharField if you need to preserve leading zeros.
    cardNo = models.IntegerField()
    expMonth = models.CharField(max_length=15, choices=MONTH_CHOICES, default='January')
    expYear = models.IntegerField(choices=YEAR_CHOICES, default=2000)
    # IntegerField does not support max_length; if you need fixed-length, consider CharField.
    cvv = models.IntegerField()

    def __str__(self):
        return f"Delivery for {self.name} by {self.author.username}"