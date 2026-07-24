from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = "__all__"

        widgets = {

            'customer_id': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'CUS1001'
            }),

            'first_name': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'gender': forms.Select(attrs={
                'class':'form-control'
            }),

            'dob': forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),

            'phone': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class':'form-control'
            }),

            'address': forms.Textarea(attrs={
                'class':'form-control',
                'rows':3
            }),

            'city': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'state': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'pincode': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'status': forms.Select(attrs={
                'class':'form-control'
            }),

        }