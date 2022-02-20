"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase

from gst.utils import CaculateTax
from gst.models import TaxDetails
from users.models import TaxPayer
# TODO: Configure your database in settings.py and sync before running tests.

class SimpleTest(TestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(SimpleTest, cls).setUpClass()
        django.setup()

    def test_CalculateTax_SameState(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        txdetails = TaxDetails(value=5000,taxrate=18,taxpayer=taxpayer)
        taxes = CaculateTax(txdetails)
        self.assertEqual(taxes, (450,450,0,0,0)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_InterState(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        txdetails = TaxDetails(value=5000,taxrate=18,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTax(txdetails)
        self.assertEqual(taxes, (0,0,0,900,0)) #cgst,sgst,ugst,igst,cess
    
    def test_CalculateTax_SameState_otherTerritory(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        txdetails = TaxDetails(value=5000,taxrate=18,taxpayer=taxpayer)
        taxes = CaculateTax(txdetails)
        self.assertEqual(taxes, (450,0,450,0,0)) #cgst,sgst,ugst,igst,cess
    
    def test_CalculateTax_InterState_otherTerritory(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        txdetails = TaxDetails(value=5000,taxrate=18,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTax(txdetails)
        self.assertEqual(taxes, (0,0,0,900,0)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_SameState(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        txdetails = TaxDetails(value=5000,taxrate=18,cessrate=10,taxpayer=taxpayer)
        taxes = CaculateTax(txdetails)
        self.assertEqual(taxes, (450,450,0,0,500)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_InterState(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM")
        txdetails = TaxDetails(value=5000,taxrate=18,cessrate=10,taxpayer=taxpayer,interstate=True)
        taxes = CaculateTax(txdetails)
        self.assertEqual(taxes, (0,0,0,900,500)) #cgst,sgst,ugst,igst,cess

    def test_CalculateTax_SameState_otherTerritory(self):
        taxpayer = TaxPayer(gstin="18AABCU9603R1ZM",isotherterritory=True)
        txdetails = TaxDetails(value=5000,taxrate=18,cessrate=10,taxpayer=taxpayer,interstate=False)
        taxes = CaculateTax(txdetails)
        self.assertEqual(taxes, (450,0,450,0,500)) #cgst,sgst,ugst,igst,cess

    