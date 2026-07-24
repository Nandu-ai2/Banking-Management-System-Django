from django.db import models


class Employee(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    DEPARTMENT_CHOICES = [
        ('Accounts', 'Accounts'),
        ('Loans', 'Loans'),
        ('Customer Service', 'Customer Service'),
        ('Cash', 'Cash'),
        ('IT', 'IT'),
        ('HR', 'HR'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    employee_id = models.CharField(
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
        choices=GENDER_CHOICES
    )

    dob = models.DateField()

    department = models.CharField(
        max_length=30,
        choices=DEPARTMENT_CHOICES
    )

    designation = models.CharField(
        max_length=50
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        unique=True
    )

    address = models.TextField()

    joining_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['-created_at']

        verbose_name = "Employee"

        verbose_name_plural = "Employees"

    def __str__(self):

        return f"{self.employee_id} - {self.first_name} {self.last_name}"