from django.db import models
from account.models import UserAccount
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.

TRANSACTION_TYPES=[
    ['PAY', 'PAY'],
    ]

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    payment_id = models.IntegerField(null=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction=models.DecimalField(decimal_places=2,max_digits=12)
    class Meta:
        ordering=['timestamp']

    def __str__(self):
        return f"{self.account.user.account.account_no}"
    

STATUS=[
    ['New Orders','New Orders'],
    ['In Process', 'In Process'],
    ['Sending','Sending'],
    ['Sent', 'Sent'],
    ['Cancelled', 'Cancelled']
]
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status=models.CharField(choices=STATUS,max_length=100, null=True)
    order_no = models.IntegerField(null=True, blank=True)
    placed_on = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, blank=True, related_name="orders")
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.order_no)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'