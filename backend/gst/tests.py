"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase

from gst.utils import CaculateTaxonProduct,CaculateTaxonService
from gst.models import ProductTaxDetails,Product,ServiceTaxDetails,Service
from users.models import TaxPayer
# TODO: Configure your database in settings.py and sync before running tests.

class GSTUtilsTests(TestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(GSTUtilsTests, cls).setUpClass()
        django.setup()

    def test_CalculateTax_SameState(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        product = Product(name="sampleproduct",taxrate=18)
        txdetails = ProductTaxDetails(value=5000,product=product,taxpayer=taxpayer)
        taxes = CaculateTaxonProduct(txdetails)
        self.assertEqual(taxes, (450,450,0,0,0)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_InterState(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        product = Product(name="sampleproduct",taxrate=18)
        txdetails = ProductTaxDetails(value=5000,product=product,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTaxonProduct(txdetails)
        self.assertEqual(taxes, (0,0,0,900,0)) #cgst,sgst,ugst,igst,cess
    
    def test_CalculateTax_SameState_otherTerritory(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        product = Product(name="sampleproduct",taxrate=18)
        txdetails = ProductTaxDetails(value=5000,product=product,taxpayer=taxpayer)
        taxes = CaculateTaxonProduct(txdetails)
        self.assertEqual(taxes, (450,0,450,0,0)) #cgst,sgst,ugst,igst,cess
    
    def test_CalculateTax_InterState_otherTerritory(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        product = Product(name="sampleproduct",taxrate=18)
        txdetails = ProductTaxDetails(value=5000,product=product,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTaxonProduct(txdetails)
        self.assertEqual(taxes, (0,0,0,900,0)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_SameState_withcess(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        product = Product(name="sampleproduct",taxrate=18,cessrate=10,)
        txdetails = ProductTaxDetails(value=5000,product=product,taxpayer=taxpayer)
        taxes = CaculateTaxonProduct(txdetails)
        self.assertEqual(taxes, (450,450,0,0,500)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_InterState_withcess(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        product = Product(name="sampleproduct",taxrate=18,cessrate=10)
        txdetails = ProductTaxDetails(value=5000,product=product,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTaxonProduct(txdetails)
        self.assertEqual(taxes, (0,0,0,900,500)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_SameState_otherTerritory_withcess(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        product = Product(name="sampleproduct",taxrate=18,cessrate=10)
        txdetails = ProductTaxDetails(value=5000,product=product,taxpayer=taxpayer,interstate=False)
        taxes = CaculateTaxonProduct(txdetails)
        self.assertEqual(taxes, (450,0,450,0,500)) #cgst,sgst,ugst,igst,cess

    

#Service

    def test_CalculateTax_SameState_Service(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        service = Service(name="sampleproduct",taxrate=18)
        txdetails = ServiceTaxDetails(value=5000,service=service,taxpayer=taxpayer)
        taxes = CaculateTaxonService(txdetails)
        self.assertEqual(taxes, (450,450,0,0,0)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_InterState_Service(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        service = Service(name="sampleproduct",taxrate=18)
        txdetails = ServiceTaxDetails(value=5000,service=service,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTaxonService(txdetails)
        self.assertEqual(taxes, (0,0,0,900,0)) #cgst,sgst,ugst,igst,cess
    
    def test_CalculateTax_SameState_otherTerritory_Service(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        service = Service(name="sampleproduct",taxrate=18)
        txdetails = ServiceTaxDetails(value=5000,service=service,taxpayer=taxpayer)
        taxes = CaculateTaxonService(txdetails)
        self.assertEqual(taxes, (450,0,450,0,0)) #cgst,sgst,ugst,igst,cess
    
    def test_CalculateTax_InterState_otherTerritory_Service(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        service = Service(name="sampleproduct",taxrate=18)
        txdetails = ServiceTaxDetails(value=5000,service=service,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTaxonService(txdetails)
        self.assertEqual(taxes, (0,0,0,900,0)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_SameState_withcess_Service(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        service = Service(name="sampleproduct",taxrate=18,cessrate=10,)
        txdetails = ServiceTaxDetails(value=5000,service=service,taxpayer=taxpayer)
        taxes = CaculateTaxonService(txdetails)
        self.assertEqual(taxes, (450,450,0,0,500)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_InterState_withcess_Service(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        service = Service(name="sampleproduct",taxrate=18,cessrate=10)
        txdetails = ServiceTaxDetails(value=5000,service=service,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTaxonService(txdetails)
        self.assertEqual(taxes, (0,0,0,900,500)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_SameState_otherTerritory_withcess_Service(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        service = Service(name="sampleproduct",taxrate=18,cessrate=10)
        txdetails = ServiceTaxDetails(value=5000,service=service,taxpayer=taxpayer,interstate=False)
        taxes = CaculateTaxonService(txdetails)
        self.assertEqual(taxes, (450,0,450,0,500)) #cgst,sgst,ugst,igst,cess