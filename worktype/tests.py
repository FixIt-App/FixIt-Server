from django.test import TestCase

from worktype.models import WorkType

class WorkTypeTestCase(TestCase):

    def setUp(self):
        WorkType.objects.create(name = "Carpinteria", description = "Un trabajo muy duro", icon = "random/url.png" )

    def test_works_are_created(self):
        """Wortypes are correctly created"""
        worktype = WorkType.objects.get(name = "Carpinteria")
        
        self.assertEqual(worktype.name, 'Carpinteria')
