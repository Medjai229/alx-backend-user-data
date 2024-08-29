#!/usr/bin/env python3
"""
File: encrypt_password.py

This module provides functions to hash a password and to verify a given
password against a hashed password.

Author: Malik Hussein
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password for storing.
    """
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(b'password', salt)
    return hashed_pw
