
from django.contrib import admin
from django.urls import path
from users.views.apiviews import TaxPayersAPIView
from api.auth.views import LoginView

urlpatterns = [
    path('taxpayers/', TaxPayersAPIView.as_view()),
    path('taxpayers/<int:id>/', TaxPayersAPIView.as_view()),
    path('login/',LoginView.as_view())
]
