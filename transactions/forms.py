from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:

        model = Transaction

        fields = "__all__"

        widgets = {

            'account': forms.Select(attrs={
                'class': 'form-control'
            }),

            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

        }