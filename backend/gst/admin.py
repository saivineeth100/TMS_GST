from itertools import product
from django.contrib import admin
from gst.models import Product,Service,TaxDue,ProductTaxDetails,ServiceTaxDetails
# Register your models here.
admin.site.register(Product)
admin.site.register(Service)

admin.site.register(TaxDue)

admin.site.register(ProductTaxDetails)

admin.site.register(ServiceTaxDetails)