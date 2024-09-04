#!/usr/bin/env python3
""" Session Authentication module for the API
"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from api.v1.views.users import User


class SessionAuth(Auth):
    """ Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a new session for a given user_id
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None

        session_id = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ Retrieves the User instance based on a Request object
        """
        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)
