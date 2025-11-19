from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class with additional validation if needed.
    """
    
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        
        return self.get_user(validated_token), validated_token


def get_user_from_token(request):
    """
    Utility function to get user from JWT token.
    """
    auth = CustomJWTAuthentication()
    try:
        user, token = auth.authenticate(request)
        return user
    except AuthenticationFailed:
        return None