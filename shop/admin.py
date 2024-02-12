from django.contrib import admin

# Register your models here.
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'stock_quantity'
    )
    search_fields = (
        'name', 'stock_quantity'
    )
    
admin.site.register(Product, ProductAdmin)