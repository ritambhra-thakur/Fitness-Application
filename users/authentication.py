
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    '''
        Security Warning: Don't use this production environment
    '''
    def enforce_csrf(self, request):
        pass