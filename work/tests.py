from django.test import TestCase

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token

from work.views import create_work, WorkDetail
from worktype.models import WorkType
from customer.models import Customer, Address
from django.contrib.auth.models import User 
from work.models import Work
from image.models import Image


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

    def test_work_modified(self):
        work = Work.objects.get(pk = 1)
        image = Image.objects.get(pk = 1)

        factory = APIRequestFactory()
        user = User.objects.get(pk = 1)
        request_body = {
            "description": "new description",
            "images":[ str(image.id) ]
        }

        request = factory.put('/api/work/' + str(work.id) + '/', request_body)
        force_authenticate(request, user=user, token=self.token.key)
        
        response = WorkDetail.as_view()(request,  work.id)
        self.assertEqual(response.status_code, 200, 'It should return 200, modified')

        imageUpdated = Image.objects.get(pk = 1)    
        self.assertEqual(work.id, imageUpdated.work.id, 'Work id in image shoud be updated')

        workUpdated = Work.objects.get(pk = 1)
        self.assertEqual("new description", workUpdated.description, "description in work should be updated")

    def test_work_modified_forbidden(self):
        work = Work.objects.get(pk = 1)
        image = Image.objects.get(pk = 1)

        factory = APIRequestFactory()
        user = User.objects.get(pk = 2)
        request_body = {
            "description": "new description",
            "images":[ str(image.id) ]
        }

        request = factory.put('/api/work/' + str(work.id) + '/', request_body)
        force_authenticate(request, user=user, token=self.token.key)
        
        response = WorkDetail.as_view()(request,  work.id)
        self.assertEqual(response.status_code, 403, 'It should return 403, forbidden: user not owner of work')

        
