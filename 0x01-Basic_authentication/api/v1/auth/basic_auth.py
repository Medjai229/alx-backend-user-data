#!/usr/bin/env python3
""" Basic Authentication module for the API
"""

from api.v1.auth.auth import Auth
import base64


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
