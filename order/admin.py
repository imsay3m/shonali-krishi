from django.contrib import admin
from .models import Order,Transaction,CartItem
# Register your models here.
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ['account','payment_id', 'transaction_type','amount','balance_after_transaction','timestamp']
admin.site.register(Transaction,TransactionModelAdmin)


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'user','display_products', 'total', 'status', 'placed_on']
    def display_products(self, obj):
        products = obj.products.all()
        return ", ".join(product.name for product in obj.products.all())
    display_products.short_description = 'Products'
admin.site.register(Order,OrderModelAdmin)


class CartItemModelAdmin(admin.ModelAdmin):
    list_display=['user','product','quantity','date_added']
admin.site.register(CartItem,CartItemModelAdmin)