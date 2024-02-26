from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body']
        widgets={
            'body':forms.Textarea(attrs={
                'placeholder': 'Type your review....',
                'name':'review',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        user = self.cleaned_data.get('user')
        product = self.cleaned_data.get('product')

        if user and product:
            if user not in product.buyer.all():
                raise forms.ValidationError("Only the Buyer of the product can write a review.")
        
        return cleaned_data