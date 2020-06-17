from django.contrib import admin

# Register your models here.
from order.models import ShopCart

from order.models import OrderProduce

from order.models import Order


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','produce','price','quantity','amount']
    list_filter = ['user']



class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name','phone','city','total','status']
    list_filter =  ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','ip','city','total')
    can_delete = False


class OrderProduceAdmin(admin.ModelAdmin):
    list_display = ['user','produce','price','quantity','amount']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduce,OrderProduceAdmin)
