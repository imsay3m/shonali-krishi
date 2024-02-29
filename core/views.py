from django.shortcuts import render
from django.views.generic import TemplateView
from service.models import Service
from order.models import CartItem
# Create your views here.
def home(request,category_slug=None):
    services=Service.objects.all()
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)-sum(item.product.discount_price * item.quantity for item in cart_items)
        return render(request,'index.html',{'services':services,'cart_items': cart_items, 'total_price': total_price})
    else:
        return render(request,'index.html',{'services':services})
class AboutView(TemplateView):
    template_name="about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = None
        total_price=0
        if self.request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=self.request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)-sum(item.product.discount_price * item.quantity for item in cart_items)
        context['cart_items'] = cart_items
        context['total_price'] = total_price
        return context

class ComingSoonView(TemplateView):
    template_name="coming_soon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = None
        total_price=0
        if self.request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=self.request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)-sum(item.product.discount_price * item.quantity for item in cart_items)
        context['cart_items'] = cart_items
        context['total_price'] = total_price
        return context