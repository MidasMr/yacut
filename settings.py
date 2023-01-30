import os
import re
from string import ascii_letters, digits

URL_SYMBOLS = ascii_letters + digits
SHORT_LINK_ATTEMPS = 5
SHORT_LINK_LENGTH = 6
SHORT_LINK_PATTERN = re.compile(r'^[a-zA-Z0-9_]+$')
USER_SHORT_LINK_LENGTH = 16


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
