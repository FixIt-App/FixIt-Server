from django.test import TestCase

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token

from work.views import create_work, WorkDetail, get_my_works, assign_work
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


    def test_get_my_works_filter(self):
        """My works and its filters"""

        factory = APIRequestFactory()
        user = User.objects.get(pk = 1)

        request = factory.get('/api/myworks/')
        force_authenticate(request, user=user, token=self.token.key)
        
        response = get_my_works(request)

        self.assertEqual(response.status_code, 200, 'It should return 200, ok')
        self.assertEqual(len(response.data), 2, 'It should have 2 works regardless of the state')

        # finished works

        request = factory.get('/api/myworks/?state=FINISHED')
        force_authenticate(request, user=user, token=self.token.key)
        
        response = get_my_works(request)

        self.assertEqual(response.status_code, 200, 'It should return 200, ok')
        self.assertEqual(len(response.data), 1, 'It should have 1 finished work')


        request = factory.get('/api/myworks/?state=ORDERED')
        force_authenticate(request, user=user, token=self.token.key)
        
        response = get_my_works(request)

        self.assertEqual(response.status_code, 200, 'It should return 200, ok')
        self.assertEqual(len(response.data), 1, 'It should have 1 ordered work')
    
    def test_get_my_works_multiple_filter(self):
        """My works and its multiple filters"""

        factory = APIRequestFactory()
        user = User.objects.get(pk = 1)

        request = factory.get('/api/myworks/?state=ORDERED,FINISHED')
        force_authenticate(request, user=user, token=self.token.key)
        
        response = get_my_works(request)

        self.assertEqual(response.status_code, 200, 'It should return 200, ok')
        self.assertEqual(len(response.data), 2, 'Multistate filter should have 2 works')

        self.assertEqual(len(list(filter(lambda work: work.get('state') == 'FINISHED', 
            response.data))), 1, 'Multistate filter should have 1 work finished')

        self.assertEqual(len(list(filter(lambda work: work.get('state') == 'ORDERED', 
            response.data))), 1, 'Multistate filter should have 1 work ordered')

    def test_cancel_work(self):

        factory = APIRequestFactory()
        user = User.objects.get(pk = 1)

        request = factory.delete('/api/work/1/', None)
        force_authenticate(request, user = user.id, token = self.token.key)
        
        response = WorkDetail.as_view()(request, Work.objects.get(pk = 1).id)

        self.assertEqual(response.status_code, 200, 'It should have succesfully updated the service')
        work = Work.objects.get(pk = 1)

        self.assertEqual(work.state, 'CANCELED', 'It should have updated the state to canceled')

    def test_cancel_work_forbidden(self):

        token = Token.objects.get(user__id = 2)
        factory = APIRequestFactory()
        user = User.objects.get(pk = 2)

        request_body = { }
        request = factory.delete('/api/work/1/', request_body)
        force_authenticate(request, user = user, token = token.key)
        
        response = WorkDetail.as_view()(request, "1")

        self.assertEqual(response.status_code, 403, 'It should not be able to cancel works')
        work = Work.objects.get(pk = 1)

        self.assertEqual(work.state, 'ORDERED', 'It should not update the work state')

    def test_cancel_work_not_found(self):

        token = Token.objects.get(user__id = 2)
        factory = APIRequestFactory()
        user = User.objects.get(pk = 2)

        request_body = { }
        request = factory.delete('/api/work/112321/', request_body)
        force_authenticate(request, user = user, token = token.key)
        
        response = WorkDetail.as_view()(request, '112321')

        self.assertEqual(response.status_code, 404, 'It should not find the work')
    
    def test_assign_work(self):
        token = Token.objects.get(user__id = 17)
        factory = APIRequestFactory()
        user = User.objects.get(pk = 17)

        request_body = { }
        request = factory.post('/api/work/1/worker/', request_body)
        force_authenticate(request, user = user, token = token.key)

        response = assign_work(request, '1')
        self.assertEqual(response.status_code, 200, 'It should successfully assign work to a work with no worker')
        work = Work.objects.get(pk = 1)
        self.assertEqual(work.worker.user.id, 17, 'It should correctly update de the worker works')


    def test_fail_to_assign_work_abbilities(self):
        token = Token.objects.get(user__id = 18)
        factory = APIRequestFactory()
        user = User.objects.get(pk = 18)

        request_body = { }
        request = factory.post('/api/work/1/worker/', request_body)
        force_authenticate(request, user = user, token = token.key)

        response = assign_work(request, '1')
        self.assertEqual(response.status_code, 422, 'It should not be able to assign work to a worker with no capabilities')
        work = Work.objects.get(pk = 1)
        self.assertEqual(work.worker, None, 'It shoud not have an assigned worker')

    
    def test_fail_to_assign_already_assigned(self):
        token = Token.objects.get(user__id = 17)
        factory = APIRequestFactory()
        user = User.objects.get(pk = 17)
        request_body = { }
        request = factory.post('/api/work/50/worker/', request_body)
        force_authenticate(request, user = user, token = token.key)

        response = assign_work(request, '50')
        self.assertEqual(response.status_code, 403, 'It should not be able to assign work work with a worker')


