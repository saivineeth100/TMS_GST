from django.db import models

# Create your models here.
class TaxDue(models.Model):
    tax_type = models.CharField(max_length=10)    