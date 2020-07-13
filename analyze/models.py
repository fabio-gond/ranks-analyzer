from django.db import models

# Create your models here.

class Seller(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    platform = models.CharField(max_length=32) ## Where did I contacted the customer
    other = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
    def __str__(self):
        return self.name


class ProductParent(models.Model):
    asin = models.CharField(max_length=32,default='')
    code = models.CharField(max_length=64) ## Seller's choosen SKU
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    marketplace = models.CharField(max_length=2, default = 'IT')
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
    def __str__(self):
        return self.code


class Product(models.Model):
    asin = models.CharField(max_length=32,default='')
    parent = models.ForeignKey(ProductParent, on_delete=models.CASCADE, null = True)
    code = models.CharField(max_length=64) ## Seller's choosen SKU
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    marketplace = models.CharField(max_length=2, default = 'IT')
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
    def __str__(self):
        return self.code