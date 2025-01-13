from django.contrib import admin
from .models import Product,Order
# Register your models here.

class ProductAdmin(admin.ModelAdmin):   # show the product table to admin
    list_display=['id','pname','price']
admin.site.register(Product,ProductAdmin)  # only take two parameters
admin.site.register(Order)



  