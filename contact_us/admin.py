from django.contrib import admin
from .models import ContactUs
# Register your models here.

class ContactUsModelAdmin(admin.ModelAdmin):
    list_display=['name','email','phone','message']

admin.site.register(ContactUs,ContactUsModelAdmin)