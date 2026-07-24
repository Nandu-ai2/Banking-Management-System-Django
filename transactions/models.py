from django.db import models
from accounts.models import Account


class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer', 'Transfer'),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    transaction_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.account.account_number} - {self.transaction_type}"