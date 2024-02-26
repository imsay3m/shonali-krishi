from django.contrib import admin
from .models import UserAccount,UserAddress
# Register your models here.
class UserAccountModelAdmin(admin.ModelAdmin):
    list_display = ['user','account_no','balance', 'image']

class UserAddressModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'street_address', 'city', 'postal_code', 'country']

admin.site.register(UserAccount,UserAccountModelAdmin)
admin.site.register(UserAddress,UserAddressModelAdmin)