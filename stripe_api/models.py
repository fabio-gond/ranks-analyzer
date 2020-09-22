from django.db import models
from users.models import CustomUser

class Plan(models.Model):
    name = models.CharField(max_length=32, null= True, blank=True)
    code = models.CharField(max_length=32, null= True, blank=True)
    kwds_qty = models.IntegerField()
    days_step = models.SmallIntegerField(default= 3)
    interval = models.CharField(max_length=16, default = "month")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    plan_id = models.CharField(max_length=64, null= True, blank=True)
    product_id = models.CharField(max_length=64, null= True, blank=True)
    price_id = models.CharField(max_length=64, null= True, blank=True)
    active = models.BooleanField(default = True)
    currency = models.CharField(max_length=64, default= 'eur')
    interval_count = models.SmallIntegerField(default= 1) # The number of intervals (specified in the interval attribute) between subscription billings. For example, interval=month and interval_count=3 bills every 3 months.
    trial_period_days = models.SmallIntegerField(default= 0)

    def __str__(self):
        return self.name

class OneTimeProduct(models.Model):
    name = models.CharField(max_length=32, null= True, blank=True)
    code = models.CharField(max_length=32, null= True, blank=True)
    kwds_qty = models.IntegerField()
    days_step = models.SmallIntegerField(default= 3)
    interval = models.CharField(max_length=16, default = "month")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_id = models.CharField(max_length=64, null= True, blank=True)
    price_id = models.CharField(max_length=64, null= True, blank=True)
    active = models.BooleanField(default = True)
    description = models.CharField(max_length=128, null= True, blank=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    subscription_id = models.CharField(max_length=64, null= True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null= True)
    customer_id = models.CharField(max_length=64, null= True, blank=True)
    cancel_at_period_end = models.BooleanField(default = False)
    collection_method = models.CharField(max_length=32, null= True, blank=True)
    created = models.DateTimeField()
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    default_payment_method = models.CharField(max_length=64, null= True, blank=True)
    price_id = models.CharField(max_length=64, null= True, blank=True)
    product_id = models.CharField(max_length=64, null= True, blank=True)
    url = models.CharField(max_length=256, null= True, blank=True)
    latest_invoice = models.CharField(max_length=64, null= True, blank=True)
    status = models.CharField(max_length=32, null= True, blank=True)

    def __str__(self):
        return self.subscription_id

class OneTimePurchase(models.Model):
    product = models.ForeignKey(OneTimeProduct, on_delete=models.CASCADE, null= True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null= True)
    created = models.DateTimeField(auto_now_add=True)
    period_end = models.DateTimeField()
    



