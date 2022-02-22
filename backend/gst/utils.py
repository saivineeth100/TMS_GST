from decimal import Decimal

def CaculateTaxonProduct(item):
    cgst,sgst,ugst,igst,cess = 0,0,0,0,0
    if item.interstate:
        igst += item.value * Decimal(item.product.taxrate/100)
    else:
        cgst += item.value * Decimal(item.product.taxrate/200)
        if item.taxpayer.isotherterritory:
            ugst += item.value * Decimal(item.product.taxrate/200)
        else:
            sgst += item.value * Decimal(item.product.taxrate/200)
    if item.product.cessrate is not None:
        cess += item.value * Decimal(item.product.cessrate/100)
    return round(cgst,2),round(sgst,2),round(ugst,2),round(igst,2),round(cess,2)

def CaculateTaxonService(item):
    cgst,sgst,ugst,igst,cess = 0,0,0,0,0
    if item.interstate:
        igst += item.value * Decimal(item.service.taxrate/100)
    else:
        cgst += item.value * Decimal(item.service.taxrate/200)
        if item.taxpayer.isotherterritory:
            ugst += item.value * Decimal(item.service.taxrate/200)
        else:
            sgst += item.value * Decimal(item.service.taxrate/200)
    if item.service.cessrate is not None:
        cess += item.value * Decimal(item.service.cessrate/100)
    return round(cgst,2),round(sgst,2),round(ugst,2),round(igst,2),round(cess,2)
    