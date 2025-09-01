# In profiles/backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None
        
        # Try to find a user matching either the username or the email
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        
        try:
            user = UserModel.objects.get(**kwargs)
        except UserModel.DoesNotExist:
            return None # No user found, authentication fails

        # Check the password and that the user is active
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None