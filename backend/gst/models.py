
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class AbstractTaxinfo(models.Model):
    name = models.CharField(max_length=50)
    taxrate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)])
    cessrate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)])
    isexempt = models.BooleanField(default=False)

    class Meta:
        abstract = True
    
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
    cgst = models.DecimalField(decimal_places=2,max_digits=10)
    sgst = models.DecimalField(decimal_places=2,max_digits=10)
    ugst = models.DecimalField(decimal_places=2,max_digits=10)
    igst = models.DecimalField(decimal_places=2,max_digits=10)
    cess = models.DecimalField(decimal_places=2,max_digits=10)
    total = models.DecimalField(decimal_places=2,max_digits=1000)
    taxpayer = models.ForeignKey('users.TaxPayer', verbose_name=_("taxpayers"), on_delete=models.CASCADE,related_name="taxdues")
    generatedby = models.ForeignKey('users.TaxAccountant', verbose_name=_("taxaccountants"), on_delete=models.CASCADE,related_name="clienttaxdues")
    generatedon = models.DateTimeField(auto_now_add=True)
    editedon = models.DateTimeField(auto_now=True)
    dueon = models.DateTimeField()
    ispaid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.taxpayer.username}_{self.generatedon}'
    
        