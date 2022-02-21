
import json
from django.test import override_settings
from django.contrib.auth.models import Group

from django_hosts import reverse


from api.tests.test_setup import TestSetup


@override_settings(DEFAULT_HOST='api')
class AuthViewsTests(TestSetup):
    def setUp(self):
        self.taxpayersCRUD_url = reverse(viewname="taxpayers")
                
        return super().setUp()

    def test_retrieve_Single_taxpayer_withoutLogginguser(self):
        taxpayers_retrieve_url = reverse(viewname="taxpayer",args={1}) 
        res = self.client.get(taxpayers_retrieve_url)
        self.assertEqual(res.status_code, 401)

    def test_retrieve_Single_Sametaxpayer_byloggingas_TaxPayer(self):
        loginres = self.client.post(self.login_url,{"username": "taxpayer", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        taxpayers_retrieve_url = reverse(viewname="taxpayer",args={1})    
        res = self.client.get(taxpayers_retrieve_url)
        taxpayerid =  json.loads(res.content).get("id")
        username =  json.loads(res.content).get("username")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(taxpayerid, 1)
        self.assertEqual(username, "taxpayer")

    def test_retrieve_Single_Othertaxpayer_byloggingas_TaxPayer(self):
        loginres = self.client.post(self.login_url,{"username": "taxpayer", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        taxpayers_retrieve_url = reverse(viewname="taxpayer",args={2})    
        res = self.client.get(taxpayers_retrieve_url)
        self.assertEqual(res.status_code, 404)
    
    #Even though we are using pagiated endpoint, since we are logging as Taxpayer we have acess to Taxpayer data of login user only
    #So we dont show paginated response, will show normal single object response
    def test_retrieve_Multiple_Sametaxpayer_byloggingas_TaxPayer(self):
        loginres = self.client.post(self.login_url,{"username": "taxpayer", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')  
        res = self.client.get(self.taxpayersCRUD_url)
        taxpayerid =  json.loads(res.content).get("id")
        username =  json.loads(res.content).get("username")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(taxpayerid, 1)
        self.assertEqual(username, "taxpayer")

    #Login as TaxAccountant that has 2 Taxpayers
    def test_retrieve_Multiple_taxpayers_byloggingas_TaxAccountant(self):
        loginres = self.client.post(self.login_url,{"username": "taxaccountant", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        res = self.client.get(self.taxpayersCRUD_url)
        count =  json.loads(res.content).get("count")
        results = json.loads(res.content).get("results")
        taxpayerid =  results[0].get("id")
        username =  results[0].get("username")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(count, 2)
        self.assertEqual(taxpayerid, 3)
        self.assertEqual(username, "taxpayer3")

        #Login as TaxAccountant that has No Taxpayers
    def test_retrieve_Multiple_Taxpayers_byloggingas_NTaxAccountant(self):
        loginres = self.client.post(self.login_url,{"username": "taxaccountant2", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        res = self.client.get(self.taxpayersCRUD_url)
        count =  json.loads(res.content).get("count")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(count, 0)

    #Admin User Has Access to All Taxpayers
    def test_retrieve_Multiple_Taxpayers_byloggingas_AdminUser(self):
        loginres = self.client.post(self.login_url,{"username": "saivineeth", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}') 
        res = self.client.get(self.taxpayersCRUD_url)
        count =  json.loads(res.content).get("count")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(count, 4)

    def test_create_TaxPayer_byloggingas_Taxpayer(self):
        loginres = self.client.post(self.login_url,{"username": "taxpayer", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        data = {}
        res = self.client.post(self.taxpayersCRUD_url,data)
        self.assertEqual(res.status_code, 403)

    def test_create_TaxPayer_byloggingas_TaxAccountant(self):
        loginres = self.client.post(self.login_url,{"username": "taxaccountant", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        data = {"username": "taxpayer9","first_name": "","last_name": "",
        "email": "","gstin":"18AABCU9603R1ZM"}
        res = self.client.post(self.taxpayersCRUD_url,data)
        taxaccountantid =  json.loads(res.content).get("taxaccountants")
        username =  json.loads(res.content).get("username")
        self.assertEqual(taxaccountantid, [1])
        self.assertEqual(username, "taxpayer9")

    def test_create_TaxPayer_byloggingas_Admin(self):
        loginres = self.client.post(self.login_url,{"username": "adminuser", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        data = {"username": "taxpayer8","first_name": "","last_name": "",
        "email": "","gstin":"18AABCU9603R1ZM"}
        res = self.client.post(self.taxpayersCRUD_url,data)
        taxaccountantids =  json.loads(res.content).get("taxaccountants")
        username =  json.loads(res.content).get("username")
        self.assertEqual(taxaccountantids, [])
        self.assertEqual(username, "taxpayer8")