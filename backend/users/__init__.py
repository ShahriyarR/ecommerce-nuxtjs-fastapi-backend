from .authentication import Authenticate, oauth2_scheme, get_current_active_user, check_if_user_is_admin

auth_service = Authenticate()

__all__ = ['auth_service', 'oauth2_scheme', 'get_current_active_user', 'check_if_user_is_admin']