from django.contrib.auth.backends import ModelBackend
from users.models import TaxAccountant,TaxPayer


class GenericAuthBackend(ModelBackend):    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(self.UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = self.UserModel._default_manager.get_by_natural_key(username)
        except self.UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            self.UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id: int):
        try:
            user = self.UserModel._default_manager.get(pk=user_id)
        except self.UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
        
class TaxAccountantAuthBackend(GenericAuthBackend):
    UserModel = TaxAccountant

class TaxPayerAuthBackend(GenericAuthBackend):
    UserModel = TaxPayer