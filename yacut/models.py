from datetime import datetime
from urllib.parse import urlparse
from random import sample
import re

from flask import url_for

from . import db
from settings import (
    SHORT_LINK_SYMBOLS, SHORT_LINK_ATTEMPS, SHORT_LINK_LENGTH,
    MAX_URL_LENGTH, USER_SHORT_LINK_LENGTH, SHORT_LINK_PATTERN
)


CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя "{name}" уже занято.'
INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
INCORRECT_URL_MESSAGE = 'Введен неправильный URL'
SHORT_ID_GENERATION_ERROR_MESSAGE = (
    'Ошибка автоматического создания короткой ссылки'
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(length=MAX_URL_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(length=SHORT_LINK_LENGTH),
        nullable=False,
        unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'mapping_view',
                short_link=self.short,
                _external=True
            )
        )

    @staticmethod
    def short_link_is_free(short):
        return not URLMap.get_by_short_link(short)

    @staticmethod
    def validate_url(url):
        if len(url) > MAX_URL_LENGTH:
            raise ValueError(INCORRECT_URL_MESSAGE)
        parsed_url = urlparse(url)
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValueError(INCORRECT_URL_MESSAGE)
        return url

    @staticmethod
    def validate_short_link(short):
        if len(short) > USER_SHORT_LINK_LENGTH:
            raise ValueError(INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE)
        if not URLMap.short_link_is_free(short):
            raise ValueError(
                CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=short)
            )
        if not re.fullmatch(SHORT_LINK_PATTERN, short):
            raise ValueError(INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE)
        return short

    @staticmethod
    def get_by_short_link(short_link):
        return URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(SHORT_LINK_ATTEMPS):
            short_link = ''.join(sample(SHORT_LINK_SYMBOLS, SHORT_LINK_LENGTH))
            if URLMap.short_link_is_free(short_link):
                return short_link
        raise RuntimeError(SHORT_ID_GENERATION_ERROR_MESSAGE)

    @staticmethod
    def create(original, short=None, validate=False):
        if not short:
            short = URLMap.get_unique_short_id()
        elif validate:
            short = URLMap.validate_short_link(short)
            original = URLMap.validate_url(original)
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap
