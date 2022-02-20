from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from users.models import TaxAccountant,TaxPayer,AdminUser

# Register your models here.

@admin.register(TaxAccountant)
class UserAdmin(BaseUserAdmin):
    pass
@admin.register(TaxPayer)
class UserAdmin(BaseUserAdmin):
    pass
@admin.register(AdminUser)
class UserAdmin(BaseUserAdmin):
    pass