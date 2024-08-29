#!/usr/bin/env python3
"""
file: filtered_logger.py

A module that provides a logger that filters out sensitive data

Author: Malik Hussein
"""

from typing import List
import re
import logging
from os import environ
from mysql.connector import connection

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filter a log message by replacing sensitive data
    """
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator,
                      field + "=" + redaction + separator, temp)
    return temp


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor for RedactingFormatter class
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record and filters out sensitive data
        """
        return filter_datum(self.fields,
                            self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR
                            )


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object that logs at the INFO level
    and writes to stdout. The logger is configured to redact
    sensitive data from the log output.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connection object to the MySQL database.
    """
    username = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = environ.get('PERSONAL_DATA_DB_NAME')

    connector = connection.MySQLConnection(
        user=username,
        password=password,
        host=db_host,
        database=db_name
    )

    return connector


def main() -> None:

    """
    Connects to a MySQL database and logs each user's information to stdout,
    redacting sensitive fields in the log output.
    """
    db = get_db()
    cursor = db.cursor()

    query = ('SELECT * FROM users;')
    cursor.execute(query)
    fetched_data = cursor.fetchall()

    logger = get_logger()

    for row in fetched_data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])

        logger.info(fields)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
