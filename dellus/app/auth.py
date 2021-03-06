"""Contains classes related to JWT based auth"""
from flask_jwt_extended import (
    jwt_optional, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token, jwt_refresh_token_required)


class TokenAuth:
   
    def __init__(self, secret_key=None, access_expiry=None,
                 refresh_expiry=None):
        pass

    def create_access_token(self, identity):
        return create_access_token(identity=identity)

    def create_refresh_token(self):
        pass

    def create_token(self, identity):
        """return both refresh and access token"""
        token = dict(access_token=create_access_token(identity=identity),
                     refresh_token=create_refresh_token(identity=identity))
        return token

    def refresh(self, refresh_token):
        return create_access_token()

   
class APITokenAuth(TokenAuth):
   
    token_optional = jwt_optional
    token_required = jwt_required
    get_jwt_identity = get_jwt_identity
    jwt_refresh_token_required = jwt_refresh_token_required
