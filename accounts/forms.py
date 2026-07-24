from django import forms
from .models import Account


class AccountForm(forms.ModelForm):

    class Meta:

        model = Account

        fields = [
            'account_number',
            'customer',
            'account_type',
            'balance',
            'phone',
            'email',
            'address',
            'status'
        ]

        widgets = {

            'account_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'customer': forms.Select(attrs={
                'class': 'form-control'
            }),

            'account_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'balance': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),

        }