from django.db import models
from users.models import CustomUser

# Create your models here.

""" class Seller(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    platform = models.CharField(max_length=32, null=True, blank = True) ## Where did I contacted the customer
    other = models.CharField(max_length=64, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
    def __str__(self):
        return self.name """


class ProductParent(models.Model):
    asin = models.CharField(max_length=32,default='')
    code = models.CharField(max_length=64) ## Seller's choosen SKU
    #seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    marketplace = models.CharField(max_length=2, default = 'IT')
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
    def __str__(self):
        return self.code


class Product(models.Model):
    asin = models.CharField(max_length=32,default='')
    parent = models.ForeignKey(ProductParent, on_delete=models.CASCADE, null = True)
    code = models.CharField(max_length=64) ## Seller's choosen SKU
    #seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    marketplace = models.CharField(max_length=2, default = 'IT')
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
    def __str__(self):
        return self.code

class Keyword(models.Model):
    keyword = models.CharField(max_length=64, null=False) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null= True, blank=True)
    marketplace =  models.CharField(max_length=3, null=False) 
    volume = models.IntegerField(null= True, blank=True)
    importance = models.SmallIntegerField(null= True, blank=True)
    def __str__(self):
        return str(self.keyword) + " - " + self.product.code + " - " + self.marketplace 
    

class AmazonRank(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null= True, blank=True)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    day = models.DateField(null=False)
    indexed = models.BooleanField(default = False)
    amazon_choice = models.BooleanField(default = False)
    rank =  models.SmallIntegerField(default = 0)
    rank_sponsored =  models.SmallIntegerField(default = 0)
    page =  models.SmallIntegerField(null=True, blank=True,default = 0)
    pos_in_page =  models.SmallIntegerField(null=True, blank=True, default = 0)
    pos_in_page_sponsored =  models.SmallIntegerField(null=True, blank=True, default = 0)
    top_seller = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now=True, null = True)

    def __str__(self):
        return str(self.keyword) + " | " + self.day.strftime("%d/%m/%y")