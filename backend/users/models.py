from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser as BaseAbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

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

class TaxPayer(AbstractUser):
    taxaccountants = models.ManyToManyField('users.TaxAccountant',blank=True)
    temppassword = models.CharField(max_length=50,null=TRUE) # Can login once only - will be created if Taxpayer is created by TaxAccountant or Admin
    istemppassword = models.BooleanField(default=False)
    class Meta:
        db_table  = 'TaxPayers'

class TaxAccountant(AbstractUser):    
    taxpayers = models.ManyToManyField(TaxPayer,blank=True,through=TaxPayer.taxaccountants.through)
    class Meta:
        db_table  = 'TaxAccountants'