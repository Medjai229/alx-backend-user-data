#!/usr/bin/env python3
""" Authentication module for the API
"""

from flask import request
from typing import List, TypeVar
from models.user import User


USR = TypeVar('User')


class Auth():
    """ Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ public method
        """
        return None

    def current_user(self, request=None) -> USR:
        """ public method
        """
        return None
