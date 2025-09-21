# core/authentication.py

import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions

# Import both of your models
from .models import CustomUser, SupabaseUser

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) != 2:
            raise exceptions.AuthenticationFailed('Invalid token header.')

        token = auth_header[1].decode('utf-8')

        try:
            payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=['HS256'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise exceptions.AuthenticationFailed('Invalid or expired token.')

        user_id_from_token = payload.get('sub')
        if not user_id_from_token:
            raise exceptions.AuthenticationFailed('Invalid payload in token.')

        try:
            # Query the Supabase DB directly using our unmanaged model
            supabase_user = SupabaseUser.objects.get(id=user_id_from_token)

            # Extract the role from the JSON metadata field
            user_role = supabase_user.raw_app_meta_data.get('role', 'student')

        except SupabaseUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found in Supabase.')

        # Get or create a local Django user to represent this session.
        django_user, created = CustomUser.objects.update_or_create(
            id=user_id_from_token,
            defaults={
                'email': supabase_user.email,
                'username': supabase_user.email,
                'role': user_role
            }
        )

        return (django_user, token)