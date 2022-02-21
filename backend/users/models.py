from math import fabs
from django.db import models
from django.contrib.auth.models import AbstractUser as BaseAbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


from gst.models import TaxDue,ProductTaxDetails,ServiceTaxDetails
from gst.utils import CaculateTaxonProduct
# Create your models here.
class AbstractUser(BaseAbstractUser):
    
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    dp = models.URLField(null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.username}"



class AdminUser(AbstractUser):

    class Meta:
        db_table  = 'AdminUsers'

GSTINREGEXValidator = RegexValidator("^([0][1-9]|[1-2][0-9]|[3][0-7])([A-Z]{5})([0-9]{4})([A-Z]{1}[1-9A-Z]{1})([Z]{1})([0-9A-Z]{1})+$",message="GSTIN is invalid")

class TaxPayer(AbstractUser):
    taxaccountants = models.ManyToManyField('users.TaxAccountant',blank=True)
    temppassword = models.CharField(max_length=50,null=True) # Can login once only - will be created if Taxpayer is created by TaxAccountant or Admin
    istemppassword = models.BooleanField(default=False)
    isotherterritory = models.BooleanField(default=False)
    gstin = models.CharField(max_length=15,validators=[GSTINREGEXValidator])

    class Meta:
        db_table  = 'TaxPayers'
        ordering = ('-id',)

class TaxAccountant(AbstractUser):    
    taxpayers = models.ManyToManyField(TaxPayer,blank=True,through=TaxPayer.taxaccountants.through)

    class Meta:
        db_table  = 'TaxAccountants'
        ordering = ('-id',)

    def GenerateTaxDue(self,Ptaxdetails:list[ProductTaxDetails],Staxdetails:list[ServiceTaxDetails],taxpayerid:int):
        cgst,sgst,ugst,igst,cess = 0
        taxdue:TaxDue =  TaxDue(cgst,sgst,ugst,igst,cess)
        taxdue.taxpayer_id = taxpayerid
        taxdue.generatedby = self
        taxdue.save()
        for ptaxdetail in Ptaxdetails:
            ptaxdetail.taxdue = taxdue.id
            p_cgst,p_sgst,p_ugst,p_igst,p_cess = CaculateTaxonProduct(ptaxdetail)
            taxdue.cgst += p_cgst
            taxdue.sgst += p_sgst
            taxdue.ugst += p_ugst
            taxdue.igst += p_igst
            taxdue.cess += p_cess
        for staxdetail in Staxdetails:
            staxdetail.taxdue = taxdue.id
            s_cgst,s_sgst,s_ugst,s_igst,s_cess = CaculateTaxonProduct(staxdetail)
            taxdue.cgst += s_cgst
            taxdue.sgst += s_sgst
            taxdue.ugst += s_ugst
            taxdue.igst += s_igst
            taxdue.cess += s_cess
        taxdue.save()
        ProductTaxDetails.objects.bulk_create(Ptaxdetails)
        ServiceTaxDetails.objects.bulk_create(Staxdetails)
        return taxdue