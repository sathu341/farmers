from django.contrib import admin

# Register your models here.
from .models import Product, Cart, Order, Delivery,Farm_table,NewCart

admin.site.register(Product)
admin.site.register(NewCart)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Farm_table)