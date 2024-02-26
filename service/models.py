from django.db import models

# Create your models here.
class Service(models.Model):
    name=models.CharField(max_length=22)
    description = models.TextField(max_length=105)
    image=models.ImageField(upload_to='images/service/')

    def __str__(self):
        return self.name