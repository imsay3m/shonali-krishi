from django.shortcuts import render
from django.urls import reverse_lazy
from contact_us.forms import ContactUsForm
from django.views.generic import FormView
from django.contrib import messages
from order.models import CartItem
# Create your views here.
class ContactUsView(FormView):
    template_name='contact_us/contact.html'
    form_class=ContactUsForm
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'You Have Submitted the Message Successfully! We will get back to you soon..')
        return super().form_valid(form)

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