
from gst.models import ProductTaxDetails,Product,ServiceTaxDetails,Service

def CaculateTaxonProduct(item:ProductTaxDetails):
    cgst,sgst,ugst,igst,cess = 0,0,0,0,0
    if item.interstate:
        igst += item.value * (item.product.taxrate/100)
    else:
        cgst += item.value * (item.product.taxrate/200)
        if item.taxpayer.isotherterritory:
            ugst += item.value * (item.product.taxrate/200)
        else:
            sgst += item.value * (item.product.taxrate/200)
    if item.product.cessrate is not None:
        cess += item.value * (item.product.cessrate/100)
    return round(cgst,2),round(sgst,2),round(ugst,2),round(igst,2),round(cess,2)

def CaculateTaxonService(item:ServiceTaxDetails):
    cgst,sgst,ugst,igst,cess = 0,0,0,0,0
    if item.interstate:
        igst += item.value * (item.service.taxrate/100)
    else:
        cgst += item.value * (item.service.taxrate/200)
        if item.taxpayer.isotherterritory:
            ugst += item.value * (item.service.taxrate/200)
        else:
            sgst += item.value * (item.service.taxrate/200)
    if item.service.cessrate is not None:
        cess += item.value * (item.service.cessrate/100)
    return round(cgst,2),round(sgst,2),round(ugst,2),round(igst,2),round(cess,2)
    