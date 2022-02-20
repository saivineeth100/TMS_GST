
from gst.models import TaxDetails


def CaculateTax(item:TaxDetails):
    cgst,sgst,ugst,igst,cess = 0,0,0,0,0
    if item.interstate:
        igst += item.value * (item.taxrate/100)
    else:
        cgst += item.value * (item.taxrate/200)
        if item.taxpayer.isotherterritory:
            ugst += item.value * (item.taxrate/200)
        else:
            sgst += item.value * (item.taxrate/200)
    if item.cessrate is not None:
        cess += item.value * (item.cessrate/100)
    return cgst,sgst,ugst,igst,cess


    