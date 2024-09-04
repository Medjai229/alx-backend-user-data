#!/usr/bin/env python3
""" Authentication module for the API
"""

from flask import request
from typing import List, TypeVar
from models.user import User
from os import getenv


USR = TypeVar('User')


class Auth():
    """ Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if the given request path is not in the list of
        excluded paths and returns False if it is, and True if it is not.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        s_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                s_excluded_path = excluded_path[:-1].rstrip('/')
                if s_path.startswith(s_excluded_path):
                    return False
            else:
                s_excluded_path = excluded_path.rstrip('/')
                if s_path == s_excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the value of the Authorization header from a request
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> USR:
        """ public method
        """
        return None

    def session_cookie(self, request=None):
        """ Returns the value of the session cookie from a request
        """
        if request is None:
            return None

        session_name = getenv('SESSION_NAME')

        if session_name is None:
            return None

        cookie = request.cookies.get(session_name)
        return cookie
