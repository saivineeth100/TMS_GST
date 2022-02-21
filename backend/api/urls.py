
from django.contrib import admin
from django.urls import path,include
from users.views.apiviews import TaxPayersAPIView
from gst.views import TaxDuesView
from api.auth.urls import urlpatterns as authurls

urlpatterns = [
    path('taxpayers/', TaxPayersAPIView.as_view(),name="taxpayers"),
    path('taxpayers/<int:id>/', TaxPayersAPIView.as_view(),name="taxpayers"),
    path('taxdues/', TaxDuesView.as_view(),name="taxdues"),
    path('taxdues/<int:id>/', TaxDuesView.as_view(),name="taxdue"),
    path('auth/',include(authurls))
]
