from django.contrib import admin
from .models import Category,Product,Review

# Register your models here.
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']


class ProductModelAdmin(admin.ModelAdmin):
    list_display=['name','display_categories','is_sold_out','is_discount','price','discount_price']
    # desplay_modelName
    def display_categories(self, obj):
        categories = obj.categories.all()
        return ", ".join(category.name for category in obj.categories.all())
    display_categories.short_description = 'Categories'

admin.site.register(Category,CategoryModelAdmin)
admin.site.register(Product,ProductModelAdmin)
admin.site.register(Review)