from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Role model
class Role(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role

# Linking User with Role
class user_role(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)

# Seller profile
class selleradd(models.Model):
    sellername = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    shopname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    profile = models.ImageField(upload_to='seller_profiles/')

    def __str__(self):
        return str(self.sellername)

# Product listing
class addproduct(models.Model):
    sellername = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField(default="No description available")
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product_name

# Customer profile
class customers(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.customer_name

# Order list
class orderlist(models.Model):
    product_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=200)
    sellername = models.CharField(max_length=100)
    shopname = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_email = models.CharField(max_length=200)
    customer_number = models.CharField(max_length=140)
    delivery_address = models.CharField(max_length=130)
    order_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Order of {self.product_name} by {self.customer_name}"
