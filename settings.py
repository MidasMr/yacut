import os
import re
from string import ascii_letters, digits

SHORT_LINK_SYMBOLS = ascii_letters + digits
MAX_URL_LENGTH = 2048
SHORT_LINK_ATTEMPS = 5
SHORT_LINK_LENGTH = 6
SHORT_LINK_PATTERN = re.compile(f'^[{SHORT_LINK_SYMBOLS}]+$')
USER_SHORT_LINK_LENGTH = 16
URL_PATTERN = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
)


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
