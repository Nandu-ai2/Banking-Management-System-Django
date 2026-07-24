from django.db import models
from customers.models import Customer
from accounts.models import Account


class Loan(models.Model):

    LOAN_TYPES = [
        ('Home', 'Home'),
        ('Personal', 'Personal'),
        ('Education', 'Education'),
        ('Vehicle', 'Vehicle'),
        ('Business', 'Business'),
    ]

    STATUS = [
        ('Active', 'Active'),
        ('Closed', 'Closed'),
    ]

    loan_number = models.CharField(
        max_length=20,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )

    loan_type = models.CharField(
        max_length=20,
        choices=LOAN_TYPES
    )

    loan_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    duration = models.IntegerField(
        help_text="Months"
    )

    emi = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.loan_number