from ninja.security import APIKeyHeader
from optimizer.models import AccessTokens
from ninja.errors import HttpError

class ApiKey(APIKeyHeader):
    param_name = 'X-API-Key'

    def authenticate(self, request, key):
        try:
            return AccessTokens.objects.get(token=key).user
        except AccessTokens.DoesNotExist:
            raise HttpError(401, 'X-API-Key não informado ou inválido')