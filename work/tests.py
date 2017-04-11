from django.test import TestCase

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token

from work.views import create_work
from worktype.models import WorkType
from customer.models import Customer, Address
from django.contrib.auth.models import User 


# Create your tests here.
class WorkTypeTestCase(TestCase):

    def setUp(self):
        self.worktype = WorkType.objects.create(name = "Carpintería", description = "Un trabajo muy duro", icon = "random/url.png" )
        user = User(first_name = 'testFN', \
                        last_name = 'testLN' ,   \
                        username = 'testusername',     \
                        email = 'test@email.com')
        user.set_password('testpassword')
        user.save()
        self.user = user
        customer = Customer(user = user, city = 'testCity', phone = '+573002525365')
        customer.save()
        self.customer = customer
        address = Address(name = 'name', \
                        address = 'address', \
                        city = 'city',       \
                        country = 'country', \
                        customer = customer)
        address.save()
        self.address = address

        self.token = Token.objects.get(user__username='testusername')

    def test_create_work_response(self):
        """Wortypes are correctly created"""
        worktype = WorkType.objects.get(name = "Carpintería")
        
        print("hay un total de " + str(len(WorkType.objects.all())))

        factory = APIRequestFactory()
        user = User.objects.get(username='testusername')

        request_body = {
            "worktypeid": self.worktype.id,
            "date": "2017-03-30T01:36:30.023Z",
            "description": "Se me dañó la ducha D:",
            "addressid": self.address.id,
            "images":[]
        }
        request = factory.post('/api/work/', request_body)
        force_authenticate(request, user=user, token=self.token.key)
        response = create_work(request)

        self.assertEqual(response.status_code, 201, 'It should return 201, created')
        self.assertEqual(response.data['id'], 1, 'It should return workid id 1')
        self.assertEqual(response.data['description'], 'Se me dañó la ducha D:', 'It should hace a description')
        self.assertEqual(response.data['state'], 'ORDERED', 'It should be ordered')
