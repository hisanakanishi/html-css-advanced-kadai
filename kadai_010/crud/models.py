from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
    
    #新規作成・編集(完了時のリダイレクト先
    def get_absolute_url(selt):
        return reverse('list')
