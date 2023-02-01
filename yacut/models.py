from datetime import datetime
from random import sample
import re

from flask import url_for

from . import db
from settings import (
    SHORT_LINK_SYMBOLS, SHORT_LINK_ATTEMPS, SHORT_LINK_LENGTH,
    MAX_URL_LENGTH, USER_SHORT_LINK_LENGTH, SHORT_LINK_PATTERN,
    URL_PATTERN
)


API_CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя "{name}" уже занято.'
CUSTOM_ID_ALREADY_EXISTS_MESSAGE = 'Имя {name} уже занято!'
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
        if URLMap.get_by_short_link(short):
            raise ValueError(
                CUSTOM_ID_ALREADY_EXISTS_MESSAGE.format(name=short)
            )
        return True

    @staticmethod
    def validate_url(url):
        if re.match(URL_PATTERN, url) is None:
            raise ValueError(INCORRECT_URL_MESSAGE)
        return True

    @staticmethod
    def validate_short_link(short):
        if len(short) > USER_SHORT_LINK_LENGTH:
            raise ValueError(INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE)
        if not re.fullmatch(SHORT_LINK_PATTERN, short):
            raise ValueError(INCORRECT_NAME_FOR_SHORT_LINK_MESSAGE)
        return True

    @staticmethod
    def get_by_short_link(short_link):
        return URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(SHORT_LINK_ATTEMPS):
            url = ''.join(sample(SHORT_LINK_SYMBOLS, SHORT_LINK_LENGTH))
            if URLMap.get_by_short_link(url):
                continue
            return url
        raise ValueError(SHORT_ID_GENERATION_ERROR_MESSAGE)

    @staticmethod
    def create(original, short=None, validate=False):
        if not short:
            short = URLMap.get_unique_short_id()
        elif validate:
            URLMap.validate_url(original)
            URLMap.validate_short_link(short)
        else:
            URLMap.short_link_is_free(short)
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap
