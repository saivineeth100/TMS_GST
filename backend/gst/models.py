
from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from gst.utils import CaculateTaxonProduct, CaculateTaxonService


class AbstractTaxinfo(models.Model):
    name = models.CharField(max_length=50)
    taxrate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)])
    cessrate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)])
    isexempt = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ('-id',)
    
    def __str__(self):
        return self.name

class Product(AbstractTaxinfo):    
    taxpayer = models.ForeignKey('users.TaxPayer', verbose_name=_("taxpayers"), on_delete=models.CASCADE,related_name="products")
    

class Service(AbstractTaxinfo):
    taxpayer = models.ForeignKey('users.TaxPayer', verbose_name=_("taxpayers"), on_delete=models.CASCADE,related_name="services")

class AbstractTaxDetails(models.Model):
    interstate = models.BooleanField(default=False)
    value = models.DecimalField(decimal_places=2,max_digits=10)
    
    class Meta:
        abstract = True
        ordering = ('-id',)
    
    
    
class ProductTaxDetails(AbstractTaxDetails):
    product = models.ForeignKey('gst.Product', verbose_name=_("products"), on_delete=models.CASCADE,related_name="taxdetails")
    taxdue = models.ForeignKey('gst.TaxDue', verbose_name=_("taxdues"), on_delete=models.CASCADE,related_name="product_taxdetails")
    taxpayer = models.ForeignKey('users.TaxPayer', verbose_name=_("taxpayers"), on_delete=models.CASCADE,related_name="product_taxdetails")
    def __str__(self):
        return f'{self.taxpayer.username}_{self.product}'


class ServiceTaxDetails(AbstractTaxDetails):
    service = models.ForeignKey('gst.Service', verbose_name=_("services"), on_delete=models.CASCADE,related_name="taxdetails")
    taxdue = models.ForeignKey('gst.TaxDue', verbose_name=_("taxdues"), on_delete=models.CASCADE,related_name="service_taxdetails")
    taxpayer = models.ForeignKey('users.TaxPayer', verbose_name=_("taxpayers"), on_delete=models.CASCADE,related_name="service_taxdetails")
    
    def __str__(self):
        return f'{self.taxpayer.username}_{self.service}'

class TaxDue(models.Model):
    cgst = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    sgst = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    ugst = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    igst = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    cess = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    total = models.DecimalField(decimal_places=2,max_digits=1000,default=0)
    taxpayer = models.ForeignKey('users.TaxPayer', verbose_name=_("taxpayers"), on_delete=models.CASCADE,related_name="taxdues")
    generatedby = models.ForeignKey('users.TaxAccountant', verbose_name=_("taxaccountants"), on_delete=models.CASCADE,related_name="clienttaxdues")
    generatedon = models.DateTimeField(auto_now_add=True)
    editedon = models.DateTimeField(auto_now=True)
    dueon = models.DateTimeField()
    ispaid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.taxpayer.username}_{self.generatedon}'
    class Meta:
        ordering = ('-id',)
    def Recalculate(self):
        for ptaxdetail in self.product_taxdetails.all():
            p_cgst,p_sgst,p_ugst,p_igst,p_cess = CaculateTaxonProduct(ptaxdetail)
            self.cgst += p_cgst
            self.sgst += p_sgst
            self.ugst += p_ugst
            self.igst += p_igst
            self.cess += p_cess
        for staxdetail in self.service_taxdetails.all():
            s_cgst,s_sgst,s_ugst,s_igst,s_cess = CaculateTaxonService(staxdetail)
            self.cgst += s_cgst
            self.sgst += s_sgst
            self.ugst += s_ugst
            self.igst += s_igst
            self.cess += s_cess
        self.save()

    def CalculateTaxDue(self,Ptaxdetails:list[ProductTaxDetails],Staxdetails:list[ServiceTaxDetails]):
        for ptaxdetail in Ptaxdetails:
            t_taxdetail = ProductTaxDetails._default_manager.create(**ptaxdetail,taxdue=self)
            t_taxdetail.save()
            p_cgst,p_sgst,p_ugst,p_igst,p_cess = CaculateTaxonProduct(t_taxdetail)
            self.cgst += p_cgst
            self.sgst += p_sgst
            self.ugst += p_ugst
            self.igst += p_igst
            self.cess += p_cess
        for staxdetail in Staxdetails:
            s_taxdetail = ServiceTaxDetails._default_manager.create(**staxdetail,taxdue=self)
            s_cgst,s_sgst,s_ugst,s_igst,s_cess = CaculateTaxonService(s_taxdetail)
            self.cgst += s_cgst
            self.sgst += s_sgst
            self.ugst += s_ugst
            self.igst += s_igst
            self.cess += s_cess
        self.save()
        # ProductTaxDetails.objects.bulk_create(Ptaxdetails)
        # ServiceTaxDetails.objects.bulk_create(Staxdetails)
        return self
    
        