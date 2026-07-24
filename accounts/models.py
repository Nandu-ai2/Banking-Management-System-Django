from django.db import models
from customers.models import Customer


class Account(models.Model):

    ACCOUNT_TYPES = [
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    ]

    STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    account_number = models.CharField(
        max_length=20,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="accounts"
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField()

    address = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.account_number} - {self.customer.first_name} {self.customer.last_name}"