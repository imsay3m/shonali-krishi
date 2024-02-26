from django import forms
from .models import ContactUs

class ContactUsForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields=['name','email', 'phone','message']
        widgets = {
            'name': forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Enter your name',
                'name':'name',
            }),
            'email': forms.EmailInput(attrs={
                'type':'email', 
                'placeholder': 'Enter email address',
                'name':'email'
            }),
            'phone':forms.TextInput(attrs={
                'type':'text',
                'placeholder': 'Enter phone number',
                'name':'phone',
            }),
            'message':forms.Textarea(attrs={
                'placeholder': 'Enter message',
                'name':'message',
            })
        }