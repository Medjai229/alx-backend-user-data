#!/usr/bin/env python3

from typing import List
import re
import logging

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Filter a log message by replacing sensitive data
    """
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator, field + "=" + redaction + separator, temp)

    return temp
