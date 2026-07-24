from django.db import models


class Customer(models.Model):

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    customer_id = models.CharField(
        max_length=20,
        unique=True
    )

    first_name = models.CharField(
        max_length=50
    )

    last_name = models.CharField(
        max_length=50
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER
    )

    dob = models.DateField()

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        unique=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=50
    )

    state = models.CharField(
        max_length=50
    )

    pincode = models.CharField(
        max_length=10
    )

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
        return f"{self.customer_id} - {self.first_name} {self.last_name}"