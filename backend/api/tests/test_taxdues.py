import json
from django.test import override_settings

from django_hosts import reverse

from .test_setup import TestSetup

@override_settings(DEFAULT_HOST='api')
class TaxpayersTests(TestSetup):

    def setUp(self):
        self.taxduesCRUD_url = reverse(viewname="taxdues")                
        return super().setUp()

    def test_createTaxDue_asTaxPayer(self):
        data = { "product_taxdetails": [ { "interstate": False, "value": "15000.00", "product": 1, "taxpayer": 1 } ], "service_taxdetails": [ {  "interstate": False, "value": "10000.00", "service": 1, "taxpayer": 1 } ], "taxpayer": 1,"dueon": "2022-03-22T05:06:51Z", "ispaid": False }
        loginres = self.client.post(self.login_url,{"username": "taxpayer", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        res = self.client.post(self.taxduesCRUD_url,data)
        self.assertEqual(res.status_code, 403)

    def test_createTaxDue_asTaxAccountant(self):
        data = "{ \"id\": 1, \"product_taxdetails\": [ { \"id\": 1, \"interstate\": false, \"value\": \"15000.00\", \"product\": 1, \"taxpayer\": 1 }], \"service_taxdetails\": [ { \"id\": 1, \"interstate\": false, \"value\": \"10000.00\", \"service\": 1, \"taxpayer\": 1 } ], \"taxpayer\": 1, \"generatedon\": \"2022-02-22T05:06:56.500778Z\", \"editedon\": \"2022-02-22T05:06:56.500778Z\", \"dueon\": \"2022-03-22T05:06:51Z\", \"ispaid\": false }"
        loginres = self.client.post(self.login_url,{"username": "taxaccountant", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        res = self.client.post(self.taxduesCRUD_url,data,content_type="application/json")
        content = json.loads(res.content)
        cgst =  content.get("cgst")
        sgst =  content.get("sgst")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(cgst, '2250.00')
        self.assertEqual(sgst, '2250.00')

    def test_createTaxDue_asTaxAccountant_with_interstate_decimals(self):
        data = "{ \"id\": 1, \"product_taxdetails\": [ { \"id\": 1, \"interstate\": true, \"value\": \"15000.00\", \"product\": 1, \"taxpayer\": 1 }], \"service_taxdetails\": [ { \"id\": 1, \"interstate\": false, \"value\": \"22520.00\", \"service\": 1, \"taxpayer\": 1 } ], \"taxpayer\": 1, \"generatedon\": \"2022-02-22T05:06:56.500778Z\", \"editedon\": \"2022-02-22T05:06:56.500778Z\", \"dueon\": \"2022-03-22T05:06:51Z\", \"ispaid\": false }"
        loginres = self.client.post(self.login_url,{"username": "taxaccountant", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        res = self.client.post(self.taxduesCRUD_url,data,content_type="application/json")
        content = json.loads(res.content)
        cgst =  content.get("cgst")
        sgst =  content.get("sgst")
        igst =  content.get("igst")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(cgst, '2026.80')
        self.assertEqual(sgst, '2026.80')
        self.assertEqual(igst, '2700.00')

    def test_createTaxDue_asTaxAccountant_with_otherterritory_decimals(self):
        data = "{ \"product_taxdetails\": [ { \"interstate\": true, \"value\": \"15000.00\", \"product\": 3, \"taxpayer\": 2 }], \"service_taxdetails\": [ { \"id\": 1, \"interstate\": false, \"value\": \"22520.00\", \"service\": 2, \"taxpayer\": 2 } ], \"taxpayer\": 2, \"generatedon\": \"2022-02-22T05:06:56.500778Z\", \"editedon\": \"2022-02-22T05:06:56.500778Z\", \"dueon\": \"2022-03-22T05:06:51Z\", \"ispaid\": false }"
        loginres = self.client.post(self.login_url,{"username": "taxaccountant", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        res = self.client.post(self.taxduesCRUD_url,data,content_type="application/json")
        content = json.loads(res.content)
        cgst =  content.get("cgst")
        sgst =  content.get("sgst")
        igst =  content.get("igst")
        ugst =  content.get("ugst")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(cgst, '2026.80')
        self.assertEqual(sgst, '0.00')
        self.assertEqual(igst, '2700.00')
        self.assertEqual(ugst, '2026.80')

    def test_createTaxDue_asTaxAccountant_with_interstate_decimals_cess(self):
        data = "{ \"id\": 1, \"product_taxdetails\": [ {  \"interstate\": true, \"value\": \"15000.00\", \"product\": 1, \"taxpayer\": 1 },{  \"interstate\": true, \"value\": \"15000.00\", \"product\": 2, \"taxpayer\": 1 }], \"service_taxdetails\": [ { \"id\": 1, \"interstate\": false, \"value\": \"22520.00\", \"service\": 1, \"taxpayer\": 1 } ], \"taxpayer\": 1, \"generatedon\": \"2022-02-22T05:06:56.500778Z\", \"editedon\": \"2022-02-22T05:06:56.500778Z\", \"dueon\": \"2022-03-22T05:06:51Z\", \"ispaid\": false }"
        loginres = self.client.post(self.login_url,{"username": "taxaccountant", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        res = self.client.post(self.taxduesCRUD_url,data,content_type="application/json")
        content = json.loads(res.content)
        cgst =  content.get("cgst")
        sgst =  content.get("sgst")
        igst =  content.get("igst")        
        cess =  content.get("cess")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(cgst, '2026.80')
        self.assertEqual(sgst, '2026.80')
        self.assertEqual(igst, '4500.00')
        self.assertEqual(cess, '1500.00')
    
    def test_createTaxDue_and_EditTaxDue_asTaxAccountant_with_interstate_decimals_cess(self):
        data = "{ \"product_taxdetails\": [ {  \"interstate\": true, \"value\": \"15000.00\", \"product\": 1, \"taxpayer\": 1 },{  \"interstate\": true, \"value\": \"15000.00\", \"product\": 2, \"taxpayer\": 1 }], \"service_taxdetails\": [ { \"id\": 1, \"interstate\": false, \"value\": \"22520.00\", \"service\": 1, \"taxpayer\": 1 } ], \"taxpayer\": 1, \"generatedon\": \"2022-02-22T05:06:56.500778Z\", \"editedon\": \"2022-02-22T05:06:56.500778Z\", \"dueon\": \"2022-03-22T05:06:51Z\", \"ispaid\": false }"
        loginres = self.client.post(self.login_url,{"username": "taxaccountant", "password":"test@123"})
        tokens = json.loads(loginres.content).get("tokens")
        acesstoken = tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {acesstoken}')
        res = self.client.post(self.taxduesCRUD_url,data,content_type="application/json")
        content = json.loads(res.content)
        id = content.get("id")
        cgst =  content.get("cgst")
        sgst =  content.get("sgst")
        igst =  content.get("igst")        
        cess =  content.get("cess")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(cgst, '2026.80')
        self.assertEqual(sgst, '2026.80')
        self.assertEqual(igst, '4500.00')
        self.assertEqual(cess, '1500.00')
        taxduesedit_url = reverse(viewname="taxdues",args={id})
        editeddata = "{ \"product_taxdetails\": [ {  \"interstate\": true, \"value\": \"30000.00\", \"product\": 1, \"taxpayer\": 1 },{  \"interstate\": true, \"value\": \"1000.00\", \"product\": 2, \"taxpayer\": 1 }], \"service_taxdetails\": [ { \"id\": 1, \"interstate\": false, \"value\": \"22520.00\", \"service\": 1, \"taxpayer\": 1 } ], \"taxpayer\": 1, \"generatedon\": \"2022-02-22T05:06:56.500778Z\", \"editedon\": \"2022-02-22T05:06:56.500778Z\", \"dueon\": \"2022-03-22T05:06:51Z\", \"ispaid\": false }"
        edit_res = self.client.put(taxduesedit_url,editeddata,content_type="application/json")
        edited_content = json.loads(edit_res.content)
        e_cgst =  edited_content.get("cgst")
        e_sgst =  edited_content.get("sgst")
        e_igst =  edited_content.get("igst")        
        e_cess =  edited_content.get("cess")
        self.assertEqual(edit_res.status_code, 200)
        self.assertEqual(e_cgst, '4053.60')
        self.assertEqual(e_sgst, '4053.60')
        self.assertEqual(e_igst, '10020.00')
        self.assertEqual(e_cess, '1600.00')
