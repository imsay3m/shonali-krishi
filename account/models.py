from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAccount(models.Model):
    user=models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    image=models.ImageField(upload_to="profile/images",default='images/profile/user_avatar.png',)
    account_no=models.IntegerField(unique=True)#account number will not be same for multiple user
    birth_date=models.DateField(null=True,blank=True)
    initial_deposite_date=models.DateField(auto_now_add=True)
    balance=models.DecimalField(default=500,max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.account_no}"

class UserAddress(models.Model):
    user=models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
    phone=models.CharField(max_length=14,unique=True)
    street_address=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    postal_code=models.IntegerField()
    country=models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.user.email}"