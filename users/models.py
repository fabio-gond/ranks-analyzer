from django.contrib.auth.models import AbstractUser
from django.db import models
#from stripe_api.models import Plan, OneTimeProduct


class CustomUser(AbstractUser):
    # add additional fields in here
    # Where did I contacted the customer
    platform = models.CharField(max_length=32, null=True, blank=True)
    other = models.CharField(max_length=64, null=True, blank=True)
    """ plan = models.ForeignKey(
        Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='plans')
    plan_current_checkout = models.ForeignKey(
        Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='plans_current_checkout')
    plan_paid_until = models.DateField(null=True)
    one_time_product = models.ForeignKey(
        OneTimeProduct, on_delete=models.SET_NULL, null=True, blank=True, related_name='stripe_products')
    one_time_current_checkout = models.ForeignKey(
        OneTimeProduct, on_delete=models.SET_NULL, null=True, blank=True, related_name='stripe_products_current_checkout')
    one_time_paid_until = models.DateField(null=True) """
    stripe_email = models.CharField(max_length=64, null=True, blank=True)
    stripe_cust_id = models.CharField(max_length=32, null=True, blank=True)
    stripe_checkout_session_id = models.CharField(
        max_length=128, null=True, blank=True)

    def __str__(self):
        return self.email
