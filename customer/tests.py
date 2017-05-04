from django.test import TestCase
from django.contrib.auth.models import User 

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token

from customer.views import confirm_phone, CustomerDetail
from customer.models import Customer
from customer.models import Confirmation

class ConfirmationTests(TestCase):

    fixtures = ['data_customer']

    def test_confirm_sms(self):
        """
            sms correct confirmation
        """
        token = Token.objects.get(user__id = 1)
        factory = APIRequestFactory()
        user = User.objects.get(pk = 1)

        request_body = {
            "code": "4321",
        }
        request = factory.post('/api/phone/confirmations/', request_body)
        force_authenticate(request, user=user, token = token.key)
        response = confirm_phone(request)

        confirmation = Confirmation.objects.get(pk = 1)
        self.assertEqual(response.status_code, 200, 'It should return ok when confirming phone')
        self.assertEqual(confirmation.state, True, 'It should update the confirmation state correctly')

class ConfirmEmail(TestCase):

    fixtures = ['data_customer']

    def test_confirm_email(self):
        response = self.client.get('/confirmations/thi-sis-afa-ket-oke-n/')
        self.assertEqual(response.status_code, 200, 'It should successfully confirm the user')
        confirmation = Confirmation.objects.get(pk = 2)
        self.assertEqual(confirmation.state, True, 'It should update the confirmation state')

    def test_fail_email_confirmation(self):
        response = self.client.get('/confirmations/thiaaa-sis-afa-ket-oke-n/')
        self.assertEqual(response.status_code, 404, 'It should not find the confirmation')

class UpdateCustomer(TestCase):

    fixtures = ['data_customer']

    def setUp(self):
        self.token = Token.objects.get(user__username='davidfcalle@gmail.com')
        self.user = User.objects.get(pk = 1)
        self.customer = Customer.objects.get(pk = 1)

    def test_update_email(self):
        factory = APIRequestFactory()

        request_body = {
            "email": "test@test.test",
        }

        request = factory.put('/api/customers/' + str(self.customer.id) + '/', request_body)
        force_authenticate(request, user=self.user, token=self.token.key)
        
        response = CustomerDetail.as_view()(request,  self.customer.id)
        self.assertEqual(response.status_code, 200, 'It should return 200, modified')

        updatedCustomer = Customer.objects.get(pk = 1)
        self.assertEqual(updatedCustomer.user.email, "test@test.test", 'Email should be modified')

        self.assertEqual(updatedCustomer.user.username, "test@test.test", 'Username should be modified')

    def test_update_duplicate_email(self):
        factory = APIRequestFactory()
        other = User.objects.get(pk = 2)
        request_body = {
            "email": other.email,
        }

        prevEmail = self.user.email

        request = factory.put('/api/customers/' + str(self.customer.id) + '/', request_body)
        force_authenticate(request, user=self.user, token=self.token.key)
        
        response = CustomerDetail.as_view()(request,  self.customer.id)
        self.assertEqual(response.status_code, 400, 'It should return 400, duplicated email')

        updatedCustomer = Customer.objects.get(pk = 1)
        self.assertEqual(updatedCustomer.user.email, prevEmail, 'Email should not change')

    def test_update_duplicate_phone(self):
        factory = APIRequestFactory()
        other = Customer.objects.get(pk = 9)
        request_body = {
            "phone": other.phone,
        }

        prevPhone = self.customer.phone

        request = factory.put('/api/customers/' + str(self.customer.id) + '/', request_body)
        force_authenticate(request, user=self.user, token=self.token.key)
        
        response = CustomerDetail.as_view()(request,  self.customer.id)
        self.assertEqual(response.status_code, 400, 'It should return 400, duplicated phone')

        updatedCustomer = Customer.objects.get(pk = 1)
        self.assertEqual(updatedCustomer.phone, prevPhone, 'Phone should not change')
