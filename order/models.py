"""Doctype"""
from itertools import product
from django.contrib.auth.models import User
from django.db import models
from product.models import Product

# Create your models here.
class Order(models.Model):
    """
    Represents an order placed by a user.
    """

    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = (
        (ORDERED, 'ordered'),
        (SHIPPED, 'shipped')
    )

    user = models.ForeignKey(
        User,
        related_name='orders',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

class Meta:
    """
    Metadata options for the OrderItem model.
    """
    ordering = ('-created_at',)


class OrderItem(models.Model):
    """
    Represents an item in an order.
    """

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
