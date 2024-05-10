from django.db import models
from datetime import datetime

class Article(models.Model):
    app_label = 'api'
    id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.FloatField()
    tax = models.FloatField()
    creation_date = models.DateField(datetime.now().date())     

class Order(models.Model):
    app_label = 'api'
    id = models.AutoField(primary_key=True)
    price = models.FloatField(default=0)
    tax_price = models.FloatField(default=0)
    creation_date = models.DateField(datetime.now().date()) 

class Order_Article(models.Model):
    app_label = 'api'
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='articles')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    
    
