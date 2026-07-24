from django import forms
from .models import Loan


class LoanForm(forms.ModelForm):

    class Meta:

        model = Loan

        fields = "__all__"

        widgets = {

            'loan_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'LOAN1001'
            }),

            'customer': forms.Select(attrs={
                'class': 'form-control'
            }),

            'account': forms.Select(attrs={
                'class': 'form-control'
            }),

            'loan_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'loan_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '100000'
            }),

            'interest_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '8.50'
            }),

            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '12'
            }),

            'emi': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '8500'
            }),

            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),

        }