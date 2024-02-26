from django.urls import path
from .views import  ProductDetailView, product
urlpatterns = [
    path('',product,name='products'),
    path('details/<int:id>/', ProductDetailView.as_view(), name='product_details'),
    path('<slug:category_slug>/', product, name='products_by_category'),
]
