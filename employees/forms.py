from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):

    class Meta:

        model = Employee

        fields = "__all__"

        widgets = {

            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'EMP1001'
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),

            'dob': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'department': forms.Select(attrs={
                'class': 'form-control'
            }),

            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Software Engineer'
            }),

            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '50000'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9876543210'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'employee@gmail.com'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter Address'
            }),

            'joining_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),

        }