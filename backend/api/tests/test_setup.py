from unicodedata import name
from rest_framework.test import APITestCase
from django_hosts import reverse


class TestSetup(APITestCase):
    fixtures = ['users','gst']
    def setUp(self):
        self.login_url = reverse(viewname="login")
        return super().setUp()

    def tearDown(self):
        return super().tearDown()