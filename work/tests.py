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

    fixtures = ['data']

    def setUp(self):
        self.token = Token.objects.get(user__username='david')

    def test_create_work_response(self):
        """Wortypes are correctly created"""
        worktype = WorkType.objects.get(pk = 1)
        address = Address.objects.get(pk = 1)

        factory = APIRequestFactory()
        user = User.objects.get(pk = 1)

        request_body = {
            "worktypeid": worktype.id,
            "date": "2017-03-30T01:36:30.023Z",
            "description": "Se me dañó la ducha D:",
            "addressid": address.id,
            "images":[]
        }
        request = factory.post('/api/work/', request_body)
        force_authenticate(request, user=user, token=self.token.key)
        
        response = create_work(request)

        self.assertEqual(response.status_code, 201, 'It should return 201, created')
        self.assertEqual(response.data['state'], 'ORDERED', 'It should be ordered')
        
