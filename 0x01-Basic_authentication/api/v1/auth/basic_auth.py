#!/usr/bin/env python3
""" Basic Authentication module for the API
"""

from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


USR = TypeVar('User')


class BasicAuth(Auth):
    """ Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts and returns the Base64 part of the Authorization header.
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes a Base64-encoded string, returning the decoded string.
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header,
                validate=True
                )
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts and returns the user email and password from the
        decoded Base64 Authorization header.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> USR:
        """ Returns the User object corresponding to
        the given email address and password.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users = User.search({'email': user_email})

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

        except Exception:
            return None

        return None

    def current_user(self, request=None) -> USR:
        """
        Overwrite current_user method from Auth class
        """
        auth = self.authorization_header(request)
        encoded_base64 = self.extract_base64_authorization_header(auth)
        decoded_base64 = self.decode_base64_authorization_header(
            encoded_base64)
        email, password = self.extract_user_credentials(decoded_base64)
        return self.user_object_from_credentials(email, password)
