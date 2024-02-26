from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserAccount,UserAddress


class UserRegistrationForm(UserCreationForm):
    image=forms.ImageField(required=False)
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    phone=forms.CharField(max_length=14)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=50)
    postal_code=forms.CharField()
    country=forms.CharField(max_length=50)
    class Meta:
        model=User
        fields=['username','password1','password2','first_name','last_name','email','image','birth_date','phone','street_address','city','postal_code','country']
        widgets = {
            'username': forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Enter your username',
                'name':'username',
            }),
            'password1': forms.PasswordInput(attrs={
                'type':'password',
                'name':'password',
                'placeholder':'Enter Password*',
            }),
            'password2': forms.PasswordInput(attrs={
                'type':'password',
                'name':'confirmpassword',
                'placeholder':'Enter Confirm Password*',
            }),
            'first_name': forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Enter your First name',
                'name':'first_name',
            }),
            'last_name': forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Enter your Last name',
                'name':'last_name',
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
            'street_address':forms.TextInput(attrs={
                'type':'text',
                'placeholder': 'Enter Street Address',
                'name':'street_address',
            }),
            'city':forms.TextInput(attrs={
                'type':'text',
                'placeholder': 'Enter City',
                'name':'city',
            }),
            'postal_code':forms.TextInput(attrs={
                'type':'text',
                'placeholder': 'Enter Postal Code',
                'name':'postal_code',
            }),'country':forms.TextInput(attrs={
                'type':'text',
                'placeholder': 'Enter Country',
                'name':'country',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].initial = 'images/profile/user_avatar.png'

    def save(self,commit=True):
        our_user=super().save(commit=False)
        if commit==True:
            our_user.save()
            image = self.cleaned_data.get('image', 'images/profile/user_avatar.png')
            birth_date=self.cleaned_data.get('birth_date')
            phone=self.cleaned_data.get('phone')
            street_address=self.cleaned_data.get('street_address')
            city=self.cleaned_data.get('city')
            postal_code=self.cleaned_data.get('postal_code')
            country=self.cleaned_data.get('country')

            UserAccount.objects.create(
                user=our_user,
                image=image,
                birth_date=birth_date,
                account_no=100000+int(our_user.id),
            )

            UserAddress.objects.create(
                user=our_user,
                phone=phone,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country,
            )
        
        return our_user


class UserUpdateForm(forms.ModelForm):
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    phone=forms.CharField(max_length=14)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=50)
    postal_code=forms.CharField()
    country=forms.CharField(max_length=50)

    class Meta:
        model=User
        fields=['first_name','last_name','email']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # if user have an account
        if self.instance:
            try:
                user_account=self.instance.account
                user_address=self.instance.address
            except UserAccount.DoesNotExist:
                user_account=None
                user_address=None
            if user_account:
                self.fields['birth_date'].initial=user_account.birth_date
                self.fields['phone'].initial=user_address.phone
                self.fields['street_address'].initial=user_address.street_address
                self.fields['city'].initial=user_address.city
                self.fields['postal_code'].initial=user_address.postal_code
                self.fields['country'].initial=user_address.country

    def save(self,commit=True):
        our_user=super().save(commit=False)
        if commit:
            our_user.save()

            user_account,created=UserAccount.objects.get_or_create(user=our_user)
            user_address,created=UserAddress.objects.get_or_create(user=our_user)

            user_account.birth_date=self.cleaned_data['birth_date']
            user_account.save()

            user_address.phone=self.cleaned_data['phone']
            user_address.street_address=self.cleaned_data['street_address']
            user_address.city=self.cleaned_data['city']
            user_address.postal_code=self.cleaned_data['postal_code']
            user_address.country=self.cleaned_data['country']
            user_address.save()

        return our_user