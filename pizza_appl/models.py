from django.db import models
from django.contrib.auth.models import User

class Toppings(models.Model):
    topping = models.CharField(max_length=80)
    
    def __str__(self):
        return self.topping


######################## PIZZA MODEL
class Pizza(models.Model):
    
  sizes_choices = [
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large')
]

  crusts_choices = [
    ('normal', 'Normal'),
    ('thin', 'Thin'),
    ('gluten free', 'Gluten Free'),
    ('thick', 'Thick')
    
]

  cheese_choices= [
    ('mozzarella', 'Mozzarella'),
    ('vegan', 'Vegan'),
    ('low fat', 'Low Fat')
]

  sauce_choices = [
    ('tomato', 'Tomato'),
    ('bbq', 'BBQ')
]

  pizzaSizes = tuple(sizes_choices)
  pizzaCrusts = tuple(crusts_choices)
  pizzaCheese = tuple(cheese_choices)
  pizzaSauce = tuple(sauce_choices)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  size = models.CharField(max_length=20, choices=pizzaSizes, default='medium')
  crust = models.CharField(max_length=20, choices=pizzaCrusts, default='normal')
  sauce = models.CharField(max_length=20, choices=pizzaSauce, default='tomato')
  cheese = models.CharField(max_length=20, choices=pizzaCheese, default='mozzarella')
  toppings = models.ManyToManyField(Toppings)
    
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
    cardNo = models.CharField(max_length=16)
    expMonth = models.CharField(max_length=15, choices=MONTH_CHOICES, default='January')
    expYear = models.IntegerField(choices=YEAR_CHOICES, default=2000)

    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Delivery for {self.name} by {self.author.username}"