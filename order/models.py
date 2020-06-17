from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm,TextInput ,ChoiceField,forms,Select
from django.utils.crypto import get_random_string
from product.models import Produce

from content.models import Content


class ShopCart(models.Model):
    user =models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    produce =models.ForeignKey(Produce,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.produce

    @property
    def amount(self):
        return (self.quantity * self.produce.price)

    @property
    def price(self):
        return (self.produce.price)

    def __str__(self):
        return (self.produce.title)


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']

class Order(models.Model):
    STATUS  = (
        ('New' , 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),

    )

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    code = models.CharField(max_length=5,editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(blank=True,max_length=20)
    address = models.CharField(blank=True,max_length=150)
    city = models.CharField(blank=True,max_length=20)
    country = models.CharField(blank=True,max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=20,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    adminnote = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','address','phone','city','country']

class OrderProduce(models.Model):
    STATUS =(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Canceled','Canceled')
    )
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices = STATUS,default = 'New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.produce.title



