from .authentication import Authenticate, oauth2_scheme

auth_service = Authenticate()

__all__ = ['auth_service', 'oauth2_scheme']