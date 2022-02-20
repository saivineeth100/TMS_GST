

from django.test import override_settings
from .test_setup import TestSetup

@override_settings(DEFAULT_HOST='api')
class AuthViewsTests(TestSetup):

    fixtures = ['users']

    def test_Login_Emptydata(self):
        res = self.client.post(self.login_url)
        self.assertEqual(res.status_code, 400)
    
    def test_Login_Wrongdata(self):
        data = {"username": "saivineeth", "password":"testwrongpassword"}
        res = self.client.post(self.login_url,data)
        self.assertEqual(res.status_code, 401)
    
    def test_login_Admin_user(self):
        data = {"username": "saivineeth", "password":"test@123"}
        res = self.client.post(self.login_url,data)
        self.assertEqual(res.status_code, 200)

    def test_login_TaxAccountant_user(self):
        data = {"username": "taxaccountant", "password":"test@123"}
        res = self.client.post(self.login_url,data)
        self.assertEqual(res.status_code, 200)

    def test_login_TaxPayer_user(self):
        data = {"username": "taxpayer", "password":"test@123"}
        res = self.client.post(self.login_url,data)
        self.assertEqual(res.status_code, 200)