from django.shortcuts import render
from django.urls import reverse_lazy
from contact_us.forms import ContactUsForm
from django.views.generic import FormView
from django.contrib import messages
# Create your views here.
class ContactUsView(FormView):
    template_name='contact_us/contact.html'
    form_class=ContactUsForm
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'You Have Submitted the Message Successfully! We will get back to you soon..')
        return super().form_valid(form)