from django.contrib import admin
from django.conf import settings

# External
from django_hosts import patterns, host

from domains.urls import adminurls

from api import urls as apiurls

host_patterns = patterns(
    "",
    host(r"www", settings.ROOT_URLCONF, name="www"),
    host(r"api", apiurls, name="api"),
    host(r"admin", adminurls, name="admin"),
)
