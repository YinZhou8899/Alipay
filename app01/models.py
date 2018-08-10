from django.db import models


class Goods(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField()


class Orders(models.Model):
    no = models.CharField(max_length=64)
    good = models.ForeignKey(to='Goods')
    status_choice = ((0,'未支付'),(1,'已支付'))
    status =models.IntegerField(choices=status_choice,default=0)