from django import forms

class WorkForm(forms.Form):
    addressId = forms.DecimalField(label='addressId', min_value=1)
    date = forms.CharField()