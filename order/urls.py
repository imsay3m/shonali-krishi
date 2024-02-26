from django.urls import path
from .views import add_to_cart, checkout, remove_from_cart, view_cart,item_decrement,item_increment,cart_clear,place_order

urlpatterns = [
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('cart/checkout/',checkout,name="checkout"),
    path('cart/place_order/',place_order,name='place_order'),
]
