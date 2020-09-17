from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import *

PAYMENT_OPTIONS = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class commentForm(forms.Form):
    content = forms.CharField(label='Comments', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'What is in you mind',
        'cols': '100',
        'rows': '2'
    }))


class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField()
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    zip_code = forms.CharField()
    same_contact_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=PAYMENT_OPTIONS)


class Payment_form(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('stripe_charge_id',)


class RequestRefundForm(forms.Form):
    ref_code = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter reference code',
        }
    ))
    message = forms.CharField(widget=forms.Textarea(

        attrs={
            'class': 'form-control',
            'placeholder': 'Enter messages',
            'rows': 4
        }
    ))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
    }))


class ContractForm(forms.Form):
    agree = forms.BooleanField()


class UnknownUserContactForm(forms.Form):
    contact_name = forms.CharField()
    contact_email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
    }))
    contact_phone = forms.CharField()
    contact_company = forms.CharField()
    contact_message = forms.CharField(widget=forms.Textarea(

        attrs={
            'class': 'form-control',
            'placeholder': 'Enter messages',
            'rows': 4
        }
    ))
