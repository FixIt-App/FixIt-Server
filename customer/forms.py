from django.forms import ModelForm
from customer.models import Address

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address', 'city', 'country']