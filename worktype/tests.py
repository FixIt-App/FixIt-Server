from django.test import TestCase

from worktype.models import WorkType

class WorkTypeTestCase(TestCase):

    def setUp(self):
        WorkType.objects.create(name = "Carpintería", description = "Un trabajo muy duro", icon = "random/url.png" )

    def test_works_are_created(self):
        """Wortypes are correctly created"""
        worktype = WorkType.objects.get(name = "Carpintería")
        
        self.assertEqual(worktype.name, 'Carpinteríaaa', 'it should find the user and return the same name')
