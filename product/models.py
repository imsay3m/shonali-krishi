from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,blank=True,null=True)

    class Meta:
        verbose_name_plural="Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='images/product/')
    is_discount = models.BooleanField(blank=True, default=False)
    discount_price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    categories = models.ManyToManyField(Category)
    buyer=models.ManyToManyField(User,blank=True)
    is_new=models.BooleanField(default=False)
    is_sold_out=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=False,null=False)
    body=models.TextField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewed By {self.user.first_name} {self.user.last_name}"