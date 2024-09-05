#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from api.v1.views.users import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handles login API call, authenticates user and returns user JSON
    along with a Set-Cookie header for session ID.
    """
    email = request.form.get('email')

    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    session_name = getenv('SESSION_NAME')

    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False
                 )
def logout():
    """ Deletes the user session by removing the session ID from the
    storage.
    """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
