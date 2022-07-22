from django.db import models


# TODO UUID field / adjust max len?
class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# TODO UUID field / adjust max len?
class Offer(models.Model):
    id = models.CharField(max_length=255)
    price = models.FloatField()
    items_in_stock = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
