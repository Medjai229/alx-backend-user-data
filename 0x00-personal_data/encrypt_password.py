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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verifies a given password against a hashed password.
    """
    if bcrypt.checkpw(b'password', hashed_password):
        return True
    return False
